import pytest
from src.head_hunter_api import HeadHunterAPI
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = {'items': [{'id': 1, 'name': 'Python Developer'}]}
    mock.raise_for_status.return_value = None
    return mock


@pytest.fixture
def hh_api():
    return HeadHunterAPI()




