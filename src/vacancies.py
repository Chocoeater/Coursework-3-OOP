import json
from abc import ABC, abstractmethod
from src.head_hunter_api import HeadHunterAPI


class BaseVacancy(ABC):

    @classmethod
    @abstractmethod
    def cast_to_object_list(cls, vacancies: list) -> list:
        """
        Обрабатывает JSON-строку и возвращает список объектов-вакансий
        :param vacancies: Список JSON-строк для формирования объектов
        :return: Список объектов
        """

    def __eq__(self, other) -> bool:
        """
        Равенство
        :param other: Объект BaseVacancy
        :return: True/False
        """

    def __ne__(self, other) -> bool:
        """
        Неравенство
        :param other: Объект BaseVacancy
        :return: True/False
        """

    def __lt__(self, other) -> bool:
        """
        Меньше
        :param other: Объект BaseVacancy
        :return: True/False
        """

    def __le__(self, other) -> bool:
        """
        Меньше или равно
        :param other: Объект BaseVacancy
        :return: True/False
        """

    def __gt__(self, other) -> bool:
        """
        Больше
        :param other: Объект BaseVacancy
        :return: True/False
        """

    def __ge__(self, other) -> bool:
        """
        Больше или равно
        :param other: Объект BaseVacancy
        :return: True/False
        """


class Vacancy(BaseVacancy):

    def __init__(self, name: str, url: str, solary: int, description: str, requirements: str):
        self.name = name
        self.url = url
        self.solary = solary
        self.description = description
        self.requirements = requirements

    @classmethod
    def get_vacancy(cls, json_str: dict):
        return cls(name=json_str['name'], url=json_str['alternate_url'],
                   solary=json_str['salary'] if json_str['salary'] else 0, description=json_str['snippet']['responsibility'],
                   requirements=json_str['snippet']['requirement'])

    @classmethod
    def cast_to_object_list(cls, vacancies: list) -> list:
        return [cls.get_vacancy(vacancy_dict) for vacancy_dict in vacancies]


if __name__ == '__main__':
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies('Python')
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    print(vacancies_list)