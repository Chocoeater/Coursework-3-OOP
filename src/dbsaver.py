import psycopg2
from src.config import config
from src.vacancies import Vacancy

class DBSaver:
    """Создание базы данных"""

    def __init__(self):
        self.params = config()
        self.dbname = 'headhunter'

    def create_database(self) -> None:
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE IF EXISTS {self.dbname}')
        cur.execute(f'CREATE DATABASE {self.dbname}')

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=f'{self.dbname}', **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers (
                    employers_id SERIAL PRIMARY KEY,
                    name_employer VARCHAR(255) NOT NULL,
                    url VARCHAR(255)
                )
                """
            )

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employers_id INT REFERENCES employers(employers_id),
                    name_vacancy VARCHAR(255) NOT NULL,
                    area VARCHAR(255),
                    url VARCHAR(255),
                    salary INT,
                    description TEXT,
                    requirements TEXT
                )
                """
            )

        conn.commit()
        conn.close()

    def save_to_database(self, employers, vacancies) -> None:
        """Сохраняет данные в базу"""
        conn = psycopg2.connect(dbname=f'{self.dbname}', **self.params)

        with conn.cursor() as cur:
            for emp in employers:
                cur.execute(
                    """
                    INSERT INTO employers (name_employer, url)
                    VALUES (%s, %s)
                    RETURNING employers_id
                    """,
                    (emp['name'], emp['alternate_url'])
                )
                employer_id = cur.fetchone()[0]
                for vac in vacancies[f'{employer_id}']:
                    cur.execute(
                        """
                        INSERT INTO vacancies (employers_id, name_vacancy, area, url, salary, description, requirements)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (employer_id, vac.name, vac.area, vac.url, vac.salary['from'], vac.description, vac.requirements)
                    )

        conn.commit()
        conn.close()



