import numpy as np
import matplotlib.pyplot  as plt
from skimage.morphology import (binary_closing, binary_erosion, binary_opening)
from skimage.measure import label

plus_mask = np.array([[0,0,1,0,0],
                      [0,0,1,0,0],
                      [1,1,1,1,1],
                      [0,0,1,0,0],
                      [0,0,1,0,0]])

stars_mask = np.array([[1,0,0,0,1],
                       [0,1,0,1,0],
                       [0,0,1,0,0],
                       [0,1,0,1,0],
                       [1,0,0,0,1]])


data = np.load('stars.npy')


print('count stars and plus: ',np.max(label(binary_erosion(data,plus_mask)))+np.max(label(binary_erosion(data,stars_mask))))

