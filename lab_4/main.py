import sys

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QFileDialog, QComboBox
from PyQt5 import QtCore

from iter_modul import KeywordPhotoIter


class MainWindow(QMainWindow):
    """
    This class creates the main application window,
     in the interior of the class all methods and fields are designed to configure and display the program interface
    """
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application")
        self.x = 720
        self.y = 500
        self.resize(self.x, self.y)
        self.resized.connect(self.resize_widgets)
        self.dir_or_csv = ""
        self.current_image = ""
        self.Iter_imgs = KeywordPhotoIter(self.dir_or_csv, 0)
        # Menu
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(['', '  path', '  .csv'])
        self.combo_box.setGeometry(int(self.frameGeometry().width() / 2) - (int(self.frameGeometry().width() / self.x) *
                                                                            170), int(self.frameGeometry().height() / 2)
                                   - (int(self.frameGeometry().height() / self.y) * 240),
                                   (int(self.frameGeometry().width() / self.x) * 400), 20)
        self.combo_box.currentIndexChanged.connect(self.select_dir)
        self.combo_box.currentTextChanged.connect(self.create_list_images)
        self.right_button = QPushButton("-->", self)
        self.right_button.clicked.connect(self.button_reg)
        self.right_button.setGeometry(self.frameGeometry().width() - (round(self.frameGeometry().width() / self.x) * 100
                                                                      ), self.frameGeometry().height() -
                                      (round(self.frameGeometry().height() / self.y) *
                                       (70 + round(self.y / self.frameGeometry().height()) * 30))
                                      , (round(self.frameGeometry().width() / self.x) * 100),
                                      (round(self.frameGeometry().height() / self.y) * 70))
        self.left_button = QPushButton("<--", self)
        self.left_button.clicked.connect(self.button_reg)
        self.left_button.setGeometry(0, self.frameGeometry().height() - (round(self.frameGeometry().height() / self.y) *
                                                                         (70 + round(
                                                                             self.y / self.frameGeometry().height()) * 30))
                                     , (round(self.frameGeometry().width() / self.x) * 100),
                                     (round(self.frameGeometry().height() / self.y) * 70))
        self.combo_label = QLabel("Выбор пути \nдо данных: ", self)
        self.combo_label.setFont(QFont('Times', 10))
        self.combo_label.move(self.combo_box.frameGeometry().x() - 70, self.combo_box.frameGeometry().y() - 5)
        self.image_label = QLabel("_No_images_", self)
        self.image_label.setFont(QFont('Times', 12))
        self.image_label.move(round(self.frameGeometry().width() / 2)
                              - round(self.image_label.frameGeometry().width() / 2),
                              round(self.frameGeometry().height() / 2)
                              - round(self.image_label.frameGeometry().height() / 2)
                              - round(self.frameGeometry().height() / self.y) * 20)
        self.combo_line_up = []
        self.combo_line_dw = []
        for i in range(30):
            self.combo_line_up.append(QLabel("_______________", self))
            self.combo_line_dw.append(QLabel("_______________", self))
            self.combo_line_up[i].setFont(QFont('Times', 10))
            self.combo_line_dw[i].setFont(QFont('Times', 10))
            self.combo_line_up[i].move(int(self.frameGeometry().width() / 2) + 75 * (i - 15),
                                       self.combo_box.frameGeometry().y(
                                       ) + 10)
            self.combo_line_dw[i].move(int(self.frameGeometry().width() / 2) + 75 * (i - 15),
                                       self.right_button.frameGeometry().y() - 20)

    # Активная часть
    def create_list_images(self, data_or_path_str) -> None:
        """
        This method is needed to create an iterator based on photos in a folder or on a DataFrame with paths to them.
         Next, it creates widgets of images on the screen with a certain size and a certain position,
          this is determined by the current resolution of the main window
        :param data_or_path_str: The path string to the folder or DataFrame may be empty
        :return None:
        """
        if data_or_path_str != "" and data_or_path_str != "  path" and data_or_path_str != "  .csv":
            self.Iter_imgs = KeywordPhotoIter(self.dir_or_csv, 0)
            if self.Iter_imgs.get_current_size() != 0:
                self.current_image = self.Iter_imgs.get_current_elem()
                self.image_label.setScaledContents(True)
                if ".csv" not in self.dir_or_csv:
                    self.image_label.setPixmap(QPixmap(f"{self.dir_or_csv}/{self.current_image}"))
                else:
                    self.image_label.setPixmap(QPixmap(f"{self.current_image}"))
            self.image_label.setFixedSize(round(self.frameGeometry().width() / self.x) * 400,
                                          round(self.frameGeometry().height() / self.y) * 340)
        if data_or_path_str == "" or self.Iter_imgs.get_current_size() == 0:
            if self.Iter_imgs.get_current_size() != 0:
                self.Iter_imgs = KeywordPhotoIter("", 0)
            self.current_image = ""
            self.image_label.setScaledContents(False)
            self.image_label.clear()
            self.image_label.setText("_No_images_")
            self.image_label.setFont(QFont('Times', 12))
            self.image_label.setFixedSize(100, 100)
        self.image_label.move(round(self.frameGeometry().width() / 2)
                              - round(self.image_label.frameGeometry().width() / 2),
                              round(self.frameGeometry().height() / 2)
                              - round(self.image_label.frameGeometry().height() / 2)
                              - round(self.frameGeometry().height() / self.y) * 20)

    def button_reg(self) -> None:
        """
        The method deals with changing the widget in the appropriate direction along the iterator,
         thereby changing the image following the list in two directions
        :return None:
        """
        if self.Iter_imgs.get_current_size() != 0:
            button_text = self.sender().text()
            if button_text == '-->':
                if self.Iter_imgs.get_current_index() == self.Iter_imgs.get_current_size() - 1:
                    self.Iter_imgs = KeywordPhotoIter(self.dir_or_csv, 0)
                    self.current_image = self.Iter_imgs.get_current_elem()
                else:
                    self.current_image = self.Iter_imgs.__next__()
            elif button_text == '<--':
                if self.Iter_imgs.get_current_index() == 0:
                    self.Iter_imgs = KeywordPhotoIter(self.dir_or_csv, 1)
                    self.current_image = self.Iter_imgs.get_current_elem()
                else:
                    self.current_image = self.Iter_imgs.back()
            self.image_label.setScaledContents(True)
            if ".csv" not in self.dir_or_csv:
                self.image_label.setPixmap(QPixmap(
                    f"{self.dir_or_csv}/{self.current_image}"))
            else:
                self.image_label.setPixmap(QPixmap(f"{self.current_image}"))

    def resizeEvent(self, event):
        """
        Method for generating a resizing event
        :param event:
        :return super().resizeEvent(event): Transmits the occurrence of an event
        """
        self.resized.emit()
        return super().resizeEvent(event)

    def resize_widgets(self) -> None:
        """
        The method adjusts the widget sizes to the changed size of the main window,
         and is triggered after an event is detected
        :return None:
        """
        self.combo_box.setGeometry(int(self.frameGeometry().width() / 2) - (int(self.frameGeometry().width() / self.x) *
                                                                            170), int(self.frameGeometry().height() / 2)
                                   - (int(self.frameGeometry().height() / self.y) * 240),
                                   (int(self.frameGeometry().width() / self.x) * 400), 20)
        self.combo_label.move(self.combo_box.frameGeometry().x() - 70, self.combo_box.frameGeometry().y() - 5)
        if self.Iter_imgs.get_current_size() != 0:
            self.image_label.setFixedSize(round(self.frameGeometry().width() / self.x) * 400,
                                          round(self.frameGeometry().height() / self.y) * 340)
        self.image_label.move(round(self.frameGeometry().width() / 2)
                              - round(self.image_label.frameGeometry().width() / 2),
                              round(self.frameGeometry().height() / 2)
                              - round(self.image_label.frameGeometry().height() / 2)
                              - round(self.frameGeometry().height() / self.y) * 20)
        self.right_button.setGeometry(self.frameGeometry().width() - (round(self.frameGeometry().width() / self.x) * 100
                                                                      ), self.frameGeometry().height() -
                                      (round(self.frameGeometry().height() / self.y) *
                                       (70 + round(self.y / self.frameGeometry().height()) * 30))
                                      , (round(self.frameGeometry().width() / self.x) * 100),
                                      (round(self.frameGeometry().height() / self.y) * 70))
        self.left_button.setGeometry(0, self.frameGeometry().height() - (round(self.frameGeometry().height() / self.y) *
                                                                         (70 + round(
                                                                             self.y / self.frameGeometry().height()) * 30))
                                     , (round(self.frameGeometry().width() / self.x) * 100),
                                     (round(self.frameGeometry().height() / self.y) * 70))
        for i in range(30):
            self.combo_line_up[i].move(int(self.frameGeometry().width() / 2) + 75 * (i - 15),
                                       self.combo_box.frameGeometry().y(
                                       ) + 10)
            self.combo_line_dw[i].move(int(self.frameGeometry().width() / 2) + 75 * (i - 15),
                                       self.right_button.frameGeometry().y() - 20)

    def select_dir(self, ind_comb):
        """
        The method opens a window for selecting a folder or file,
         depending on what the user has selected in the ComboBox widget, respectively,
          after selecting, the path to the selected object is placed in the ComboBox line
        :param ind_comb: The index of the selected option, path, or DataFrame
        :return None:
        """
        if ind_comb == 1:
            self.dir_or_csv = str(QFileDialog.getExistingDirectory(self, "Выберите папку"))
        elif ind_comb == 2:
            filename = QFileDialog.getOpenFileName(self, "Выберите файл", '', "DataFrame (*.csv)")
            self.dir_or_csv = filename[0]
        self.combo_box.setItemText(0, self.dir_or_csv)
        self.combo_box.setCurrentIndex(0)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
