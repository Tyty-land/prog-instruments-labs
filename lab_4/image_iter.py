from data_loader import DataLoader

class KeywordPhotoIter:
    """
    An iterator for navigating through a list of images.
    Retains the original interface and functionality.
    """

    def __init__(self, csv_or_dir_path: str, start_or_end: bool):
        """
        Initializes the iterator. Uses DataLoader to upload images.

        :param csv_or_dir_path: Path to the CSV file or folder with images
        :param start_or_end: True - start from the end, False - start from the beginning
        """
        self.data_keyword = DataLoader.load_images(csv_or_dir_path)

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
        if 0 <= self.index < self.limit:
            return self.data_keyword[self.index]
        return ""
