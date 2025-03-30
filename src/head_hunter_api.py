from abc import ABC, abstractmethod
import requests


class BaseHeadHunterAPI(ABC):
    """
    Абстрактный класс для работы с API hh.ru
    """

    @abstractmethod
    def get_vacancies(self, keyword: str) -> str:
        """
        Получает вакансии с hh.ru
        :param keyword: Ключевое слово для поиска
        :return: Строка в формате JSON
        """


class HeadHunterAPI(BaseHeadHunterAPI):
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []

    def get_vacancies(self, keyword):
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1


if __name__ == '__main__':
    hh_api = HeadHunterAPI()
    hh_api.get_vacancies('Python')
    print(hh_api.vacancies)