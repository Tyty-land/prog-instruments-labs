from image_iter import KeywordPhotoIter
from config import IMG_EXTNS

class AppState:
    """
    A class for managing the application state.
    Manages the application state using an existing KeywordPhotoIter.
    """

    def __init__(self):
        self.image_iterator = None
        self.source_path = ""
        self.source_type = ""
        self.current_image_display_path = ""

    def initialize_iterator(self, source_path: str, start_from_end: bool = False):
        """
        Initializes the iterator using an existing KeywordPhotoIter.

        :param source_path: Path to a folder or CSV file
        :param start_from_end: Start from the end of the list
        """

        self.source_path = source_path
        if IMG_EXTNS[5] in source_path:
            self.source_type = 'csv'
        else:
            self.source_type = 'directory'

        self.image_iterator = KeywordPhotoIter(source_path, start_from_end)
        self._update_current_image_display_path()

    def _update_current_image_display_path(self):
        """Updates the path to display the current image."""
        if self.has_images():
            current_elem = self.image_iterator.get_current_elem()
            if self.source_type == 'directory':
                self.current_image_display_path = f"{self.source_path}/{current_elem}"
            else:
                self.current_image_display_path = current_elem
        else:
            self.current_image_display_path = ""

    def next_image(self):
        """Skip to the next image"""
        if self.has_images():
            if self.image_iterator.get_current_index() == self.image_iterator.get_current_size() - 1:
                self.initialize_iterator(self.source_path, False)
            else:
                self.image_iterator.__next__()
            self._update_current_image_display_path()
            return self.current_image_display_path
        return ""

    def previous_image(self):
        """Go to the previous image"""
        if self.has_images():
            if self.image_iterator.get_current_index() == 0:
                self.initialize_iterator(self.source_path, True)
            else:
                self.image_iterator.back()
            self._update_current_image_display_path()
            return self.current_image_display_path
        return ""

    def has_images(self) -> bool:
        """Checks if there are images to display."""
        return self.image_iterator is not None and self.image_iterator.get_current_size() > 0

    def total_images(self) -> int:
        """Returns the total number of images"""
        if self.image_iterator is not None:
            return self.image_iterator.get_current_size()
        return 0

    def current_index(self) -> int:
        """Returns the current index"""
        if self.image_iterator is not None:
            return self.image_iterator.get_current_index()
        return 0

    def get_current_image_for_display(self):
        """Returns the path to the current image to display"""
        return self.current_image_display_path

    def reset(self):
        """Reset the status"""
        self.image_iterator = None
        self.source_path = ""
        self.source_type = ""
        self.current_image_display_path = ""
