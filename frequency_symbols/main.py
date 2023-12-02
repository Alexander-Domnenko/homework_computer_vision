from skimage.measure import label, regionprops
import numpy as np
import matplotlib.pyplot as plt


def circularity_std(area, perimeter):
    r = perimeter / (2 * np.pi) + 0.5
    circularity = (4 * np.pi * area / perimeter**2) * (1 - 0.5 / r)**2
    return circularity

def has_vline(arr):
    return 1. in arr.mean(0)

def has_vline_first_column(arr):
    res = np.all(arr[:, 0], axis=0)
    return res

def has_hline(arr):
    return 1. in arr.mean(1)

image = plt.imread('symbols.png').mean(2) > 0
labeled = label(image)

def recognize(prop):
    euler_number = prop.euler_number

    if euler_number == -1:
        if has_vline_first_column(prop.image):
            return 'B'
        return '8'
    elif euler_number == 0:
        y, x = prop.centroid_local
        y /= prop.image.shape[0]
        x /= prop.image.shape[1]
        
        if euler_number == 0 and has_vline_first_column(prop.image):
            if (circularity_std(prop.area, prop.perimeter)) <= 0.205:
                return 'D'
            return 'P'
        elif has_hline(prop.image):
            return '*'
        elif np.isclose(x, y, 0.07):
            if prop.image[prop.image.shape[0] // 2][prop.image.shape[1] // 2] == 0:
                return '0'
        elif prop.image[prop.image.shape[0] - 1, 0]:
            return 'A'
    else:
        if prop.image.mean() == 1.0:
            return '-'
        else:
            mean_arr = prop.image.mean(0)
            
            if mean_arr[mean_arr == 1].shape[0] > 1:
                return '1'
            else:
                tmp = prop.image.copy()
                tmp[[0, -1], :] = 1
                tmp[:, [0, -1]] = 1
                tmp_labeled = label(tmp)
                tmp_props = regionprops(tmp_labeled)
                tmp_euler = tmp_props[0].euler_number

                if tmp_euler == -3:
                    return 'X'
                elif tmp_euler == -1: 
                    return '/'
                elif prop.eccentricity > 0.5:
                    return 'W'
                return '*'
    return 'undefined'

props = regionprops(labeled)
result = {}

for prop in props:
    symbol = recognize(prop)
    
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1

print(result)

print(f"percentage of character recognition: {(sum(result.values()) - result.get('undefined', 0)) / sum(result.values()) * 100}")
