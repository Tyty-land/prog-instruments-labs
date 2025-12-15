from PyQt5.QtWidgets import QComboBox, QLabel, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QObject, pyqtSignal

class SourceSelector(QObject):
    """
    A component for selecting a data source while maintaining the original logic.
    """

    source_selected = pyqtSignal(str)
    text_changed = pyqtSignal(str)

    def __init__(self, parent, base_x: int = 720, base_y: int = 500):
        super().__init__(parent)
        self.parent = parent
        self.base_x = base_x
        self.base_y = base_y
        self.current_path = ""

        self.combo_box = QComboBox(parent)
        self.combo_label = QLabel("Выбор пути \nдо данных: ", parent)

        self._setup_widgets()
        self._setup_connections()

    def _setup_widgets(self):
        """Widget setup (original logic)"""
        self.combo_box.addItems(['', '  path', '  .csv'])
        self.combo_label.setFont(QFont('Times', 10))

    def _setup_connections(self):
        """Configuring Signal connections"""
        self.combo_box.currentIndexChanged.connect(self._handle_selection)
        self.combo_box.currentTextChanged.connect(self.text_changed.emit)

    def _handle_selection(self, index: int):
        """Selection processing in the combo box (original logic)"""
        if index == 1:  # Папка
            self._select_directory()
        elif index == 2:  # CSV файл
            self._select_csv_file()

    def _select_directory(self):
        """Folder selection (original logic)"""
        path = str(QFileDialog.getExistingDirectory(self.parent, "Выберите папку"))
        if path:
            self.current_path = path
            self.combo_box.setItemText(0, path)
            self.combo_box.setCurrentIndex(0)
            self.source_selected.emit(path)

    def _select_csv_file(self):
        """Selecting a CSV file (original logic)"""
        filename = QFileDialog.getOpenFileName(
            self.parent, "Выберите файл", '', "DataFrame (*.csv)"
        )
        if filename[0]:
            self.current_path = filename[0]
            self.combo_box.setItemText(0, filename[0])
            self.combo_box.setCurrentIndex(0)
            self.source_selected.emit(filename[0])

    def update_geometry(self, window_width: int, window_height: int):
        """
        Updates the geometry of the component (retains the original calculation logic).

        :param window_width: The current width of the window
        :param window_height: The current height of the window
        """
        x = int(window_width / 2) - (int(window_width / self.base_x) * 170)
        y = int(window_height / 2) - (int(window_height / self.base_y) * 240)
        width = (int(window_width / self.base_x) * 400)
        height = 20

        self.combo_box.setGeometry(x, y, width, height)
        self.combo_label.move(x - 70, y - 5)

    def get_combo_box_y(self):
        """Returns the Y-coordinate of the combo box for decorative lines"""
        return self.combo_box.geometry().y()
