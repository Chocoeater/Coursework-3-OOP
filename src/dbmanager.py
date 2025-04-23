from abc import ABC, abstractmethod
from src.dbsaver import DBSaver
from src.config import config
import psycopg2


class BaseDBManager(ABC):
    """Абстрактный класс для задания необходимого интерфейса дочерним классам"""

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        pass

    @abstractmethod
    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self, avg_salary: float):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        pass


class DBManager(BaseDBManager):
    def __init__(self):
        self.params = config()
        self.dbname = 'headhunter'

    def get_companies_and_vacancies_count(self):
        conn = psycopg2.connect(dbname=f'{self.dbname}', **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name_employer, COUNT(v.vacancy_id) AS vacancies_count
                FROM employers e
                LEFT JOIN vacancies v ON e.employers_id = v.employers_id
                GROUP BY e.name_employer
                ORDER by vacancies_count DESC
                """
            )
            result = cur.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self):
        conn = psycopg2.connect(dbname=f'{self.dbname}', **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name_employer, v.name_vacancy, v.salary, v.url
                FROM vacancies v
                LEFT JOIN employers e USING(employers_id)
                ORDER BY v.salary DESC
                """
            )
            result = cur.fetchall()
        conn.close()
        return result

    def get_avg_salary(self):
        conn = psycopg2.connect(dbname=f'{self.dbname}', **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(v.salary)
                FROM vacancies v
                WHERE v.salary IS NOT NULL and v.salary <> 0
                """
            )
            result = cur.fetchone()[0]
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self, avg_salary: float):
        conn = psycopg2.connect(dbname=f'{self.dbname}', **self.params)

        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT e.name_employer, v.name_vacancy, v.salary, v.url
                FROM vacancies v
                LEFT JOIN employers e USING(employers_id)
                WHERE v.salary > {avg_salary}
                """
            )
            result = cur.fetchall()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        conn = psycopg2.connect(dbname=f'{self.dbname}', **self.params)

        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT e.name_employer, v.name_vacancy, v.salary, v.url
                FROM vacancies v
                LEFT JOIN employers e USING(employers_id)
                WHERE LOWER(name_vacancy) LIKE '%{keyword.lower()}%'
                ORDER BY salary DESC
                """
            )
            result = cur.fetchall()
        conn.close()
        return result