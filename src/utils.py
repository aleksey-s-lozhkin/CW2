from typing import List

from src.vacancy import Vacancy


def get_salary_display(vacancy: Vacancy) -> str:
    """Форматирование отображения зарплаты"""
    if not vacancy.salary:
        return "Не указана"

    salary = vacancy.salary
    salary_from = salary.get('from')
    salary_to = salary.get('to')
    currency = salary.get('currency', 'RUR')

    if salary_from and salary_to:
        result = f"{salary_from} - {salary_to}"
    elif salary_from:
        result = f"от {salary_from}"
    elif salary_to:
        result = f"до {salary_to}"
    else:
        return "Не указана"

    result += f" {currency}"
    return result


def display_vacancies(vacancies: List[Vacancy], title: str = "Вакансии"):
    """Отображение списка вакансий"""
    if not vacancies:
        print(f"{title} не найдены")
        return

    print(f"\n{title} ({len(vacancies)} шт.):")
    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. {vacancy.title}")
        print(f"   Ссылка: {vacancy.url}")
        print(f"   Зарплата: {get_salary_display(vacancy)}")
        print(f"   Описание: {vacancy.description}")
        print(f"   Обязанности: {vacancy.responsibility}")
        print(f"   Опыт: {vacancy.experience}")
