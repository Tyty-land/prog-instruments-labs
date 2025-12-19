from typing import Tuple

import argparse
from icrawler.builtin import GoogleImageCrawler

from tools_dataframe_module import writer_csv, \
    pandas_statistical_calculation, demonstration_of_results
from tools_imgs_module import create_absolut_dir, \
    get_data_imgs, display_histogram
from tools_lab_module import data_frame_filter, sort_square_images


def get_p() -> Tuple[str, str, str]:
    """
     A function that accepts command-line parameters, namely:
        -k = keyword to search for a photo (default = "None")
        -sd = path to the future folder with photos (default = "")
        -D = path and name to the .csv DataFrame
        (default = "DataFrame.csv")
        then collects these parameters into a
        tuple and returns this tuple
    :return res_tuple: a tuple containing all three cmd parameters
    """
    p_cmd = argparse.ArgumentParser()
    p_cmd.add_argument("-k", "--keyword", type=str,
                       help="keyword", default="None")
    p_cmd.add_argument("-sd", "--save_dir", type=str,
                       help="save dir", default="")
    p_cmd.add_argument("-D", "--data_frame", type=str,
                       help="data frame file", default="DataFrame.csv")
    args = p_cmd.parse_args()
    res_tuple = (args.keyword, create_absolut_dir(args.save_dir),
               create_absolut_dir(args.data_frame))
    return res_tuple

def main() -> None:
    """
    The main function that performs the basic logic of the program.
    Some functions are designed to output sequential
    changes to the data in the DataFrame,
     as well as statistical data obtained by Pandas
    :return None:
    """
    key_word, save_dir, data_frame = get_p()
    google_crawl = GoogleImageCrawler(
        storage={'root_dir': f'{save_dir}image_{key_word}_dir'})
    google_crawl.crawl(keyword=key_word, max_num=10)
    writer_csv(get_data_imgs(f'{save_dir}image_{key_word}_dir'),
               data_frame, 0)
    print("\n[@] - Statistical data obtained using Pandas:\n")
    pd_st = pandas_statistical_calculation(data_frame)
    for i in range(len(pd_st)):
        for j in range(len(pd_st[i])):
            print(pd_st[i][j], "\n")
    print("[@] - The initial version of the DataFrame:")
    demonstration_of_results(data_frame)
    data_frame_filter(data_frame, int(pd_st[0][5]), int(pd_st[1][5]))
    print("[@] - Filtered by DataFrame assignment:")
    demonstration_of_results(data_frame)
    sort_square_images(data_frame)
    print("[@] - Sorted by the added column of DataFrame areas:")
    demonstration_of_results(data_frame)
    display_histogram(data_frame, 5)


if __name__ == '__main__':
    main()
