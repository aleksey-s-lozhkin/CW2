from src.utils import display_vacancies
from src.vacancy_manager import VacancyManager


def main():
    """Главная функция программы - консольный интерфейс."""
    manager = VacancyManager()

    print("Система управления вакансиями")

    # Основной цикл программы
    while True:
        # Меню выбора действий
        print("\nМеню:")
        print("1. Поиск вакансий на hh.ru")
        print("2. Сохранить найденные вакансии")
        print("3. Топ N вакансий по зарплате")
        print("4. Поиск по ключевому слову")
        print("5. Показать все сохраненные вакансии")
        print("6. Очистить хранилище")
        print("7. Выход")

        choice = input("Выберите действие: ").strip()

        # Поиск вакансий через API
        if choice == '1':
            keyword = input("Поисковый запрос: ").strip()
            if not keyword:
                print("Запрос не может быть пустым")
                continue
            try:
                per_page = int(input("Количество вакансий (по умолчанию 50): ") or "50")
            except ValueError:
                per_page = 50
            vacancies = manager.search_vacancies(keyword, per_page=per_page)
            display_vacancies(vacancies, "Найденные вакансии")

        # Сохранение найденных вакансий
        elif choice == '2':
            if not manager.current_vacancies:
                print("Сначала выполните поиск вакансий")
                continue
            saved_count = manager.save_current_vacancies()
            print(f"Сохранено {saved_count} вакансий")

        # Топ вакансий по зарплате
        elif choice == '3':
            try:
                n = int(input("Количество вакансий для показа: ").strip())
            except ValueError:
                print("Введите число")
                continue
            top_vacancies = manager.get_top_n_by_salary(n)
            display_vacancies(top_vacancies, f"Топ-{n} вакансий по зарплате")

        # Поиск по ключевому слову в сохраненных вакансиях
        elif choice == '4':
            keyword = input("Ключевое слово для поиска: ").strip()
            if not keyword:
                print("Ключевое слово не может быть пустым")
                continue
            vacancies = manager.search_by_keyword(keyword)
            display_vacancies(vacancies, f"Вакансии с ключевым словом '{keyword}'")

        # Показать все сохраненные вакансии
        elif choice == '5':
            vacancies = manager.get_all_saved_vacancies()
            display_vacancies(vacancies, "Все сохраненные вакансии")

        # Очистка хранилища
        elif choice == '6':
            confirm = input("Очистить все хранилище? (y/n): ").lower().strip()
            if confirm == 'y':
                manager.clear_storage()
                print("Хранилище очищено")

        # Выход из программы
        elif choice == '7':
            print("Выход")
            break

        # Обработка неверного выбора
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    """Точка входа в программу."""
    main()
