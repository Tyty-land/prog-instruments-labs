from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QFont

class ImageViewer(QLabel):
    """
    Widget for displaying images with original positioning logic
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_scaled = None
        self.base_x = 720  # Базовая ширина
        self.base_y = 500  # Базовая высота
        self._setup_defaults()

    def _setup_defaults(self):
        """Setting default values (original logic)"""
        self.setText("_No_images_")
        self.setFont(QFont('Times', 12))
        self._is_scaled = False

    def display_image(self, image_path: str):
        """
        Displays the image while maintaining the original logic.

        :param image_path: The full path to the image
        """
        if image_path:
            self.setScaledContents(True)
            pixmap = QPixmap(image_path)
            self.setPixmap(pixmap)
            self._is_scaled = True
        else:
            self.clear_display()

    def clear_display(self):
        """Clearing the display (original logic)"""
        self.setScaledContents(False)
        self.clear()
        self.setText("_No_images_")
        self.setFont(QFont('Times', 12))
        self._is_scaled = False
        self.setFixedSize(100, 100)

    def update_geometry(self, window_width: int, window_height: int):
        """
        Updates the geometry of the widget (retains the original calculation logic).

        :param window_width: The current width of the window
        :param window_height: The current height of the window
        """
        if self._is_scaled:
            new_width = round(window_width / self.base_x) * 400
            new_height = round(window_height / self.base_y) * 340
            self.setFixedSize(new_width, new_height)

        label_width = self.width()
        label_height = self.height()

        x = round(window_width / 2) - round(label_width / 2)
        y = (round(window_height / 2) - round(label_height / 2) -
             round(window_height / self.base_y) * 20)

        self.move(x, y)
