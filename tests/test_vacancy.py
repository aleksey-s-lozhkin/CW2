import pytest

from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancy():
    """Фикстура с тестовой вакансией"""
    return Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/1",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Backend разработчик",
        responsibility="Разработка API",
        experience="1-3 года",
    )


@pytest.fixture
def vacancy_no_salary():
    """Фикстура с вакансией без зарплаты"""
    return Vacancy(
        title="Intern",
        url="https://hh.ru/vacancy/3",
        salary=None,
        description="Стажер",
        responsibility="Помощь команде",
        experience="Без опыта",
    )


def test_vacancy_creation(sample_vacancy):
    """Тест создания вакансии"""
    assert sample_vacancy.title == "Python Developer"
    assert sample_vacancy.url == "https://hh.ru/vacancy/1"
    assert sample_vacancy.salary["from"] == 100000


def test_comparison_salary():
    """Тест сравнения зарплат"""
    vacancy1 = Vacancy("Python Developer", "url1", {"from": 100000, "to": 150000}, "desc1", "resp1", "exp1")
    vacancy2 = Vacancy("Data Scientist", "url2", {"from": 120000}, "desc2", "resp2", "exp2")

    assert vacancy1._get_comparison_salary() == 125000
    assert vacancy2._get_comparison_salary() == 120000
    assert vacancy1 > vacancy2
    assert vacancy2 < vacancy1


def test_no_salary(vacancy_no_salary):
    """Тест вакансии без зарплаты"""
    assert vacancy_no_salary._get_comparison_salary() == 0


def test_to_dict(sample_vacancy):
    """Тест преобразования в словарь"""
    vacancy_dict = sample_vacancy.to_dict()
    assert vacancy_dict["title"] == "Python Developer"
    assert vacancy_dict["url"] == "https://hh.ru/vacancy/1"
    assert vacancy_dict["salary"]["from"] == 100000


def test_from_dict():
    """Тест создания из словаря"""
    data = {
        'title': 'Test',
        'url': 'https://test.ru',
        'salary': {'from': 50000},
        'description': 'Test desc',
        'responsibility': 'Test resp',
        'experience': 'Test exp',
    }
    vacancy = Vacancy.from_dict(data)
    assert vacancy.title == 'Test'
    assert vacancy.salary['from'] == 50000


def test_get_salary_display(sample_vacancy, vacancy_no_salary):
    """Тест отображения зарплаты"""

    display = sample_vacancy.get_salary_display()
    assert "100000" in display
    assert "150000" in display
    assert "RUR" in display

    assert vacancy_no_salary.get_salary_display() == "Не указана"


def test_str_representation(sample_vacancy):
    """Тест строкового представления"""
    str_repr = str(sample_vacancy)
    assert "Python Developer" in str_repr
    assert "https://hh.ru/vacancy/1" in str_repr
    assert "Зарплата:" in str_repr


def test_equality():
    """Тест равенства вакансий"""
    vacancy1 = Vacancy("Title", "url1", {"from": 100000}, "desc", "resp", "exp")
    vacancy2 = Vacancy("Title", "url2", {"from": 100000}, "desc", "resp", "exp")
    vacancy3 = Vacancy("Title", "url3", {"from": 200000}, "desc", "resp", "exp")

    assert vacancy1 == vacancy2

    assert vacancy1 != vacancy3
