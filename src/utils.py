from src.dbmanager import DBManager
from src.dbsaver import DBSaver
from src.head_hunter_api import HeadHunterAPI
from src.vacancies import Vacancy


def print_vacancies(vacancies):
    for vac in vacancies:
        print('-' * 50)
        print(f"Компания: {vac[0]}")
        print(f"Вакансия: {vac[1]}")
        print(f"Зарплата: {vac[2]}")
        print(f"Ссылка: {vac[3]}")
    print('-' * 50)


def user_interface():
    print('Добро пожаловать в систему вакансий HeadHunter!')

    keyword = input('Введите ключевое слово для поиска работодателей (Например, Сбербанк или Яндекс): ')

    print(f'Парсим данные по ключевому слову "{keyword}". . .')

    hh_api = HeadHunterAPI()
    employers = hh_api.get_employers(keyword, pages=1)
    print(f'Найдено {len(employers)} работодателей.')

    print('Получаем вакансии. . .')
    vac = hh_api.get_vacancies()
    vacancies = dict()
    for key, value in vac.items():
        new_data = Vacancy.cast_to_object_list(value)
        vacancies[key] = new_data

    print('Формируем и заполняем базу данных. . .')
    db_saver = DBSaver()
    db_saver.create_database()
    db_saver.save_to_database(employers, vacancies)
    print('✅ База данный успешно создана и заполнена!\n')

    db = DBManager()

    while True:
        print("\n Меню:")
        print("1 — Список компаний и количество вакансий")
        print("2 — Список всех вакансий (название, зп, ссылка)")
        print("3 — Средняя зарплата")
        print("4 — Вакансии с зарплатой выше средней")
        print("5 — Поиск по ключевому слову в названии вакансии")
        print("0 — Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            data = db.get_companies_and_vacancies_count()
            print("\nКомпании и количество вакансий:")
            for row in data:
                print(f"{row[0]} — {row[1]} вакансий")

        elif choice == "2":
            vacancies = db.get_all_vacancies()
            print("\nВсе вакансии:")
            print_vacancies(vacancies)

        elif choice == "3":
            avg = db.get_avg_salary()
            print(f"\nСредняя зарплата: {int(avg)} руб.")

        elif choice == "4":
            avg_salary = db.get_avg_salary()
            vacancies = db.get_vacancies_with_higher_salary(avg_salary)
            print("\nВакансии с зарплатой выше средней:")
            print_vacancies(vacancies)

        elif choice == "5":
            keyword = input("Введите ключевое слово: ").strip()
            vacancies = db.get_vacancies_with_keyword(keyword)
            print(f"\nВакансии с ключевым словом '{keyword}':")
            print_vacancies(vacancies)

        elif choice == "0":
            print("👋 Выход из программы.")
            break

        else:
            print("❗ Неверный ввод. Попробуйте снова.")
