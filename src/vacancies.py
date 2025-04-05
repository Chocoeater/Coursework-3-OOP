import json
from abc import ABC, abstractmethod
from src.head_hunter_api import HeadHunterAPI


class BaseVacancy(ABC):
    __slots__ = ['name', ' url', 'salary', 'description', 'requirements']

    @abstractmethod
    def __validation_salary(self, salary: int | None) -> int:
        """
        Валидирует значения заработной платы. Если заработная плата не задана, возвращает 0
        :param salary: Заработная плата
        :return: 0 или значение заработной платы
        """
        pass

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

    def __init__(self, name: str, url: str, salary: int, description: str, requirements: str):
        self.name = name
        self.url = url
        self.salary = self.__validation_salary(salary)
        self.description = description
        self.requirements = requirements

    def __validation_salary(self, salary: int | None) -> int:
        if salary:
            return int(salary)
        else:
            return 0

    @classmethod
    def get_vacancy(cls, json_str: dict):
        return cls(name=json_str['name'], url=json_str['alternate_url'],
                   salary=json_str['salary'], description=json_str['snippet']['responsibility'],
                   requirements=json_str['snippet']['requirement'])

    @classmethod
    def cast_to_object_list(cls, vacancies: list) -> list:
        return [cls.get_vacancy(vacancy_dict) for vacancy_dict in vacancies]

    @staticmethod
    def _get_left_right(left: int | dict, right: int | dict) -> tuple:
        if left:
            left = left['from']
        if right:
            right = right['from']
        return left, right

    def __eq__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left == right

    def __ne__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left != right

    def __lt__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left < right

    def __le__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left <= right

    def __gt__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left > right

    def __ge__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left >= right

    def to_dict(self) -> dict:
        """
        Возвращает словарь с атрибутами объекта
        :return: Словарь с атрибутами
        """
        data = {
            'name': self.name,
            'url': self.url,
            'salary': self.salary,
            'description': self.description,
            'requirements': self.requirements
        }
        return data




if __name__ == '__main__':
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies('Python')
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    listik = [vac.salary for vac in vacancies_list]
    print(listik)
    print([listik[0] == listik[i] for i in range(len(listik))])