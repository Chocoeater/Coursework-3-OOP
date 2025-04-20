from abc import ABC, abstractmethod
import requests
from requests.exceptions import HTTPError, RequestException


class BaseHeadHunterAPI(ABC):
    @abstractmethod
    def _connect_to_api(self, keyword: str) -> None:
        pass

    @abstractmethod
    def get_employers(self, keyword: str) -> list:
        pass


class HeadHunterAPI(BaseHeadHunterAPI):
    def __init__(self):
        self.api_url = "https://api.hh.ru/employers"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "only_with_vacancies": True, "page": 0, "per_page": 100}
        self.__employers = []

    def _connect_to_api(self, keyword, pages: int = 1):
        self.__params["text"] = keyword
        self.__params["page"] = 0
        self.__employers = []
        try:
            while self.__params["page"] < pages:
                response = requests.get(self.api_url, headers=self.__headers, params=self.__params)
                response.raise_for_status()
                employers= response.json().get("items", [])
                self.__employers.extend(employers)
                self.__params["page"] += 1
        except HTTPError as e:
            print(f"Ошибка API: {e}")
        except RequestException as e:
            print(f"Сетевая ошибка: {e}")

    def get_employers(self, keyword, pages: int = 1) -> list:
        self._connect_to_api(keyword, pages)
        return self.__employers


