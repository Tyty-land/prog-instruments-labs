import os
import sys
import math
from unittest.mock import Mock, patch
import pytest

from tools_imgs_module import create_absolut_dir, get_data_imgs

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ================== Тесты для create_absolut_dir ==================

def test_create_absolut_dir_relative_path():
    """Тест 1: Конвертация относительного пути в абсолютный"""
    # Arrange - настраиваем моки
    with patch('os.getcwd') as mock_getcwd:
        mock_getcwd.return_value = 'C:\\Projects\\MyProject'

        # Мокаем константу из модуля
        with patch('tools_imgs_module.CONST_activ_dir', 'C:/Projects/MyProject/'):
            # Act
            result = create_absolut_dir("images\\test")

            # Assert
            # Windows пути нормализуются к виду с прямыми слешами
            assert result == "C:/Projects/MyProject/images/test/"

def test_create_absolut_dir_absolute_windows_path():
    """Тест 2: Абсолютный путь Windows остается без изменений"""
    # Act
    result = create_absolut_dir("C:\\Users\\Test\\images")

    # Assert
    assert result == "C:/Users/Test/images/"  # Обратные слеши заменяются на прямые

def test_create_absolut_dir_file_path():
    """Тест 4: Путь к файлу (не папке)"""
    with patch('os.getcwd') as mock_getcwd:
        mock_getcwd.return_value = 'C:\\Projects\\MyProject'
        with patch('tools_imgs_module.CONST_activ_dir', 'C:/Projects/MyProject/'):
            # Act
            result = create_absolut_dir("data.csv")

            # Assert - для файла не добавляется слеш в конце
            assert result == "C:/Projects/MyProject/data.csv"

def test_create_absolut_dir_empty_string():
    """Тест 5: Пустая строка"""
    with patch('os.getcwd') as mock_getcwd:
        mock_getcwd.return_value = 'C:\\Projects\\MyProject'
        with patch('tools_imgs_module.CONST_activ_dir', 'C:/Projects/MyProject/'):
            # Act
            result = create_absolut_dir("")

            # Assert
            assert result == "C:/Projects/MyProject/"

# ================== Тесты для get_data_imgs ==================

def test_get_data_imgs_with_images():
    """Тест 6: Получение данных изображений из папки"""
    # Arrange - создаем моки для всех внешних зависимостей
    mock_files = ["img1.jpg", "img2.png"]

    # Создаем мок-объекты для изображений
    mock_img1 = Mock()
    mock_img1.shape = (100, 200, 3)  # высота, ширина, каналы

    mock_img2 = Mock()
    mock_img2.shape = (150, 300, 3)

    with patch('os.listdir') as mock_listdir, \
            patch('cv2.imread') as mock_imread, \
            patch('os.path.getsize') as mock_getsize, \
            patch('tools_imgs_module.CONST_activ_dir', 'C:/Projects/MyProject/'):
        # Настраиваем моки
        mock_listdir.return_value = mock_files
        mock_imread.side_effect = [mock_img1, mock_img2]
        mock_getsize.side_effect = [240000, 1080000]  # размеры файлов в байтах

        # Act
        result = get_data_imgs("C:\\Test\\Images")

        # Assert
        assert len(result) == 3  # Заголовок + 2 изображения

        # Проверяем заголовок
        assert result[0] == ["Absolute Path:", "Relative path:", "Height:", "Width:", "Color_depth:"]

        # Нормализуем пути для сравнения (заменяем обратные слеши на прямые)
        actual_path = result[1][0].replace("\\", "/")
        expected_path = "C:/Test/Images/img1.jpg"
        assert actual_path == expected_path

        # Проверяем размеры
        assert result[1][2] == 100  # Высота
        assert result[1][3] == 200  # Ширина

        # Проверяем расчет глубины цвета
        # (размер в байтах * 8 бит) / (ширина * высота)
        expected_depth = math.ceil((240000 * 8) / (100 * 200))
        assert result[1][4] == expected_depth

        # Проверяем что функции были вызваны правильно
        mock_listdir.assert_called_once_with("C:\\Test\\Images")
        assert mock_imread.call_count == 2


def test_get_data_imgs_empty_directory():
    """Тест 7: Получение данных из пустой папки"""
    with patch('os.listdir') as mock_listdir, \
            patch('tools_imgs_module.CONST_activ_dir', 'C:/Projects/MyProject/'):
        mock_listdir.return_value = []  # Пустая папка

        # Act
        result = get_data_imgs("C:\\Test\\Empty")

        # Assert
        assert len(result) == 1  # Только заголовок
        assert result[0] == ["Absolute Path:", "Relative path:", "Height:", "Width:", "Color_depth:"]
        mock_listdir.assert_called_once_with("C:\\Test\\Empty")
