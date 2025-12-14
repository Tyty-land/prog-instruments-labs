import os

from tools_dataframe_module import ReaderCsv, writer_csv
from typing import List


def data_frame_filter(data_frame: str, height_max: int,
                      width_max: int) -> None:
    """
    A function from the task that filters the data in the DataFrame by
    the width and height of the images. Overwrite the entire
    file with the DataFrame, that is, creates a new
    DataFrame that will already be filtered
    :param data_frame: The path or name to the DataFrame (.csv)
    :param height_max: Information from Pandas about the maximum height
    :param width_max: Information from Pandas about the maximum width
    :return None:
    """
    data_imgs = ReaderCsv(data_frame)
    os.remove(data_frame)
    i = 1
    end = len(data_imgs)
    while i < end:
        if int(data_imgs[i][2]) > height_max or int(data_imgs[i][3]) > \
                width_max:
            data_imgs.pop(i)
            end -= 1
        else:
            i += 1
    writer_csv(data_imgs, data_frame, 0)


def sort_square_images(data_frame: str) -> None:
    """
    The function adds a new column of information
    about each image - the area of the image.
    At the same time, it sorts from a smaller area to a larger one.
    The DataFrame is being overwritten
    :param data_frame: The path or name to the DataFrame (.csv)
    :return None:
    """
    data_imgs = ReaderCsv(data_frame)
    os.remove(data_frame)
    data_imgs[0].append("Square:")
    for i_row in range(1, len(data_imgs)):
        data_imgs[i_row].append(str(int(data_imgs[i_row][2]) *
                                    int(data_imgs[i_row][3])))
    writer_csv(sort_data(data_imgs, 5), data_frame, 0)


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
    x = 2
    while x < len(data_imgs):
        if int(data_imgs[x][i_sort_param]) < \
                int(data_imgs[x - 1][i_sort_param]):
            y = x
            while int(data_imgs[y][i_sort_param]) < \
                    int(data_imgs[y - 1][i_sort_param]):
                tmp = data_imgs[y]
                data_imgs[y] = data_imgs[y - 1]
                data_imgs[y - 1] = tmp
                y -= 1
                if y == 1:
                    x = 2
                    break
                x = y
        x += 1
    return data_imgs
