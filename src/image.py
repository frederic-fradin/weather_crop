from PIL import Image, ImageDraw
import requests
import cv2
import numpy as np

def_url = 'https://www.worldagweather.com/fcstwx/tmp_gefs_day7_in_metric_2440.png'

def main_colors(url_local):
    # img = Image.open(requests.get(url, stream=True).raw)
    img = cv2.imread(url_local)
    img = np.flip(img, axis=-1)
    height, width, _ = np.shape(img)
    print(height, width)

    data = np.reshape(img, (height * width, 3))
    data = np.float32(data)

    number_clusters = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
    # print(centers)

    font = cv2.FONT_HERSHEY_SIMPLEX
    bars = []
    rgb_values = []

    for index, row in enumerate(centers):
        bar, rgb = create_bar(200, 200, row)
        bars.append(bar)
        rgb_values.append(rgb)

    img_bar = np.hstack(bars)
    color_ref = {}
    for index, row in enumerate(rgb_values):
        image = cv2.putText(img_bar, f'{index + 1}. RGB: {row}', (5 + 200 * index, 200 - 10),
                            font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        print(f'{index + 1}. RGB{row}')
        color_ref[index] = row

    return img_bar, color_ref

def crop_image(url:str, left:int, top:int, right:int, bottom:int) -> object:
    # Opens a image in RGB mode
    im = Image.open(requests.get(url, stream=True).raw)
    
    # Cropped image of above dimension
    # (It will not change original image)
    im_crop = im.crop((left, top, right, bottom))

    # save a image using extension
    im_crop.save("./reports/figures/crop_image.png")

    # Define matin colors

    img_bar, color_ref = main_colors(url_local="./reports/figures/crop_image.png")

    return im_crop, img_bar, color_ref

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
    main_colors()