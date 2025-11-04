import os
import json

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.vacancy import Vacancy

class VacancyStorage(ABC):
    """ Абстрактный класс для работы с файлом вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """ Метод для добавления вакансии в файл"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any]) ->List[Vacancy]:
        """ Метод для получения вакансий из файла по критериям"""
        pass

    @abstractmethod
    def del_vacancy(self, criteria: Dict[str, Any]) ->None:
        """ Метод для удаления вакансии из файла по критериям"""
        pass

    @abstractmethod
    def clear_all(self) -> None:
        """Очистка всего хранилища"""
        pass

    def connect(self) -> None:
        """Подключение к хранилищу (заглушка)"""
        pass

    def disconnect(self) -> None:
        """Отключение от хранилища (заглушка)"""
        pass

    def is_connected(self) -> bool:
        """Проверка подключения (заглушка)"""
        return True


class JSONVacancyStorage(VacancyStorage):
    """Класс для работы с вакансиями в JSON-файле"""

    def __init__(self, filename: str = "vacancies.json"):
        self.filename = filename
        self._file_exists()

    def _file_exists(self) -> None:
        """Создает файл, если он не существует"""

        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as json_file:
                json.dump([], json_file, ensure_ascii=False, indent=2)

    def _get_vacancies(self) -> List[Dict[str, Any]]:
        """Чтение вакансий из файла"""

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Запись вакансий в файл"""

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в JSON-файл"""

        vacancies_data = self._get_vacancies()
        vacancy_dict = vacancy.to_dict()

        for existing_vacancy in vacancies_data:
            if existing_vacancy.get('url') == vacancy.url:
                return

        vacancies_data.append(vacancy_dict)
        self._write_vacancies(vacancies_data)

    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Vacancy]:
        """Получение вакансий по критериям из JSON-файла"""

        if criteria is None:
            criteria = {}

        vacancies_data = self._get_vacancies()
        filtered_vacancies = []

        for vacancy_dict in vacancies_data:
            matches = True

            for key, value in criteria.items():
                if key == 'salary_min':

                    salary = vacancy_dict.get('salary', {})
                    salary_from = salary.get('from', 0)
                    salary_to = salary.get('to', 0)
                    actual_salary = max(salary_from, salary_to)
                    if actual_salary < value:
                        matches = False
                        break
                elif key == 'keyword':

                    keyword = value.lower()
                    title = vacancy_dict.get('title', '').lower()
                    description = vacancy_dict.get('description', '').lower()
                    if keyword not in title and keyword not in description:
                        matches = False
                        break
                else:

                    if vacancy_dict.get(key) != value:
                        matches = False
                        break

            if matches:
                filtered_vacancies.append(Vacancy.from_dict(vacancy_dict))

        return filtered_vacancies

    def del_vacancy(self, criteria: Dict[str, Any]) -> None:
        """Удаление вакансий по критериям из JSON-файла"""

        vacancies_data = self._get_vacancies()

        filtered_vacancies = []

        for vacancy_dict in vacancies_data:
            matches = True

            for key, value in criteria.items():
                if vacancy_dict.get(key) != value:
                    matches = False
                    break

            if not matches:
                filtered_vacancies.append(vacancy_dict)

        self._write_vacancies(filtered_vacancies)

    def clear_all(self) -> None:
        """Очистка всего JSON-файла"""
        self._write_vacancies([])

    def connect(self) -> None:
        """Подключение к хранилищу (заглушка)"""
        pass

    def disconnect(self) -> None:
        """Отключение от хранилища (заглушка)"""
        pass

    def is_connected(self) -> bool:
        """Проверка подключения (заглушка)"""
        return True