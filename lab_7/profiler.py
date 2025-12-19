import cProfile
import pstats
import os
import sys

from tools_dataframe_module import reader_csv
from tools_lab_module import sort_data

def quick_profile():
    """Быстрый профайлинг наиболее критичных функций."""
    # Создаем тестовый CSV файл
    test_content = """Absolute Path:;Relative path:;Height:;Width:;Color_depth:
/path/img1.jpg;img1.jpg;800;600;24
/path/img2.jpg;img2.jpg;1024;768;32
/path/img3.jpg;img3.jpg;640;480;16
/path/img4.jpg;img4.jpg;1920;1080;24
/path/img5.jpg;img5.jpg;1280;720;32
"""

    test_file = "test_profile.csv"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)

    with open('profile_end.txt', 'w', encoding='utf-8') as f:
        # Профайлинг reader_csv
        f.write("\n1. Профайлинг reader_csv (1000 вызовов):\n")
        f.write("-" * 60 + "\n")

        profiler = cProfile.Profile()
        profiler.enable()

        for _ in range(1000):
            data = reader_csv(test_file)

        profiler.disable()

        stats_stream = open('temp_stats.txt', 'w')
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.sort_stats('cumulative').print_stats(10)
        stats_stream.close()

        with open('temp_stats.txt', 'r') as temp:
            f.write(temp.read())

        # Профайлинг sort_data
        f.write("\n2. Профайлинг sort_data (1000 элементов, 100 вызовов):\n")
        f.write("-" * 60 + "\n")

        import random
        test_data = [["Height:", "Width:"]] + [[str(random.randint(100, 2000)),
                                                str(random.randint(100, 2000))]
                                               for _ in range(1000)]

        profiler = cProfile.Profile()
        profiler.enable()

        for _ in range(100):
            sorted_data = sort_data(test_data.copy(), 1)

        profiler.disable()

        stats_stream = open('temp_stats2.txt', 'w')
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.sort_stats('cumulative').print_stats(10)
        stats_stream.close()

        with open('temp_stats2.txt', 'r') as temp:
            f.write(temp.read())

        # Создаем бОльший файл для тестирования масштабирования
        f.write("\n3. Тестирование масштабируемости (5000 элементов):\n")
        f.write("-" * 60 + "\n")

        large_test_data = [["Height:", "Width:"]] + [[str(random.randint(100, 2000)),
                                                      str(random.randint(100, 2000))]
                                                     for _ in range(5000)]

        import time
        start_time = time.time()
        sort_data(large_test_data.copy(), 1)
        elapsed_time = time.time() - start_time

        f.write(f"Время сортировки 5000 элементов: {elapsed_time:.4f} секунд\n")
        f.write(f"Оценка сложности: O(n²) - время растет квадратично\n")

    # Удаляем временные файлы
    os.remove(test_file)
    if os.path.exists('temp_stats.txt'):
        os.remove('temp_stats.txt')
    if os.path.exists('temp_stats2.txt'):
        os.remove('temp_stats2.txt')


if __name__ == "__main__":
    quick_profile()
