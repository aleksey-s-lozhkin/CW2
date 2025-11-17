from unittest.mock import Mock, patch

import pytest

from src.vacancy import Vacancy
from src.vacancy_manager import VacancyManager


@pytest.fixture
def manager_with_mocks():
    """Фикстура с менеджером вакансий с полными моками"""
    with (
        patch('src.vacancy_manager.HeadHunterAPIClient') as mock_api_class,
        patch('src.vacancy_manager.JSONVacancyStorage') as mock_storage_class,
    ):
        # Создаем моки
        mock_api = Mock()
        mock_storage = Mock()

        # Настраиваем классы моков
        mock_api_class.return_value = mock_api
        mock_storage_class.return_value = mock_storage

        # Создаем менеджер
        manager = VacancyManager("test_vacancies.json")

        # Сохраняем моки для доступа в тестах
        manager.mock_api = mock_api
        manager.mock_storage = mock_storage

        return manager


@pytest.fixture
def mock_vacancies():
    """Фикстура с мок-вакансиями"""
    return [
        Vacancy("Python Dev", "url1", {"from": 100000}, "desc1", "resp1", "exp1"),
        Vacancy("Java Dev", "url2", {"to": 90000}, "desc2", "resp2", "exp2"),
    ]


def test_search_vacancies(manager_with_mocks, mock_vacancies):
    """Тест поиска вакансий"""
    # Настраиваем мок API
    manager_with_mocks.mock_api.get_vacancies_as_objects.return_value = mock_vacancies

    # Вызываем метод
    result = manager_with_mocks.search_vacancies("Python")

    # Проверяем результат
    assert len(result) == 2  # Должно вернуть 2 вакансии
    assert result == mock_vacancies
    assert manager_with_mocks.current_vacancies == mock_vacancies

    # Проверяем вызов API - исправлено: убран параметр area
    manager_with_mocks.mock_api.get_vacancies_as_objects.assert_called_once_with(keyword="Python", per_page=50)


def test_save_current_vacancies(manager_with_mocks, mock_vacancies):
    """Тест сохранения вакансий"""
    manager_with_mocks.current_vacancies = mock_vacancies

    # Вызываем метод
    saved_count = manager_with_mocks.save_current_vacancies()

    # Проверяем вызовы к хранилищу
    assert manager_with_mocks.mock_storage.add_vacancy.call_count == 2
    assert saved_count == 2


def test_save_empty_vacancies(manager_with_mocks):
    """Тест сохранения пустого списка вакансий"""
    saved_count = manager_with_mocks.save_current_vacancies()
    assert saved_count == 0
    manager_with_mocks.mock_storage.add_vacancy.assert_not_called()


def test_get_top_n_by_salary(manager_with_mocks):
    """Тест получения топа по зарплате"""
    # Настраиваем мок хранилища
    mock_vacancies = [
        Vacancy("High", "url1", {"from": 200000}, "desc1", "resp1", "exp1"),
        Vacancy("Medium", "url2", {"from": 150000}, "desc2", "resp2", "exp2"),
        Vacancy("Low", "url3", {"from": 100000}, "desc3", "resp3", "exp3"),
    ]
    manager_with_mocks.mock_storage.get_vacancies.return_value = mock_vacancies

    # Получаем топ-2
    top_2 = manager_with_mocks.get_top_n_by_salary(2)

    # Проверяем результат
    assert len(top_2) == 2
    # Проверяем, что вакансии отсортированы по убыванию зарплаты
    assert top_2[0]._Vacancy__get_comparison_salary() == 200000
    assert top_2[1]._Vacancy__get_comparison_salary() == 150000


def test_search_by_keyword(manager_with_mocks):
    """Тест поиска по ключевому слову"""
    # Настраиваем мок хранилища
    python_vacancy = Vacancy(
        "Python Developer", "url1", {"from": 100000}, "Python backend development", "Write Python code", "1-3 years"
    )

    # Тестируем поиск по Python
    manager_with_mocks.mock_storage.get_vacancies.return_value = [python_vacancy]
    result = manager_with_mocks.search_by_keyword("Python")
    assert len(result) == 1
    manager_with_mocks.mock_storage.get_vacancies.assert_called_with({'keyword': 'Python'})


def test_get_all_saved_vacancies(manager_with_mocks):
    """Тест получения всех сохраненных вакансий"""
    # Настраиваем мок хранилища
    mock_vacancies = [
        Vacancy("Dev1", "url1", {"from": 100000}, "desc1", "resp1", "exp1"),
        Vacancy("Dev2", "url2", {"from": 200000}, "desc2", "resp2", "exp2"),
    ]
    manager_with_mocks.mock_storage.get_vacancies.return_value = mock_vacancies

    # Получаем все вакансии
    all_vacancies = manager_with_mocks.get_all_saved_vacancies()
    assert len(all_vacancies) == 2
    manager_with_mocks.mock_storage.get_vacancies.assert_called_once_with()


def test_delete_vacancies(manager_with_mocks):
    """Тест удаления вакансий по критериям"""
    # Настраиваем мок хранилища
    # Симулируем, что до удаления было 2 вакансии, после - 1
    manager_with_mocks.mock_storage.get_vacancies.side_effect = [
        [Mock(), Mock()],  # Первый вызов - 2 вакансии до удаления
        [Mock()],  # Второй вызов - 1 вакансия после удаления
    ]

    # Удаляем по title
    deleted_count = manager_with_mocks.delete_vacancies({"title": "Python Dev"})

    # Проверяем вызов к хранилищу
    manager_with_mocks.mock_storage.del_vacancy.assert_called_once_with({"title": "Python Dev"})
    # Проверяем количество удаленных
    assert deleted_count == 1


def test_clear_storage(manager_with_mocks):
    """Тест очистки хранилища"""
    # Вызываем метод
    manager_with_mocks.clear_storage()

    # Проверяем вызов к хранилищу
    manager_with_mocks.mock_storage.clear_all.assert_called_once()
