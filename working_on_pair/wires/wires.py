import numpy as np
import matplotlib.pyplot  as plt
from skimage.morphology import (binary_closing, binary_erosion, binary_opening)
from skimage.measure import label

struct = np.ones((3,1))

def load_image_data(image_number):
    try:
        file_name = f'wires/wires{image_number}.npy'
        data = np.load(file_name)
        return data
    except FileNotFoundError:
        print(f'file {file_name} does not exists')


def main():
    for i in range(1, 7):
        image = load_image_data(i)
        image = label(binary_opening(image, struct))
        plt.imshow(binary_opening(image,struct))
        wire_number =1 
        mark = True
        for segment in image:
            unique_values = np.unique(segment)
            num_unique = np.sum(unique_values != 0)
            if num_unique != 0 and mark and num_unique !=1:
                print(f'wire {wire_number} cut on {num_unique} parts')
                mark = False
            if num_unique == 0 and not mark:
                wire_number += 1
                mark = True
        print()
        plt.show()

main()
