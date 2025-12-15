import sys

import argparse
import cv2
import logging
import logging_config
from pathlib import Path
from typing import Tuple

from path_work_modl import clear_name_image
from path_work_modl import create_absolut_dir
from work_with_images import delimiter_channel
from work_with_images import display_graph
from work_with_images import get_data_imgs

# Получаем настроенный логгер. Имя 'ImageProcessor' соответствует конфигу.
logging_config.setup_logging()
logger = logging.getLogger('ImageProcessor')

def get_p() -> Tuple[str, str]:
    """
    A function that accepts command line parameters, namely:
        -pi = path to the image
        -ps = path to the folder where RGB copies of the image are saved.
    then collects these parameters into a tuple and returns this tuple
    :return res_tuple: a tuple containing all three cmd parameters
    """
    p_cmd = argparse.ArgumentParser()
    p_cmd.add_argument('-pi', '--path_image', type=str, help="path_image")
    p_cmd.add_argument('-ps', '--path_save', type=str, help="path_save", default="")
    args = p_cmd.parse_args()

    # ЛОГИРОВАНИЕ: параметры запуска
    logger.info(f"Запуск программы с параметрами: image={args.path_image}, save_dir={args.path_save}")

    res_tuple = (args.path_image.replace("\\", "/"), args.path_save.replace("\\", "/"))
    return res_tuple


def main() -> None:
    """
    The main function that uses the functionality of all the others
    it also starts all the work of the code
    :return None:
    """
    path_image, path_save = get_p()

    # ЛОГИРОВАНИЕ: начало загрузки
    logger.info(f"Загрузка изображения: {path_image}")

    img = cv2.imread(path_image)

    if img is None:
        # ЛОГИРОВАНИЕ: критическая ошибка
        logger.error(f"Не удалось загрузить изображение: {path_image}")
        print(f"Ошибка: файл {path_image} не найден или поврежден")
        return
    # ЛОГИРОВАНИЕ: успешная загрузка
    logger.info(f"Изображение загружено. Размер: {img.shape[1]}x{img.shape[0]}, каналы: {img.shape[2]}")
    # ЛОГИРОВАНИЕ: начало обработки
    logger.debug("Начало построения гистограммы...")

    res = get_data_imgs(img)

    # ЛОГИРОВАНИЕ: результат гистограммы
    total_pixels = res[1] * res[2]
    logger.info(f"Гистограмма построена. Всего пикселей: {total_pixels}")

    display_graph(res[0], res[1], res[2], clear_name_image(path_image))

    # ЛОГИРОВАНИЕ: разделение каналов
    abs_save_path = create_absolut_dir(path_save)
    logger.info(f"Начало разделения на RGB каналы. Сохранение в: {abs_save_path}")

    delimiter_channel(path_image, create_absolut_dir(path_save))

    # ЛОГИРОВАНИЕ: завершение
    logger.info("Обработка изображения завершена успешно")


if __name__ == '__main__':
    main()
