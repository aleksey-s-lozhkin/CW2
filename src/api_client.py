import json
import os
from abc import ABC, abstractmethod
from pprint import pprint
from typing import List, Dict
from pathlib import Path

import requests


class ApiClient(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def _request(self):
        """Метод подключения к API сервиса с вакансиями"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict]:
        """Метод для получения вакансий от сервиса с вакансиями"""
        pass


class HeadHunterAPIClient(ApiClient):
    """Класс для работы с API сервиса вакансий hh.ru"""

    def __init__(self, base_url: str = 'https://api.hh.ru/vacancies'):
        self.__base_url = base_url

    def _request(self):
        """Метод подключения к API сервиса с вакансиями hh.ru"""
        response = requests.get(self.__base_url)
        response.raise_for_status()
        return response



    def get_vacancies(self, keyword: str, area: int = 113, per_page: int = 30) -> List[Dict]:
        """Метод для получения вакансий от сервиса с вакансиями hh.ru"""
        self._request()
        params = {
            "text": keyword,
            "area": area,
            "per_page": per_page
        }

        response = requests.get(self.__base_url, params=params)
        try:
            response.raise_for_status()
            print('Запрос успешно выполнен')
            raw_data = response.json()
            return raw_data.get("items", [])
        except requests.exceptions.HTTPError as err:
            print(f"Ошибка HTTP: {err}")
            raw_data = response.json()
            return raw_data.get("items", [])

    def save_vacancies_to_json(self, keyword: str, filename: str = None, **kwargs) -> bool:
        """Получает вакансии и сразу сохраняет их в JSON файл"""

        # Если имя файла не указано, используем путь по умолчанию
        if filename is None:
            filename = 'data/raw_json.json'
            os.makedirs(os.path.dirname(filename), exist_ok=True)

        try:
            # Получаем вакансии
            vacancies = self.get_vacancies(keyword, **kwargs)

            # Проверяем, что мы получили данные
            if not vacancies:
                print("Не получено данных для сохранения")
                return False

            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w', encoding='utf-8') as raw_json:
                json.dump(vacancies, raw_json, ensure_ascii=False, indent=2)
            print(f"Успешно сохранено {len(vacancies)} вакансий в {filename}")
            return True
        except Exception as err:
            print(f"Ошибка при сохранении вакансий: {err}")
            return False


if __name__ == "__main__":
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPIClient()

    # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = hh_api.get_vacancies("Python")

    # Вывод полученного результата в консоль
    pprint(hh_vacancies)

    # Сохранение в файл по умолчанию (data/raw_data.json)
    hh_api.save_vacancies_to_json("Python", "../data/raw_json.json")
