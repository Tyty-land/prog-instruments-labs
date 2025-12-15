from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QObject, pyqtSignal

class NavigationButtons(QObject):
    """Control of navigation buttons while maintaining the original logic"""

    next_clicked = pyqtSignal()
    prev_clicked = pyqtSignal()

    def __init__(self, parent, base_x: int = 720, base_y: int = 500):
        super().__init__(parent)
        self.parent = parent
        self.base_x = base_x
        self.base_y = base_y

        self.right_button = QPushButton("-->", parent)
        self.left_button = QPushButton("<--", parent)

        self._setup_connections()

    def _setup_connections(self):
        """Configuring Signal connections"""
        self.right_button.clicked.connect(self.next_clicked.emit)
        self.left_button.clicked.connect(self.prev_clicked.emit)

    def update_geometry(self, window_width: int, window_height: int):
        """
        Updates the geometry of the buttons (retains the original calculation logic).

        :param window_width: The current width of the window
        :param window_height: The current height of the window
        """
        right_x = window_width - (round(window_width / self.base_x) * 100)
        right_y = window_height - (
                round(window_height / self.base_y) *
                (70 + round(self.base_y / window_height) * 30)
        )
        right_width = round(window_width / self.base_x) * 100
        right_height = round(window_height / self.base_y) * 70

        self.right_button.setGeometry(right_x, right_y, right_width, right_height)

        left_y = window_height - (
                round(window_height / self.base_y) *
                (70 + round(self.base_y / window_height) * 30)
        )
        left_width = round(window_width / self.base_x) * 100
        left_height = round(window_height / self.base_y) * 70

        self.left_button.setGeometry(0, left_y, left_width, left_height)

    def get_right_button_y(self):
        """Returns the Y-coordinate of the right button for decorative lines"""
        return self.right_button.geometry().y()
