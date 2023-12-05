import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

color_image = cv2.imread('balls_and_rects.png')

hsv = cv2.cvtColor(color_image, cv2.COLOR_RGB2HSV)
h = hsv[:,:,0]

binary = color_image.mean(2) > 0
labeled = label(binary)

props = regionprops(labeled)

circle_colors = []
rect_colors = []

def circularity_std(area, perimeter):
    r = perimeter / (2 * np.pi) + 0.5
    circularity = (4 * np.pi * area / perimeter**2) * (1 - 0.5 / r)**2
    return circularity

def recognize(prop):
    minr, minc, maxr, maxc = prop.bbox
    r = h[minr:maxr, minc:maxc]
   
    if circularity_std(prop.area, prop.perimeter) >= 0.86: 

        circle_colors.append(np.unique(r[0])[1])
        return 'circle'    
    
    rect_colors.append(r[0][0])
    return 'rect'

result = {}

for prop in props:
    symbol = recognize(prop)
    
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1

print(f"Count circle: {result.get('circle')} have {len(np.unique(circle_colors))} unique colors")
print(f"Count circle: {result.get('rect')} have {len(np.unique(rect_colors))} unique colors")
