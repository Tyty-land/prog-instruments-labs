import csv
import os
import re

from typing import List
from config import CSV_DLMTR, IMG_EXTNS

class DataLoader:
    """
    A class for uploading images from various sources
    (folder or CSV file). Retains the original loading logic.
    """

    @staticmethod
    def load_images(source: str) -> List[str]:
        """
        Loads a list of image paths/names from the source.
        Retains the original logic:
        - For CSV: searches for strings similar to absolute paths
        - For folder: filters only .jpg and .png files

        :param source: Folder path or CSV
        :return: List of images
        """
        data_keyword = []

        if not source:
            return data_keyword

        if IMG_EXTNS[5] in source and source != "":
            # Оригинальная логика загрузки из CSV
            with open(source, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=CSV_DLMTR)
                for row in reader:
                    for i in range(0, len(row)):
                        if re.search(r"^\w:/", row[i]) is not None:
                            data_keyword.append(row[i])
        elif source != "":
            # Оригинальная логика загрузки из папки
            data_keyword = os.listdir((source + "/").replace("//", "/"))
            end = len(data_keyword)
            i = 0
            while i < end:
                if (IMG_EXTNS[0] not in data_keyword[i] and
                        IMG_EXTNS[2] not in data_keyword[i]):
                    data_keyword.pop(i)
                    end -= 1
                else:
                    i += 1

        return data_keyword
