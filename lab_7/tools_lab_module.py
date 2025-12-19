import os

from tools_dataframe_module import reader_csv, writer_csv
from typing import List

def data_frame_filter(data_frame: str, height_max: int, width_max: int) -> None:
    """
    A function from the task that filters the data in the DataFrame by
    the width and height of the images. Overwrite the entire file with the DataFrame,
    that is, creates a new DataFrame that will already be filtered
    :param data_frame: The path or name to the DataFrame (.csv)
    :param height_max: Information from Pandas about the maximum height
    :param width_max: Information from Pandas about the maximum width
    :return None:
    """
    data_imgs = reader_csv(data_frame)
    filtered_data = [data_imgs[0]]  # Сохраняем заголовок

    for i in range(1, len(data_imgs)):
        if int(data_imgs[i][2]) <= height_max and int(data_imgs[i][3]) <= width_max:
            filtered_data.append(data_imgs[i])

    writer_csv(filtered_data, data_frame, 0)

def sort_square_images(data_frame: str) -> None:
    """
    The function adds a new column of information about each image - the area of the image.
    At the same time, it sorts from a smaller area to a larger one. The DataFrame is being overwritten
    :param data_frame: The path or name to the DataFrame (.csv)
    :return None:
    """
    data_imgs = reader_csv(data_frame)
    data_imgs[0].append("Square:")
    for i_row in range(1, len(data_imgs)):
        data_imgs[i_row].append(str(int(data_imgs[i_row][2]) * int(data_imgs[i_row][3])))

    # Сортируем данные, начиная со второй строки (первая - заголовок)
    data_imgs[1:] = sorted(data_imgs[1:], key=lambda x: int(x[5]))

    writer_csv(data_imgs, data_frame, 0)

def sort_data(data_imgs: List[list], i_sort_param: int) -> List[list]:
    """
    A function for sorting a two-dimensional array by parameter.
    Taking the second index of the parameter,
    it is fully sorted from the smallest to the largest,
    counting from the beginning of the list
    :param data_imgs: List of image data
    :param i_sort_param: The second index of the list item
    :return data_imgs: List of image data (SORT)
    """
    # Сортируем данные, начиная со второй строки (первая - заголовок)
    data_imgs[1:] = sorted(data_imgs[1:], key=lambda x: int(x[i_sort_param]))
    return data_imgs
