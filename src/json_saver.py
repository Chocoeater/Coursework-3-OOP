from abc import ABC, abstractmethod
from src.vacancies import Vacancy


class BaseJSONSaver(ABC):
    """
    Базовый абстрактный класс для задания интерфейса сохранения в файл вакансий
    """
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в файл
        :param vacancy: Объект-вакансия
        :return: None
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из файла
        :param vacancy: Объект-вакансия
        :return: None
        """
        pass

    @abstractmethod
    def get_same_vacancy(self):
        pass
