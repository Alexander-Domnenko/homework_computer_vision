import numpy as np


def load_image_data(image_number):
    try:
        file_name = f'figure{image_number}.txt'
        with open(file_name) as file:
            max_mm = float(next(file))
            data = np.loadtxt(file, skiprows=1, dtype='float')
        return data, max_mm
    except FileNotFoundError:
        print(f'file {file_name} does not exists')
        return None


def calculate_nominal_resolution(data, max_mm):
    arr = np.sum(data, axis=0)
    number_of_pixels = 0
    k = 0
    for value in arr:
        if value != 0:
            k += 1
            number_of_pixels = max(number_of_pixels, k)
        else:
            k = 0
    if number_of_pixels:
        return max_mm / number_of_pixels


def main():
    for i in range(1, 6):
        result = load_image_data(i)
        if result is not None:
            data, max_mm = result
            nominal_resolution = calculate_nominal_resolution(data, max_mm)
            print(f'resolution image{i}: ', nominal_resolution)


main()
