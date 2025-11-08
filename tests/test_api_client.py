import json
import os
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

from src.api_client import HeadHunterAPIClient
from src.vacancy import Vacancy


@pytest.fixture
def api_client():
    """Фикстура с API клиентом"""
    return HeadHunterAPIClient()


@pytest.fixture
def mock_response():
    """Фикстура с мок-ответом от API"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "items": [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/1",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "professional_roles": [{"name": "Программист"}],
                "snippet": {"responsibility": "Разработка приложений"},
                "experience": {"name": "1-3 года"},
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_response.status_code = 200
    return mock_response


def test_init(api_client):
    """Тест инициализации клиента"""
    assert api_client._HeadHunterAPIClient__base_url == 'https://api.hh.ru/vacancies'


@patch('src.api_client.requests.get')
def test_request_success(mock_get, api_client, mock_response):
    """Тест успешного запроса к API"""
    mock_get.return_value = mock_response

    response = api_client._HeadHunterAPIClient__request({"text": "python"})

    mock_get.assert_called_once_with('https://api.hh.ru/vacancies', params={"text": "python"})
    assert response == mock_response


@patch('src.api_client.requests.get')
def test_request_without_params(mock_get, api_client):
    """Тест запроса без параметров"""
    mock_response = Mock()
    mock_get.return_value = mock_response

    api_client._HeadHunterAPIClient__request()

    mock_get.assert_called_once_with('https://api.hh.ru/vacancies', params={})


@patch('src.api_client.HeadHunterAPIClient._HeadHunterAPIClient__request')
def test_get_vacancies_success(mock_request, api_client, mock_response):
    """Тест успешного получения вакансий"""
    mock_request.return_value = mock_response

    result = api_client.get_vacancies("python")

    mock_request.assert_called_once_with({"text": "python", "area": 113, "per_page": 30})
    assert len(result) == 1
    assert result[0]["name"] == "Python Developer"


@patch('src.api_client.HeadHunterAPIClient._HeadHunterAPIClient__request')
def test_get_vacancies_http_error(mock_request, api_client):
    """Тест обработки HTTP ошибки"""
    # Используем конкретное исключение HTTPError
    mock_request.side_effect = requests.exceptions.HTTPError("HTTP Error")

    result = api_client.get_vacancies("python")

    assert result == []


def test_convert_vacancy():
    """Тест преобразования данных в объекты Vacancy"""
    raw_data = [
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/1",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "professional_roles": [{"name": "Программист"}],
            "snippet": {"responsibility": "Разработка приложений"},
            "experience": {"name": "1-3 года"},
        }
    ]

    vacancies = HeadHunterAPIClient._convert_vacancy(raw_data)

    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"
    assert vacancies[0].url == "https://hh.ru/vacancy/1"


@patch('src.api_client.HeadHunterAPIClient.get_vacancies')
def test_get_vacancies_as_objects(mock_get_vacancies, api_client):
    """Тест получения вакансий в виде объектов"""
    mock_get_vacancies.return_value = [
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/1",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "professional_roles": [{"name": "Программист"}],
            "snippet": {"responsibility": "Разработка приложений"},
            "experience": {"name": "1-3 года"},
        }
    ]

    vacancies = api_client.get_vacancies_as_objects("python")

    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)


@patch('src.api_client.HeadHunterAPIClient.get_vacancies')
@patch('src.api_client.json.dump')
@patch('src.api_client.open')
@patch('src.api_client.os.makedirs')
def test_save_vacancies_to_json_success(mock_makedirs, mock_open, mock_json_dump, mock_get_vacancies, api_client):
    """Тест успешного сохранения вакансий в JSON"""
    mock_get_vacancies.return_value = [{"name": "Python Developer"}]

    result = api_client.save_vacancies_to_json("python", "test.json")

    assert result is True
    mock_makedirs.assert_called_once_with(os.path.dirname("test.json"), exist_ok=True)
    mock_open.assert_called_once_with("test.json", 'w', encoding='utf-8')
    mock_json_dump.assert_called_once()


@patch('src.api_client.HeadHunterAPIClient.get_vacancies')
@patch('src.api_client.json.dump')
@patch('src.api_client.open')
@patch('src.api_client.os.makedirs')
def test_save_vacancies_to_json_default_filename(
    mock_makedirs, mock_open, mock_json_dump, mock_get_vacancies, api_client
):
    """Тест сохранения с именем файла по умолчанию"""
    mock_get_vacancies.return_value = [{"name": "Python Developer"}]

    result = api_client.save_vacancies_to_json("python")

    assert result is True
    mock_makedirs.assert_called_once_with(os.path.dirname('data/raw_json.json'), exist_ok=True)
    mock_open.assert_called_once_with('data/raw_json.json', 'w', encoding='utf-8')


@patch('src.api_client.requests.get')
def test_request_http_error(mock_get, api_client):
    """Тест обработки HTTP ошибок в запросе"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    mock_response.url = "https://api.hh.ru/vacancies"
    mock_response.text = "Error message"
    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        api_client._HeadHunterAPIClient__request({"text": "python"})
