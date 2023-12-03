import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def load_image_data(count_files):
    try:
        data = []
        for i in range(count_files):
            data.append(np.load(f"out\\h_{i}.npy"))
        return data
    except FileNotFoundError:
        return 'file does not exist'

count_files = 100
data = load_image_data(count_files)

centroids_1 = []
centroids_2 = []

for i in range(count_files):
    labeled = label(data[i])
    regions = regionprops(labeled)

    sorted_regions = sorted(regions, key=lambda region: region.area)
    first_figure = sorted_regions[:len(sorted_regions)//2]
    second_figure = sorted_regions[len(sorted_regions)//2:]

    for region in first_figure:
        centroids_1.append(region.centroid)
    for region in second_figure:
        centroids_2.append(region.centroid)   

x_coords_1, y_coords_1 = zip(*centroids_1)
x_coords_2, y_coords_2 = zip(*centroids_2)

plt.plot(x_coords_1, y_coords_1)
plt.plot(x_coords_2, y_coords_2)
plt.show()
