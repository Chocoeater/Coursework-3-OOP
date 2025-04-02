import json
from abc import ABC, abstractmethod
from src.vacancies import Vacancy
from pathlib import Path
from typing import List, Dict



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


class JSONSaver(BaseJSONSaver):
    def __init__(self, file_name='vacancies.json'):
        self.__file_name = file_name
        self.__path_to_file = Path('data', self.__file_name)
        if not self.__path_to_file.exists():
            self.__path_to_file.write_text('[]', encoding='utf-8')

    def _load_vacancies(self) -> List[Dict]:
        """Загружает список вакансий из файла"""
        with open(self.__path_to_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_vacancies(self, vacancies: List[Dict]) -> None:
        """Сохраняет список вакансий в файл"""
        with open(self.__path_to_file, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, indent=4, ensure_ascii=False)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл, если ее еще нет"""
        vacancies = self._load_vacancies()
        vacancy_data = vacancy.to_dict()
        print(vacancy_data)
        if not any(vac.get('url') == vacancy_data.get('url') for vac in vacancies):
            vacancies.append(vacancy_data)
            self._save_vacancies(vacancies)

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass

    def get_same_vacancy(self):
        pass
