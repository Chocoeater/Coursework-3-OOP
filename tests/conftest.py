import pytest
from src.head_hunter_api import HeadHunterAPI
from unittest.mock import patch, MagicMock
from src.vacancies import Vacancy
from src.json_saver import JSONSaver

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = {'items': [{'id': 1, 'name': 'Python Developer'}]}
    mock.raise_for_status.return_value = None
    return mock


@pytest.fixture
def hh_api():
    return HeadHunterAPI()

@pytest.fixture
def vacancy():
    vacancy = Vacancy.get_vacancy({
        'name': 'Тестовый',
        'area': {'name': 'Тестовый'},
        'alternate_url': 'http://example.com/vacancy/1',
        'salary': {'from': 100000, 'to': 150000, "currency": "RUR", "gross": False},
        'snippet': {'responsibility': 'Описание', 'requirement': 'Требование'},
    })
    return vacancy


@pytest.fixture
def json_saver(tmp_path):
    # Используем временную директорию pytest для изоляции тестов
    file_path = tmp_path / 'vacancies.json'
    saver = JSONSaver(file_name=str(file_path))
    # Переопределяем путь к файлу для тестов
    saver._JSONSaver__path_to_file = file_path
    return saver



