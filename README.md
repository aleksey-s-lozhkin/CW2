### Поиск вакансий

Учебный проект на платформе SkyPro.

### Установка

#### Предварительные требования

- Python 3.8+
- Poetry (менеджер зависимостей)

### Установка Poetry

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Linux/MacOS
curl -sSL https://install.python-poetry.org | python3 -
```

### Установка проекта

1. Клонируйте репозиторий:
```bash
git clone <https://github.com/aleksey-s-lozhkin/CW2/tree/develop>
cd CW2
```

2. Установите зависимости через Poetry:
```bash
poetry install
```

3. Активируйте виртуальное окружение:
```bash
poetry shell
```

### Запуск

```bash
# Запуск демонстрации всех функций
poetry run python main.py

# Или с активированным окружением:
python main.py
```

После запуска отобразятся демонстрационные данные.

### Функциональность

#### Абстрактный класс ApiClient (`src/api_client`)
- **`class ApiClient`** - Абстрактный класс для работы с API сервиса с вакансиями

#### Абстрактный класс VacancyStorage (`src/vacancy_storage`)
- **`class VacancyStorage`** - Абстрактный класс для работы с файлом вакансий

#### Класс HeadHunterAPIClient (`src/api_client`)
- **`class HeadHunterAPIClient`** - Класс для работы с API сервиса вакансий hh.ru

#### Класс JSONVacancyStorage (`src/vacancy_storage`)
- **`class JSONVacancyStorage`** - Класс для работы с вакансиями в JSON-файле.

#### Класс Vacancy (`src/vacancy`)
- **`class Vacancy`** - Класс для работы с вакансиями.

#### Класс VacancyManager (`src/vacancy_manager`) 
- **`class VacancyManager`** - Менеджер для работы с вакансиями.

#### Утилиты (`src/utils`)
- **`get_salary_display`** - Форматирование отображения зарплаты
- **`display_vacancies`** - Отображение списка вакансий

### Структура проекта

```
coursework_1/
├── src/
│   ├── api_client/
│   ├── vacancy/
│   ├── vacancy_manager/
│   ├── vacancy_storage/
│   └── utils/ 
├── data/
│   ├── raw_json.json
│   └── vacancies.json
├── tests/  
├── main.py 
├── pyproject.toml
└── README.md
```

### Разработка

#### Добавление новых зависимостей
```bash
# Добавление production зависимости
poetry add package-name

# Добавление development зависимости
poetry add --group dev package-name
```

#### Запуск тестов
```bash
poetry run pytest
```

#### Форматирование кода
```bash
poetry run black .
poetry run isort .
```

### Демонстрация

Проект включает демонстрационный скрипт `main.py`

### Автор
aleksey.s.lozhkin@gmail.com

### Лицензия
Этот проект распространяется под лицензией MIT.