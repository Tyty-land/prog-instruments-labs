import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools_dataframe_module import reader_csv, writer_csv

def test_reader_csv_normal_case():
    """Тест 1: Чтение нормального CSV файла"""
    # Arrange - подготовка данных
    test_content = "Path;Height;Width\nimg1.jpg;100;200\nimg2.jpg;150;300\n"

    # Создаём временный файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        temp_file = f.name

    try:
        # Act - выполняем тестируемую функцию
        result = reader_csv(temp_file)

        # Assert - проверяем результат
        assert len(result) == 3  # Заголовок + 2 строки
        assert result[0] == ["Path", "Height", "Width"]
        assert result[1] == ["img1.jpg", "100", "200"]
        assert result[2] == ["img2.jpg", "150", "300"]
    finally:
        # Cleanup - очистка после теста
        os.unlink(temp_file)

def test_reader_csv_file_not_found():
    """Тест 3: Обработка отсутствующего файла"""
    # Act & Assert - проверяем что выбросится исключение
    with pytest.raises(FileNotFoundError):
        reader_csv("несуществующий_файл_12345.csv")

def test_writer_csv_basic():
    """Тест 4: Базовая запись CSV"""
    # Arrange
    test_data = [
        ["Path", "Height", "Width"],
        ["img1.jpg", "100", "200"],
        ["img2.jpg", "150", "300"]
    ]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        temp_file = f.name

    try:
        # Act
        writer_csv(test_data, temp_file, 0)

        # Assert - проверяем содержимое файла
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.strip().split('\n')

            assert len(lines) == 3
            assert lines[0] == "Path;Height;Width"
            assert lines[1] == "img1.jpg;100;200"
            assert lines[2] == "img2.jpg;150;300"
    finally:
        os.unlink(temp_file)

def test_writer_csv_different_start_index():
    """Тест 5: Запись с разными начальными индексами"""
    # Arrange
    test_data = [
        ["Path", "Height"],
        ["img1.jpg", "100"],
        ["img2.jpg", "200"],
        ["img3.jpg", "300"]
    ]

    test_cases = [
        (0, 4),  # Начать с 0 - запишутся все 4 строки
        (1, 3),  # Начать с 1 - запишутся 3 строки
        (2, 2),  # Начать с 2 - запишутся 2 строки
    ]

    for start_index, expected_lines in test_cases:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            temp_file = f.name

        try:
            # Act
            writer_csv(test_data, temp_file, start_index)

            # Assert
            with open(temp_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                assert len(lines) == expected_lines
        finally:
            os.unlink(temp_file)
