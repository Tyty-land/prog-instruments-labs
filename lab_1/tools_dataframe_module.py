import csv
import os
import pandas as pd
from typing import List
def ReaderCsv(data_frame: str) -> List[list]:
    """
    The function is designed to read data from a DataFrame into a new list line by line,  applying the necessary data transformations for the program
    :param data_frame: The path or name to the DataFrame (.csv)
    :return data_list: List of image data
    """
    with open(data_frame, 'r', encoding='utf-8') as data:
        data_list= data.read().split("\n")
        for i in range(len(data_list)):
            if data_list[i] =="":
                data_list.pop(i)
            else:
                data_list[i] = data_list[i].split(
                    ";")
    return data_list
def writer_csv(DataImgs: List[list], data_frame: str, index_start: int) -> None:
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
    if index_start<len(DataImgs):
        with open(data_frame,
                  mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            for i_row in range(index_start,
                               len(DataImgs)):
                writer.writerow(
                    DataImgs[i_row])
def demonstration_of_results(data_frame: str)-> None:
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
    DataImgs = reader_csv(data_frame)
    writer_csv(DataImgs, 'data_frame_pandas.csv', 1)
    df =pd.read_csv(
        'data_frame_pandas.csv', delimiter=';', names=DataImgs[0])
    statistical_list = [stat_key("Height:", df), stat_key("Width:", df), stat_key("Color_depth:", df)]
    os.remove('data_frame_pandas.csv')
    return statistical_list




def stat_key(column_name: str, df: pd)->List[int]:
    """
    The function is needed to generate statistical data on the corresponding column
    :param column_name: The name of the column from which you want to calculate statistical data
    :param df: DataFrame formed by Pandas
    :return statistical_list_piece: column statistics (piece)
    """
    statistical_list_piece = [df[column_name].count(),
                         df[column_name].sum(),
                         df[column_name].mean(),
                         df[column_name].median(),
                         df[column_name].min(),
                         df[column_name].max(),
                         df[column_name].mode(),
                         df[column_name].abs(),
                         df[column_name].prod(),
                         df[column_name].std(),
                         df[column_name].var(),
                         df[column_name].sem(),
                         df[column_name].skew(),
                         df[column_name].kurt(),
                         df[column_name].quantile(),
                         df[column_name].cumsum(),
                         df[column_name].cumprod(),
                         df[column_name].cummax(),
                         df[column_name].cummin()]
    return statistical_list_piece
