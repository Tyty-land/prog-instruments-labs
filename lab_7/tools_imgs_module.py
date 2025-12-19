import cv2
import os
import re
import math

import matplotlib.pyplot as plt
from tools_dataframe_module import reader_csv
from typing import List


CONST_activ_dir = os.getcwd().replace("\\", "/").lower() + "/"


def get_data_imgs(absolut_save_dir: str) -> List[list]:
    """
    The function prepares information about the pictures contained in the corresponding folder,
    according to the task. Creates a list of strings and returns it
    :param absolut_save_dir: The path to the folder with pictures
    :return data_imgs: List of data about images
    """
    images = os.listdir(absolut_save_dir)
    data_imgs = [["Absolute Path:", "Relative path:", "Height:", "Width:", "Color_depth:"]]
    for image in images:
        relative_save_dir = absolut_save_dir
        if CONST_activ_dir in relative_save_dir:
            relative_save_dir = relative_save_dir.replace(CONST_activ_dir, "/")
        img = cv2.imread(f"{absolut_save_dir}/{image}")
        height, width = img.shape[:-1]
        depth_color = math.ceil((os.path.getsize(f"{absolut_save_dir}/{image}")*8)/(height*width))
        row = [f"{absolut_save_dir}/{image}", f"{relative_save_dir}/{image}", height, width, depth_color]
        data_imgs.append(row)
    return data_imgs


def create_absolut_dir(save_dir: str) -> str:
    """
    The function checks whether a folder with photos is being created in the new directory of the current directory
    or this folder is located on another disk or in another branch that is not adjacent to this one.
    If the folder should still be located in this directory from where the program is launched, then
    the path to the current directory where the program was launched is appended
    to the path
    :param save_dir: the path to the photo saving folder obtained by the command line parameter
    :return absolut_dir: The absolute path to the corresponding file or folder
    """
    if re.search(r"\w:/+", save_dir) is None and re.search(r"\w:\\+", save_dir) is None:
        save_dir = CONST_activ_dir + save_dir
    if re.search(r"\.\w+", save_dir) is None:
        absolut_dir = (save_dir + "/").replace("\\", "/").replace("//", "/")
        return absolut_dir
    else:
        absolut_dir = save_dir.replace("\\", "/").replace("//", "/")
        return absolut_dir


def display_histogram(data_frame: str, i_sort_param: int) -> None:
    """
    The function is needed to display a histogram for a specific parameter.
    The parameter is selected the same as when sorting (sort_data)
    :param data_frame: The path or name to the DataFrame (.csv)
    :param i_sort_param: The second index of the list item
    :return None:
    """
    data_imgs = reader_csv(data_frame)
    x = []
    for i in range(1, len(data_imgs)):
        x.append(int(data_imgs[i][i_sort_param]))
    plt.figure(figsize=(10, 5))
    plt.hist(x)
    plt.title(f"Гистограмма площадей картинок")
    plt.xlabel('Площадь')
    plt.ylabel('Кол-во картинок')
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.show()

