import os
import re

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
    if re.search(r"\w:/", path_save) is None:
        path_save = CONST_activ_dir + path_save
    absolut_dir = (path_save + "/").replace("\\", "/").replace("//", "/")
    return absolut_dir
