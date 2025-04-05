from src.vacancies import Vacancy
from src.head_hunter_api import HeadHunterAPI
from src.json_saver import JSONSaver


if __name__ == '__main__':
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies('Python')
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    print(vacancies_list)
    json_saver = JSONSaver()
    for vac in vacancies_list:
        json_saver.add_vacancy(vac)