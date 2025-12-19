"""
Unit tests for tools_lab_module.py - в виде простых функций
"""
import os
import sys
import tempfile
import pytest

from tools_lab_module import sort_square_images, sort_data

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ================== Тесты для sort_data ==================

def test_sort_data_unsorted_input():
    """Тест 4: Сортировка неотсортированных данных"""
    # Arrange
    test_data = [
        ["Path", "Height"],
        ["img3.jpg", "300"],
        ["img1.jpg", "100"],
        ["img2.jpg", "200"]
    ]

    # Act
    result = sort_data(test_data, 1)  # Сортируем по колонке Height (индекс 1)

    # Assert
    assert result[1][1] == "100"  # Первое значение после сортировки
    assert result[2][1] == "200"  # Второе значение
    assert result[3][1] == "300"  # Третье значение


def test_sort_data_already_sorted():
    """Тест 5: Сортировка уже отсортированных данных"""
    # Arrange
    test_data = [
        ["Path", "Width"],
        ["img1.jpg", "100"],
        ["img2.jpg", "200"],
        ["img3.jpg", "300"]
    ]

    # Act
    result = sort_data(test_data, 1)

    # Assert - порядок не должен измениться
    assert result == test_data


def test_sort_data_empty_list():
    """Тест 6: Сортировка пустого списка"""
    # Act
    result = sort_data([], 0)

    # Assert
    assert result == []
