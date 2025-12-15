import os
from typing import List, Tuple

import cv2
import logging
import matplotlib.pyplot as plt
import numpy as np

# Получаем логгер для этого модуля
logger = logging.getLogger('ImageProcessor.ImageProcessor')

def get_data_imgs(img: List[list]) -> Tuple[list, int, int]:
    """
    This function extracts data from an image, namely, collects a list of the number of pixels from
    a certain brightness according to the formula, that is, creates a histogram, and receives size data
    this picture. After that, it enters all the received data into the tuple and returns it.
    This function also displays a scale of the data extraction progress:
        Building histogram:
        |###############################                      |
    It is needed to understand how long it will take to extract data
    :param img: an array with RGB data of the values of each pixel obtained using OpenCV
    :return res_tuple: tuple of image data(histogram, width, height)
    """
    height, width = img.shape[:-1]
    histogram_data = [0] * 256
    total_pixels = height * width

    # ЛОГИРОВАНИЕ: начало вычислений
    logger.debug(f"Начало вычисления гистограммы для изображения {width}x{height} ({total_pixels} пикселей)")

    processed_pixels = 0
    for x in range(0, height - 1):
        # Вместо os.system('cls') для прогресса - логируем каждые 5%
        if x % max(1, height // 20) == 0:
            progress = (x / height) * 100
            logger.debug(f"Прогресс гистограммы: {progress:.1f}% ({x}/{height} строк)")

        for y in range(0, width - 1):
            # ЛОГИРОВАНИЕ: детальное (только при необходимости)
            if logger.isEnabledFor(logging.DEBUG) and processed_pixels < 10:
                r, g, b = img[x][y][0], img[x][y][1], img[x][y][2]
                brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
                logger.debug(f"Пиксель [{x},{y}]: R={r}, G={g}, B={b}, яркость={brightness:.1f}")

            index_brightness = 0.2126 * img[x][y][0] + 0.7152 * img[x][y][1] + 0.0722 * img[x][y][2]
            histogram_data[round(index_brightness)] += 1
            processed_pixels += 1

    # ЛОГИРОВАНИЕ: статистика гистограммы
    max_brightness_count = max(histogram_data)
    max_brightness_idx = histogram_data.index(max_brightness_count)
    logger.info(f"Гистограмма готова. Максимум: {max_brightness_count} пикселей с яркостью {max_brightness_idx}")

    res_tuple = (histogram_data, width, height)
    return res_tuple


def display_graph(histogram_data: list, width: int, height: int, image_name: str) -> None:
    """
    It is clear from the name that the function builds the corresponding image based on the data obtained from the image
    histogram graph
    :param histogram_data:
    :param width:
    :param height:
    :param image_name:
    :return None:
    """
    plt.figure(figsize=(10, 5))
    x = np.linspace(0, len(histogram_data) - 1, len(histogram_data))
    y = []
    for i in x:
        y.append(histogram_data[int(i)])
    plt.fill_between(x, y, label='histogram', color='black')
    plt.title(f"Гистограмма {image_name} (Size: {width}x{height})")
    plt.xlabel('Яркость')
    plt.ylabel('Кол-во пикселей')
    plt.axhline(0, color='black', linewidth=0.5, ls='--')  # x
    plt.axvline(0, color='black', linewidth=0.5, ls='--')  # y
    plt.show()


def delimiter_channel(path_image: str, path_save: str) -> None:
    """
    The function divides the image into three RGB channels
    and saves it to a specific folder in a specific path
    This function also displays the progress scale of the division by channels:
        Division into RGB channels:
        |###############################                      |
    It is needed to understand how long the separation will take.
    :param path_image: path to the image
    :param path_save: path to the save folder
    :return None:
    """
    # ЛОГИРОВАНИЕ: начало разделения
    logger.info(f"Начало разделения изображения на RGB каналы: {path_image}")

    img_r_ch = cv2.imread(path_image)
    if img_r_ch is None:
        logger.error(f"Не удалось загрузить изображение для разделения: {path_image}")
        return

    height, width = img_r_ch.shape[:-1]
    logger.debug(f"Размер изображения для разделения: {width}x{height}")

    img_g_ch = img_r_ch.copy()
    img_b_ch = img_r_ch.copy()

    # ЛОГИРОВАНИЕ: прогресс обработки
    total_pixels = height * width
    processed = 0
    for x in range(0, img_r_ch.shape[:-1][0] - 1):
        # Логируем прогресс каждые 10%
        if x % max(1, height // 10) == 0:
            progress = (x / height) * 100
            logger.debug(f"Прогресс разделения каналов: {progress:.1f}%")

        for y in range(0, img_r_ch.shape[:-1][1] - 1):
            img_r_ch[x][y][1] = 0
            img_r_ch[x][y][0] = 0
            img_g_ch[x][y][2] = 0
            img_g_ch[x][y][0] = 0
            img_b_ch[x][y][2] = 0
            img_b_ch[x][y][1] = 0
            processed += 1

    # ЛОГИРОВАНИЕ: создание папки
    if not os.path.exists(path_save):
        logger.warning(f"Папка для сохранения не существует, создаю: {path_save}")
        os.mkdir(path_save)

    # ЛОГИРОВАНИЕ: сохранение файлов
    try:
        cv2.imwrite(f'{path_save}imageR.jpg', img_r_ch)
        logger.debug(f"Сохранён красный канал: {path_save}imageR.jpg")

        cv2.imwrite(f'{path_save}imageG.jpg', img_g_ch)
        logger.debug(f"Сохранён зелёный канал: {path_save}imageG.jpg")

        cv2.imwrite(f'{path_save}imageB.jpg', img_b_ch)
        logger.debug(f"Сохранён синий канал: {path_save}imageB.jpg")

        logger.info(f"Разделение на RGB каналы завершено. Файлы сохранены в {path_save}")

    except Exception as e:
        logger.error(f"Ошибка при сохранении RGB каналов: {e}", exc_info=True)
