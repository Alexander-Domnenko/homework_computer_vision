import numpy as np


def load_image_from_file(file_name):
    try:
        return np.loadtxt(file_name, skiprows=1)
    except FileNotFoundError:
        print(f'file {file_name} does not exist')
        return None


def find_first_ones_indices(image):
    y_indices, x_indices = np.where(image == 1)
    return np.min(y_indices), np.min(x_indices)


def find_image_offset(image1, image2):
    first_y_index, first_x_index = find_first_ones_indices(image1)
    second_y_index, second_x_index = find_first_ones_indices(image2)
    return second_x_index - first_x_index, second_y_index - first_y_index


def main():
    file1 = 'img1.txt'
    file2 = 'img2.txt'

    image1 = load_image_from_file(file1)
    image2 = load_image_from_file(file2)

    if image1 is not None and image2 is not None:
        offset_x, offset_y = find_image_offset(image1, image2)
        print(f'offset x: {offset_x}')
        print(f'offset y: {offset_y}')


main()
