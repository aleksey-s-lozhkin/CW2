import os
import tempfile

import pytest

from src.vacancy import Vacancy
from src.vacancy_storage import JSONVacancyStorage


@pytest.fixture
def temp_storage():
    """Фикстура с временным хранилищем"""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        temp_path = f.name

    storage = JSONVacancyStorage(temp_path)
    yield storage

    # Очистка после теста
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def sample_vacancy():
    """Фикстура с тестовой вакансией"""
    return Vacancy(
        title="Test Developer",
        url="https://hh.ru/vacancy/test",
        salary={"from": 100000, "currency": "RUR"},
        description="Test description",
        responsibility="Test responsibility",
        experience="1-3 года",
    )


def test_add_vacancy(temp_storage, sample_vacancy):
    """Тест добавления вакансии"""
    temp_storage.add_vacancy(sample_vacancy)
    vacancies = temp_storage.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].title == "Test Developer"


def test_duplicate_vacancy(temp_storage, sample_vacancy):
    """Тест добавления дубликата вакансии"""
    temp_storage.add_vacancy(sample_vacancy)
    temp_storage.add_vacancy(sample_vacancy)  # Дубликат
    vacancies = temp_storage.get_vacancies()
    assert len(vacancies) == 1  # Должна остаться одна вакансия


def test_search_by_keyword(temp_storage, sample_vacancy):
    """Тест поиска по ключевому слову"""
    temp_storage.add_vacancy(sample_vacancy)

    # Поиск по названию
    result = temp_storage.get_vacancies({"keyword": "Developer"})
    assert len(result) == 1

    # Поиск по несуществующему слову
    result = temp_storage.get_vacancies({"keyword": "Nonexistent"})
    assert len(result) == 0


def test_clear_storage(temp_storage, sample_vacancy):
    """Тест очистки хранилища"""
    temp_storage.add_vacancy(sample_vacancy)
    temp_storage.clear_all()
    vacancies = temp_storage.get_vacancies()
    assert len(vacancies) == 0


def test_search_by_salary(temp_storage):
    """Тест поиска по зарплате"""
    high_salary_vacancy = Vacancy("Senior Dev", "url1", {"from": 200000}, "desc1", "resp1", "exp1")
    low_salary_vacancy = Vacancy("Junior Dev", "url2", {"from": 50000}, "desc2", "resp2", "exp2")

    temp_storage.add_vacancy(high_salary_vacancy)
    temp_storage.add_vacancy(low_salary_vacancy)

    # Поиск с минимальной зарплатой
    result = temp_storage.get_vacancies({"salary_min": 100000})
    assert len(result) == 1
    assert result[0].title == "Senior Dev"
