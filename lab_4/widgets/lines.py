from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont

class DecorativeLines:
    """Decorative lines for the interface"""
    def __init__(self, parent, base_x: int = 720, base_y: int = 500):
        self.parent = parent
        self.base_x = base_x
        self.base_y = base_y
        self.combo_line_up = []
        self.combo_line_dw = []

        self._create_lines()

    def _create_lines(self):
        """Creating decorative lines (original logic)"""
        for i in range(30):
            # Верхние линии
            line_up = QLabel("_______________", self.parent)
            line_up.setFont(QFont('Times', 10))
            self.combo_line_up.append(line_up)

            # Нижние линии
            line_dw = QLabel("_______________", self.parent)
            line_dw.setFont(QFont('Times', 10))
            self.combo_line_dw.append(line_dw)

    def update_geometry(self, window_width: int, combo_box_y: int, right_button_y: int):
        """
        Updates the position of the lines (retains the original calculation logic).

        :param window_width: The current width of the window
        :param combo_box_y: Y-position of the combo box
        :param right_button_y: Y is the position of the right button
        """
        for i in range(30):
            x_up = int(window_width / 2) + 75 * (i - 15)
            y_up = combo_box_y + 10
            self.combo_line_up[i].move(x_up, y_up)

            x_dw = int(window_width / 2) + 75 * (i - 15)
            y_dw = right_button_y - 20
            self.combo_line_dw[i].move(x_dw, y_dw)
