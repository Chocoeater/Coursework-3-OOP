from abc import ABC, abstractmethod



class BaseVacancy(ABC):
    __slots__ = ("name", "area", "url", "salary", "description", "requirements")

    @abstractmethod
    def _validation_salary(self, salary: dict | None) -> int:
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
    def __init__(self, name: str, area: str, url: str, salary: dict, description: str, requirements: str):
        self.name = name
        self.area = area
        self.url = url if url else "Не указано"
        self.salary = self._validation_salary(salary)
        self.description = description if description else "Не указано"
        self.requirements = requirements if requirements else "Не указано"

    def _validation_salary(self, salary: dict | None) -> dict:
        if not salary:
            return {"from": 0, "to": 0, "currency": "RUR", "gross": False}
        else:
            return salary

    @classmethod
    def get_vacancy(cls, json_str: dict):
        return cls(
            name=json_str["name"],
            area=json_str["area"]["name"],
            url=json_str["alternate_url"],
            salary=json_str["salary"],
            description=json_str["snippet"]["responsibility"],
            requirements=json_str["snippet"]["requirement"],
        )

    @classmethod
    def cast_to_object_list(cls, vacancies: list) -> list:
        return [cls.get_vacancy(vacancy_dict) for vacancy_dict in vacancies]

    @staticmethod
    def _get_left_right(left: int | dict, right: int | dict) -> tuple:
        if left:
            left = left["from"]
        if right:
            right = right["from"]
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
            "name": self.name,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
            "requirements": self.requirements,
        }
        return data
