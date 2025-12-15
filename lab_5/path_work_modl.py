import os
import re
import logging

logger = logging.getLogger('ImageProcessor.PathUtils')

CONST_activ_dir = os.getcwd().replace("\\", "/").lower() + "/"

def clear_name_image(path_image: str) -> str:
    """
    Selects the file name from the full path to it.
    It is necessary to display the name in the title of the graph
    histograms
    :param path_image: the path to the file with its name in one line
    :return clear_name: clean file name
    """
    split_path = path_image.split("/")
    clear_name = split_path[-1]
    return clear_name


def create_absolut_dir(path_save: str) -> str:
    """
    This function converts a string that contains the path to the save folder,
    to a more suitable one for the rest of the program code
    :param path_save: path to the save folder (maybe relative)
    :return absolut_dir: absolute path to the save folder
    """
    original_path = path_save

    if re.search(r"\w:/", path_save) is None:
        path_save = CONST_activ_dir + path_save
        logger.debug(f"Относительный путь '{original_path}' преобразован в абсолютный: '{path_save}'")
    else:
        logger.debug(f"Путь уже абсолютный: '{path_save}'")

    absolut_dir = (path_save + "/").replace("\\", "/").replace("//", "/")

    # ЛОГИРОВАНИЕ: результат преобразования
    if absolut_dir != original_path:
        logger.info(f"Преобразован путь: '{original_path}' -> '{absolut_dir}'")

    return absolut_dir
