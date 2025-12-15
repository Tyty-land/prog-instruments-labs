import os
from typing import List, Tuple

import cv2
import matplotlib.pyplot as plt
import numpy as np


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
    histogram_data = []
    for i in range(0, 256):
        histogram_data.append(0)
    cnt = 10
    for x in range(0, height - 1):
        if cnt == 10:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Building histogram:\n|" + "#" * int(x / 20) + " " * (int((height - 1 - int(x)) / 20)) + "|")
            cnt -= 10
        else:
            cnt += 1
        for y in range(0, width - 1):
            index_brightness = 0.2126 * img[x][y][0] + 0.7152 * img[x][y][1] + 0.0722 * img[x][y][2]
            histogram_data[round(index_brightness)] += 1
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
    img_r_ch = cv2.imread(path_image)
    img_g_ch = cv2.imread(path_image)
    img_b_ch = cv2.imread(path_image)
    cnt = 10
    for x in range(0, img_r_ch.shape[:-1][0] - 1):
        if cnt == 10:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(
                f"Division into RGB channels:\n|" + "#" * int(x / 20) + " " * (int((img_r_ch.shape[:-1][0] - 1 - int(x))
                                                                                   / 20)) + "|")
            cnt -= 10
        else:
            cnt += 1
        for y in range(0, img_r_ch.shape[:-1][1] - 1):
            img_r_ch[x][y][1] = 0
            img_r_ch[x][y][0] = 0
            img_g_ch[x][y][2] = 0
            img_g_ch[x][y][0] = 0
            img_b_ch[x][y][2] = 0
            img_b_ch[x][y][1] = 0
    if not os.path.exists(path_save):
        os.mkdir(path_save)
    cv2.imwrite(f'{path_save}imageR.jpg', img_r_ch)
    cv2.imwrite(f'{path_save}imageG.jpg', img_g_ch)
    cv2.imwrite(f'{path_save}imageB.jpg', img_b_ch)
    print("[?] - The division into RGB channels is completed!")
