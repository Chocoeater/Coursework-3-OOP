from abc import ABC, abstractmethod
import requests
from requests.exceptions import HTTPError, RequestException


class BaseHeadHunterAPI(ABC):
    """
    Абстрактный класс для работы с API hh.ru
    """

    @abstractmethod
    def __connect_to_API(self, keyword: str) -> None:
        """
        Подключается к API hh.ru и сохраняет вакансии в список
        :param keyword: Ключевое слово для поиска вакансий
        :return: None
        """
    @abstractmethod
    def get_vacancies(self, keyword: str) -> str:
        """
        Возвращает список собранных вакансий при помощи API
        :param keyword: Ключевое слово для поиска
        :return: Список словарей с вакансиями
        """


class HeadHunterAPI(BaseHeadHunterAPI):
    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []

    def __connect_to_API(self, keyword, pages=1):
        self.__params['text'] = keyword
        try:
            while self.__params.get('page') != pages:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                response.raise_for_status()
                vacancies = response.json().get('items', '')
                self.__vacancies.extend(vacancies)
                self.__params['page'] += 1
        except HTTPError as e:
            print(f"Ошибка API: {e}")
            return None
        except RequestException as e:
            print(f'Сетевая ошибка: {e}')
            return None


    def get_vacancies(self, keyword, pages=1):
        self.__connect_to_API(keyword, pages)
        return self.__vacancies


if __name__ == '__main__':
    hh_api = HeadHunterAPI()
    hh_api.get_vacancies('Python')
    print(hh_api.__vacancies)