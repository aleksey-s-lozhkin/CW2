from typing import List

from src.api_client import HeadHunterAPIClient
from src.vacancy import Vacancy
from src.vacancy_storage import JSONVacancyStorage


class VacancyManager:
    """Менеджер для работы с вакансиями"""

    def __init__(self, storage_filename: str = "data/vacancies.json"):
        self.api_client = HeadHunterAPIClient()
        self.storage = JSONVacancyStorage(storage_filename)
        self.current_vacancies: List[Vacancy] = []

    def search_vacancies(self, keyword: str, per_page: int = 50) -> list:
        """Поиск вакансий по ключевому слову через API."""
        print(f"Поиск вакансий: '{keyword}'")
        self.current_vacancies = self.api_client.get_vacancies_as_objects(keyword=keyword, per_page=per_page)
        return self.current_vacancies

    def save_current_vacancies(self) -> int:
        """Сохранить текущие найденные вакансии в хранилище."""
        if not self.current_vacancies:
            return 0
        for vacancy in self.current_vacancies:
            self.storage.add_vacancy(vacancy)
        return len(self.current_vacancies)

    def get_top_n_by_salary(self, n: int) -> list:
        """Получить топ-N вакансий по зарплате из хранилища."""
        all_vacancies = self.storage.get_vacancies()
        vacancies_with_salary = [v for v in all_vacancies if v.salary]
        if not vacancies_with_salary:
            print("В хранилище нет вакансий с указанной зарплатой")
            return []
        sorted_vacancies = sorted(vacancies_with_salary, reverse=True)
        print(f"Всего вакансий с зарплатой: {len(vacancies_with_salary)}")
        return sorted_vacancies[:n]

    def search_by_keyword(self, keyword: str) -> list:
        """Поиск вакансий по ключевому слову в сохраненных данных."""
        criteria = {'keyword': keyword}
        return self.storage.get_vacancies(criteria)

    def get_all_saved_vacancies(self) -> list:
        """Получить все вакансии из хранилища."""
        return self.storage.get_vacancies()

    def delete_vacancies(self, criteria: dict) -> int:
        """Удалить вакансии по критериям."""
        vacancies_before = len(self.storage.get_vacancies())
        self.storage.del_vacancy(criteria)
        vacancies_after = len(self.storage.get_vacancies())
        return vacancies_before - vacancies_after

    def clear_storage(self) -> None:
        """Очистить хранилище."""
        self.storage.clear_all()
