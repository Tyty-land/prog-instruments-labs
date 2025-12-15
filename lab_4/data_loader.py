import csv
import os
import re

from typing import List
from config import CSV_DLMTR, IMG_EXTNS

class DataLoader:
    """
    A class for uploading images from various sources.
    """

    @staticmethod
    def from_directory(directory: str) -> List[str]:
        """Downloads images from a folder"""
        if not directory:
            return []

        images = os.listdir((directory + "/").replace("//", "/"))
        result = []
        for img in images:
            if any(ext in img.lower() for ext in IMG_EXTNS[:5]):
                result.append(img)
        return result

    @staticmethod
    def from_csv(csv_path: str) -> List[str]:
        """Uploads images from a CSV file"""
        if not csv_path:
            return []

        images = []
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=CSV_DLMTR)
                for row in reader:
                    for cell in row:
                        if cell.strip() and re.search(r"^\w:/", cell.strip()):
                            images.append(cell.strip())
        except Exception as e:
            raise ValueError(f"Ошибка при чтении CSV файла: {str(e)}")

        return images
