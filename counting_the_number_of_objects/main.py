import numpy as np
from scipy.ndimage import binary_hit_or_miss
from skimage.measure import label, regionprops

def load_image(file_path):
    try:
        file_name = file_path
        data = np.load(file_name)
        return data
    except FileNotFoundError:
        print(f'File {file_name} does not exist')
        return None 

def get_labeled_image(image):
    return label(image)

def get_regions_properties(a):
    return regionprops(a)

def find_regions_in_image(regions, image):
    mask_object = []
    regions = get_regions_properties(regions)
    for props in regions:
        minr, minc, maxr, maxc = props.bbox
        mask_object.append(image[minr:maxr, minc:maxc])
    return mask_object

def find_unique_masks(mask_object):
    unique_masks = []
    for mask in mask_object:
        is_unique = True
        for existing_mask in unique_masks:
            if np.array_equal(mask, existing_mask):
                is_unique = False
                break
        if is_unique:
            unique_masks.append(mask)
    return unique_masks

def count_objects(unique_masks, image):
    object_counts = []
    for i in range(len(unique_masks)):
        result = binary_hit_or_miss(image, unique_masks[i])
        object_counts.append(np.sum(result))
    total_objects = np.max(get_labeled_image(image))
    return object_counts, total_objects

file_path = "psnpy.txt"
image = load_image(file_path)

if image is not None:
    labeled_image = get_labeled_image(image)
    mask_objects = find_regions_in_image(labeled_image, image)
    unique_masks = find_unique_masks(mask_objects)
    object_counts, total_objects = count_objects(unique_masks, labeled_image)

    for i, count in enumerate(object_counts):
        print(f'Object {i + 1} quantity = {count}')
    print(f'Count all objects = {total_objects}')
