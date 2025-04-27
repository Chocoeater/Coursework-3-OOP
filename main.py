#
# from src.head_hunter_api import HeadHunterAPI
# from src.dbsaver import DBSaver
# from src.config import config
# from tests.conftest import hh_api
# from src.vacancies import Vacancy
#
# if __name__ == '__main__':
#     hh_api = HeadHunterAPI()
#     emp = hh_api.get_employers('Sber')
#     vac = hh_api.get_vacancies()
#     vacancies = dict()
#     for key, value in vac.items():
#         new_data = Vacancy.cast_to_object_list(value)
#         vacancies[key] = new_data
#     db_saver = DBSaver()
#     db_saver.create_database()
#     db_saver.save_to_database(emp, vacancies)


from src.utils import user_interface

if __name__ == '__main__':
    user_interface()