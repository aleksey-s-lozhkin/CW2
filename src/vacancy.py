class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, title: str, url: str, salary: dict, description: str, responsibility: str, experience: str):
        self.title = title
        self.url = url
        self.salary = salary
        self.description = description
        self.responsibility = responsibility
        self.experience = experience

    def _get_comparison_salary(self) -> int:
        """Возвращает зарплату для сравнения (среднее значение, если указан диапазон)"""

        if not self.salary:
            return 0

        salary_from = self.salary.get('from')
        salary_to = self.salary.get('to')

        # Если нет данных о зарплате
        if salary_from is None and salary_to is None:
            return 0

        # Если указаны обе границы - берем среднее
        if salary_from is not None and salary_to is not None:
            return (salary_from + salary_to) // 2
        # Если указана только нижняя граница
        elif salary_from is not None:
            return salary_from
        # Если указана только верхняя граница
        elif salary_to is not None:
            return salary_to
        else:
            return 0

    def __eq__(self, other) -> bool:
        """Проверка на равенство по зарплате"""

        if not isinstance(other, Vacancy):
            return False
        return self._get_comparison_salary() == other._get_comparison_salary()

    def __lt__(self, other) -> bool:
        """Проверка на меньше по зарплате"""

        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._get_comparison_salary() < other._get_comparison_salary()

    def __le__(self, other) -> bool:
        """Проверка на меньше или равно по зарплате"""

        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._get_comparison_salary() <= other._get_comparison_salary()

    def __gt__(self, other) -> bool:
        """Проверка на больше по зарплате"""

        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._get_comparison_salary() > other._get_comparison_salary()

    def __ge__(self, other) -> bool:
        """Проверка на больше или равно по зарплате"""

        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._get_comparison_salary() >= other._get_comparison_salary()

    def __str__(self) -> str:
        """Строковое представление вакансии"""

        return (
            f"Вакансия: {self.title}\n"
            f"Ссылка: {self.url}\n"
            f"Зарплата: {self.get_salary_display()}\n"
            f"Описание: {self.description}\n"
            f"Обязанности: {self.responsibility}\n"
            f"Требуемый опыт: {self.experience}"
        )

    def __repr__(self) -> str:
        """Представление для отладки"""

        return (
            f"Vacancy(title={self.title!r}, url={self.url!r}, "
            f"salary={self.salary!r}, description={self.description!r}, "
            f"responsibility={self.responsibility!r}, experience={self.experience!r})"
        )

    def to_dict(self) -> dict:
        """Преобразует вакансию в словарь"""

        return {
            'title': self.title,
            'url': self.url,
            'salary': self.salary,
            'description': self.description,
            'responsibility': self.responsibility,
            'experience': self.experience,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создает объект Vacancy из словаря"""

        return cls(
            title=data.get('title', ''),
            url=data.get('url', ''),
            salary=data.get('salary', {}),
            description=data.get('description', ''),
            responsibility=data.get('responsibility', ''),
            experience=data.get('experience', ''),
        )
