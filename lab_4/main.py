import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore

from config import IMG_EXTNS
from app_state import AppState
from widgets.image_viewer import ImageViewer
from widgets.navigation_buttons import NavigationButtons
from widgets.source_selector import SourceSelector
from widgets.decorative_lines import DecorativeLines

class MainWindow(QMainWindow):
    """
    The main window of the application that uses the components.
    Retains all original functionality.
    """
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application")
        self.x = 720
        self.y = 500
        self.resize(self.x, self.y)
        self.app_state = AppState()
        self._init_components()
        self.resized.connect(self.resize_widgets)
        self.source_selector.source_selected.connect(self._on_source_selected)

    def _init_components(self):
        """
        Initialization of all components
        """
        self.source_selector = SourceSelector(self, self.x, self.y)
        self.source_selector.text_changed.connect(self.create_list_images)
        self.image_viewer = ImageViewer(self)
        self.image_viewer.base_x = self.x
        self.image_viewer.base_y = self.y
        self.image_viewer.update_geometry(self.width(), self.height())
        self.nav_buttons = NavigationButtons(self, self.x, self.y)
        self.nav_buttons.next_clicked.connect(self._on_next_clicked)
        self.nav_buttons.prev_clicked.connect(self._on_prev_clicked)
        self.decorative_lines = DecorativeLines(self, self.x, self.y)
        self._update_lines_position()

    def _update_lines_position(self):
        """
        Updating the position of decorative lines
        """
        combo_y = self.source_selector.get_combo_box_y()
        right_btn_y = self.nav_buttons.get_right_button_y()

        self.decorative_lines.update_geometry(
            self.width(), self.height(), combo_y, right_btn_y
        )

    def _on_source_selected(self, path: str):
        """
        Data source selection handler
        """
        self.source_selector.current_path = path
        self.app_state.source_path = path

    def create_list_images(self, data_or_path_str) -> None:
        """
        Create a list of images based on the selected source.
        Retains the original logic.
        """
        if (data_or_path_str != "" and
                data_or_path_str != "  path" and
                data_or_path_str != "  .csv"):

            path = self.source_selector.current_path
            self.app_state.initialize_iterator(path, False)

            if self.app_state.has_images():
                image_path = self.app_state.get_current_image_for_display()
                self.image_viewer.display_image(image_path)
                self.image_viewer.update_geometry(self.width(), self.height())
            else:
                self.image_viewer.clear_display()
        else:
            self.app_state.reset()
            self.image_viewer.clear_display()

        self.image_viewer.update_geometry(self.width(), self.height())

    def _on_next_clicked(self):
        """
        Handler for pressing the 'forward' button
        """
        image_path = self.app_state.next_image()
        if image_path:
            self.image_viewer.display_image(image_path)
            self.image_viewer.update_geometry(self.width(), self.height())

    def _on_prev_clicked(self):
        """
        Handler for pressing the 'back' button
        """
        image_path = self.app_state.previous_image()
        if image_path:
            self.image_viewer.display_image(image_path)
            self.image_viewer.update_geometry(self.width(), self.height())

    def resizeEvent(self, event):
        """
        A method for handling the window resizing event.
        Retains the original logic.
        """
        self.resized.emit()
        return super().resizeEvent(event)

    def resize_widgets(self) -> None:
        """
        A method for updating widget sizes when the window size changes.
        Retains the original logic.
        """
        current_width = self.width()
        current_height = self.height()

        self.source_selector.update_geometry(current_width, current_height)
        self.image_viewer.update_geometry(current_width, current_height)
        self.nav_buttons.update_geometry(current_width, current_height)
        self._update_lines_position()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
