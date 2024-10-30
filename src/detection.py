import os
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.cluster import KMeans

os.environ['OMP_NUM_THREADS'] = '1'

image = mpimg.imread('../reports/figures/test2.png')
w, h, d = tuple(image.shape)
pixels = np.reshape(image, (w * h, d))


n_colors = 10
model = KMeans(n_clusters=n_colors, random_state=256).fit(pixels)
palette = np.uint8(model.cluster_centers_)
plt.imshow([palette])
plt.show()