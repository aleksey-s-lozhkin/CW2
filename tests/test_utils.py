from src.utils import display_vacancies, get_salary_display
from src.vacancy import Vacancy


def test_get_salary_display_full_salary():
    """Тест отображения полной зарплаты"""
    vacancy = Vacancy(
        title="Developer",
        url="https://example.com",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Test",
        responsibility="Test",
        experience="Test",
    )
    result = get_salary_display(vacancy)
    assert result == "100000 - 150000 RUR"


def test_get_salary_display_from_salary():
    """Тест отображения зарплаты только с нижней границей"""
    vacancy = Vacancy(
        title="Developer",
        url="https://example.com",
        salary={"from": 120000, "currency": "USD"},
        description="Test",
        responsibility="Test",
        experience="Test",
    )
    result = get_salary_display(vacancy)


def test_get_salary_display_to_salary():
    """Тест отображения зарплаты только с верхней границей"""
    vacancy = Vacancy(
        title="Developer",
        url="https://example.com",
        salary={"to": 200000, "currency": "RUR"},
        description="Test",
        responsibility="Test",
        experience="Test",
    )
    result = get_salary_display(vacancy)
    assert result == "до 200000 RUR"


def test_get_salary_display_no_salary():
    """Тест отображения отсутствующей зарплаты"""
    vacancy = Vacancy(
        title="Developer",
        url="https://example.com",
        salary=None,
        description="Test",
        responsibility="Test",
        experience="Test",
    )
    result = get_salary_display(vacancy)
    assert result == "Не указана"


def test_get_salary_display_empty_salary():
    """Тест отображения пустой зарплаты"""
    vacancy = Vacancy(
        title="Developer",
        url="https://example.com",
        salary={},
        description="Test",
        responsibility="Test",
        experience="Test",
    )
    result = get_salary_display(vacancy)
    assert result == "Не указана"


def test_get_salary_display_only_currency():
    """Тест отображения зарплаты только с валютой"""
    vacancy = Vacancy(
        title="Developer",
        url="https://example.com",
        salary={"currency": "EUR"},
        description="Test",
        responsibility="Test",
        experience="Test",
    )
    result = get_salary_display(vacancy)
    assert result == "Не указана"


def test_get_salary_display_default_currency():
    """Тест отображения зарплаты с валютой по умолчанию"""
    vacancy = Vacancy(
        title="Developer",
        url="https://example.com",
        salary={"from": 50000},
        description="Test",
        responsibility="Test",
        experience="Test",
    )
    result = get_salary_display(vacancy)
    assert result == "от 50000 RUR"


def test_display_vacancies_empty_list():
    """Тест отображения пустого списка вакансий"""
    # Этот тест проверит, что функция не падает на пустом списке
    display_vacancies([], "Тестовые вакансии")


def test_display_vacancies_with_data(capsys):
    """Тест отображения списка вакансий с данными"""
    vacancies = [
        Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Backend development",
            responsibility="Write code",
            experience="1-3 years",
        )
    ]

    display_vacancies(vacancies, "Найденные вакансии")

    captured = capsys.readouterr()
    output = captured.out

    assert "Найденные вакансии (1 шт.)" in output
    assert "Python Developer" in output
    assert "https://hh.ru/vacancy/123" in output
    assert "100000 - 150000 RUR" in output
    assert "Backend development" in output
    assert "Write code" in output
    assert "1-3 years" in output


def test_display_vacancies_default_title(capsys):
    """Тест отображения с заголовком по умолчанию"""
    vacancies = [
        Vacancy(
            title="Test",
            url="https://test.com",
            salary=None,
            description="Test",
            responsibility="Test",
            experience="Test",
        )
    ]

    display_vacancies(vacancies)  # Без указания title

    captured = capsys.readouterr()
    output = captured.out

    assert "Вакансии (1 шт.)" in output
