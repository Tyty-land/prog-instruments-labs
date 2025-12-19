import csv
import os
import pandas as pd

from typing import List

def reader_csv(data_frame: str) -> List[list]:
    """
    The function is designed to read data from a
    DataFrame into a new list line by line,
    applying the necessary data transformations for the program
    :param data_frame: The path or name to the DataFrame (.csv)
    :return data_list: List of image data
    """
    data_list = []
    with open(data_frame, 'r', encoding='utf-8') as data:
        csv_reader = csv.reader(data, delimiter=';')
        for row in csv_reader:
            if row:  # Пропускаем пустые строки
                data_list.append(row)
    return data_list


def writer_csv(data_imgs: List[list], data_frame: str, index_start: int) -> None:
    """
    This function creates a DataFrame of images in the format (.csv)
    according to the appropriate parameters,
    namely the list of image data, the path and name to the future
    DataFrame and the index number in the list of image data
    from which you will need to start entering data
    :param data_imgs: List of image data
    :param data_frame: The path or name to the DataFrame (.csv)
    :param index_start: Starting index
    :return None:
    """
    if index_start < len(data_imgs):
        with open(data_frame, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            for i_row in range(index_start, len(data_imgs)):
                writer.writerow(data_imgs[i_row])

def demonstration_of_results(data_frame: str) -> None:
    """
    This function outputs several DataFrame lines
    :param data_frame: The path or name to the DataFrame (.csv)
    :return None:
    """
    df = pd.read_csv(data_frame, delimiter=';')
    print("\n", df.head(), "\n")


def pandas_statistical_calculation(data_frame: str) -> List[list]:
    """
    Pandas statistics on images from the corresponding DataFrame.
    The data is arranged in a certain order
    :param data_frame: The path or name to the DataFrame (.csv)
    :return statistical_list: List of statistical data
    """
    data_imgs = reader_csv(data_frame)
    writer_csv(data_imgs, 'data_frame_pandas.csv', 1)
    df = pd.read_csv('data_frame_pandas.csv', delimiter=';', names=data_imgs[0])
    statistical_list = [stat_key("Height:", df), stat_key("Width:", df), stat_key("Color_depth:", df)]
    os.remove('data_frame_pandas.csv')
    return statistical_list


def stat_key(column_name: str, df: pd) -> List[int]:
    """
    The function is needed to generate statistical data on the corresponding column
    :param column_name: The name of the column from which you want to calculate statistical data
    :param df: DataFrame formed by Pandas
    :return statistical_list_piece: column statistics (piece)
    """
    col_data = df[column_name]

    # Вот тут
    # Вычисляем только необходимые статистики
    return [
        col_data.count(),
        col_data.sum(),
        col_data.mean(),
        col_data.median(),
        col_data.min(),
        col_data.max(),
        col_data.mode().iloc[0] if not col_data.mode().empty else None,
        col_data.std(),
        col_data.var()
    ]
