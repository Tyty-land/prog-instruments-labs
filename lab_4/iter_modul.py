import csv
import os
import re

from config import CSV_DLMTR, IMG_EXTNS

class KeywordPhotoIter:
    """
    This iterator is designed to create a list of names of downloaded files
    works with a file (data.csv) containing absolute and relative paths to files,
    and also with the path to the folder where these files are located
    :param csv_or_dir_path: .csv file or root folder
    """

    def __init__(self, csv_or_dir_path: str, start_or_end: bool):
        self.data_keyword = []
        if IMG_EXTNS[5] in csv_or_dir_path and csv_or_dir_path != "":
            with open(csv_or_dir_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=CSV_DLMTR)
                for row in reader:
                    for i in range(0, len(row)):
                        if re.search(r"^\w:/", row[i]) is not None:
                            self.data_keyword.append(row[i])
        elif csv_or_dir_path != "":
            self.data_keyword = os.listdir((csv_or_dir_path + "/").replace("//", "/"))
            end = len(self.data_keyword)
            i = 0
            while i < end:
                if IMG_EXTNS[0] not in self.data_keyword[i] and IMG_EXTNS[2] not in self.data_keyword[i]:
                    self.data_keyword.pop(i)
                    end -= 1
                else:
                    i += 1
        if start_or_end:
            self.index = len(self.data_keyword) - 1
        else:
            self.index = 0
        self.limit = len(self.data_keyword)

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index < self.limit:
            return self.data_keyword[self.index]
        else:
            raise StopIteration

    def back(self):
        self.index -= 1
        if self.index >= 0:
            return self.data_keyword[self.index]
        else:
            raise StopIteration

    def get_current_size(self):
        return self.limit

    def get_current_index(self):
        return self.index

    def get_current_elem(self) -> str:
        return self.data_keyword[self.index]
