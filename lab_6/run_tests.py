import os
import sys
import subprocess


def print_header(text):
    """Печатает красивый заголовок"""
    print(f" {text}")


def run_all_tests():
    """Запускает все тесты"""
    print_header("ЗАПУСК ВСЕХ UNIT-ТЕСТОВ")

    # Путь к папке с тестами
    test_dir = os.path.join(os.path.dirname(__file__), "unit_tests")

    # Команда для запуска pytest
    cmd = [
        sys.executable,  # Используем текущий интерпретатор Python
        "-m", "pytest",
        test_dir,
        "-v",  # Подробный вывод
        "--tb=short",  # Короткий traceback при ошибках
    ]

    print(f"Папка с тестами: {test_dir}")
    print(f"Команда: {' '.join(cmd)}")
    print("Результаты тестов:")

    # Запускаем тесты
    result = subprocess.run(cmd)

    # Возвращаем код завершения
    return result.returncode


def run_specific_test_file(filename):
    """Запускает тесты из конкретного файла"""
    print_header(f"ЗАПУСК ТЕСТОВ ИЗ {filename}")

    test_file = os.path.join(os.path.dirname(__file__), "unit_tests", filename)

    if not os.path.exists(test_file):
        print(f"Ошибка: файл {test_file} не найден!")
        return 1

    cmd = [
        sys.executable,
        "-m", "pytest",
        test_file,
        "-v",
        "--tb=short",
    ]

    print(f"Тестовый файл: {test_file}")
    print(f"Команда: {' '.join(cmd)}")
    print()

    result = subprocess.run(cmd)
    return result.returncode


def run_specific_test_function(test_file, test_name):
    """Запускает конкретную тестовую функцию"""
    print_header(f"ЗАПУСК ТЕСТА {test_name} ИЗ {test_file}")

    test_path = os.path.join(os.path.dirname(__file__), "unit_tests", test_file)

    if not os.path.exists(test_path):
        print(f"Ошибка: файл {test_path} не найден!")
        return 1

    cmd = [
        sys.executable,
        "-m", "pytest",
        f"{test_path}::{test_name}",
        "-v",
        "--tb=short",
    ]

    print(f"Тест: {test_name}")
    print(f"Файл: {test_path}")
    print(f"Команда: {' '.join(cmd)}")
    print()

    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        if sys.argv[1] == "--file" and len(sys.argv) > 2:
            # Запуск конкретного файла: python run_tests.py --file test_dataframe.py
            exit_code = run_specific_test_file(sys.argv[2])
        elif sys.argv[1] == "--test" and len(sys.argv) > 3:
            # Запуск конкретного теста: python run_tests.py --test test_dataframe.py test_reader_csv_normal_case
            exit_code = run_specific_test_function(sys.argv[2], sys.argv[3])
        else:
            print("Использование:")
            print("  python run_tests.py                    # Запустить все тесты")
            print("  python run_tests.py --file filename.py # Запустить тесты из файла")
            print("  python run_tests.py --test file.py function_name # Запустить конкретный тест")
            print("\nПримеры:")
            print("  python run_tests.py --file test_dataframe.py")
            print("  python run_tests.py --test test_dataframe.py test_reader_csv_normal_case")
            exit_code = 1
    else:
        # Запуск всех тестов по умолчанию
        exit_code = run_all_tests()

    # Завершаем с соответствующим кодом
    sys.exit(exit_code)