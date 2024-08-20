from PIL import Image, ImageDraw
import requests
import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os

def_url = 'https://www.worldagweather.com/fcstwx/tmp_gefs_day7_in_metric_2440.png'

os.environ['OMP_NUM_THREADS'] = '2'

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_colors(image, number_of_colors):
    
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    
    counts = Counter(labels)
    
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    
    return hex_colors

def crop_image(url:str, left:int, top:int, right:int, bottom:int) -> object:
    # Opens a image in RGB mode
    im = Image.open(requests.get(url, stream=True).raw)
    
    # Cropped image of above dimension
    im_crop = im.crop((left, top, right, bottom))

    # save a image using extension
    im_crop.save("./reports/figures/crop_image.png")
    color_ref = get_colors(get_image("./reports/figures/crop_image.png"), 13)

    return im_crop, color_ref

def image_rectangle(url:str, left:int, top:int, right:int, bottom:int, forme:str):
    im = Image.open(requests.get(url, stream=True).raw)

    shape = [(left, top), (right, bottom)]

    # create  rectangleimage 
    img1 = ImageDraw.Draw(im)
    if forme == 'ellipse':
        img1.ellipse(shape, fill=None, outline=(255, 0, 0), width=3) 
    else:
        img1.rectangle(shape, fill=None, outline=(255, 0, 0), width=3) 
    
    return im

def create_bar(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    return bar, (red, green, blue)

if __name__ == '__main__':
    # image_rectangle(def_url, 100, 100, 350, 350)
    # crop_image(def_url, 10, 10, 50, 50)
    pass

ref_image_color = [405, 50, 420, 545, 'rectangle']

default_color = [
                "#00afe9",
                "#360571",
                "#f402c1",
                "#004df4",
                "#0000d2",
                "#00fefe",
                "#00039e",
                "#c3c2c2",
                "#161414",
                "#ba7b00",
                "#fe8700",
                "#f50300",
                "#fbe600"
                ]