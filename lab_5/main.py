import argparse
import cv2
from typing import Tuple

from path_work_modl import clear_name_image
from path_work_modl import create_absolut_dir
from work_with_images import delimiter_channel
from work_with_images import display_graph
from work_with_images import get_data_imgs


def get_p() -> Tuple[str, str]:
    """
    A function that accepts command line parameters, namely:
        -pi = path to the image
        -ps = path to the folder where RGB copies of the image are saved.
    then collects these parameters into a tuple and returns this tuple
    :return res_tuple: a tuple containing all three cmd parameters
    """
    p_cmd = argparse.ArgumentParser()
    p_cmd.add_argument('-pi', '--path_image', type=str, help="path_image")
    p_cmd.add_argument('-ps', '--path_save', type=str, help="path_save", default="")
    args = p_cmd.parse_args()
    res_tuple = (args.path_image.replace("\\", "/"), args.path_save.replace("\\", "/"))
    return res_tuple


def main() -> None:
    """
    The main function that uses the functionality of all the others
    it also starts all the work of the code
    :return None:
    """
    path_image, path_save = get_p()
    img = cv2.imread(path_image)
    res = get_data_imgs(img)
    display_graph(res[0], res[1], res[2], clear_name_image(path_image))
    delimiter_channel(path_image, create_absolut_dir(path_save))


if __name__ == '__main__':
    main()
