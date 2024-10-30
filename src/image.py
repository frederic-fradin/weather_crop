from PIL import Image, ImageDraw
import requests
import cv2
import extcolors
import os
import pandas as pd
import plotly.express as px


def_url = 'https://www.worldagweather.com/fcstwx/tmp_gefs_day7_in_metric_2440.png'

os.environ['OMP_NUM_THREADS'] = '2'

color_legend = {
                "(255, 0, 201)":10,
                "(255, 0, 0)":8,
                "(255, 110, 0)":6,
                "(255, 160, 0)":4,
                "(255, 210, 0)":2,
                "(255, 255, 0)":1,
                "(200, 200, 200)":0,    # gris
                "(255, 255, 255)":0,    # blanc
                "(72, 108, 139)":0,     # ocean
                "(0, 255, 255)":-1,
                "(0, 180, 255)":-2,
                "(0, 80, 255)":-4,
                "(0, 0, 211)":-6,
                "(0, 0, 161)":-8,
                "(60, 0, 120)":-10
                }


def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_colors(img_path):
    img = Image.open(img_path).convert("RGBA")
    return extcolors.extract_from_image(img, tolerance=25, limit=5)

def create_image_entry(colors, file_name):
    total_pixels = colors[1]
    image_dict = {'file_name': file_name}
    image_colors = [{'colorCode': str(index), 'percent': round(color / total_pixels * 100)} for index, color in
                    colors[0] if round(color / total_pixels * 100) >= 1]
    image_dict['img_colors'] = image_colors

    # Convert the img_colors data to a DataFrame
    df = pd.DataFrame(image_dict["img_colors"])
    df['colorlegend'] = df['colorCode']
    df['colorCode'] = df['colorCode'].apply(lambda x: 'rgb' + x)

    # Map scores from color_legend and calculate the score
    df['score'] = df['colorlegend'].map(color_legend) * (df['percent']/100)
    total_score = df['score'].sum()
    title_name = f'Scoring {str(round(total_score,2))}'

    # Create the bar chart
    fig = px.bar(df,
                x='colorCode', y='percent', color='colorCode', text='percent',
                color_discrete_sequence=df['colorCode'],  # Set the bar colors based on colorCode
                width=1080, height=420, text_auto=True, title=title_name,
                )

    fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title=None)
    fig.update_traces(marker_line_color='rgb(200,200,200)', marker_line_width=1)
    
    df = px.data.iris()
    fig2 = px.scatter(df, x="petal_length", y="petal_width")
    fig2.update_layout(showlegend=False, yaxis_title=None, xaxis_title=None)
    fig2.add_hline(y=8, line_width=1, line_color='rgb(255, 0, 0)')
    fig2.add_hline(y=4, line_width=1, line_color='rgb(255, 160, 0)')
    fig2.add_hline(y=2, line_width=1, line_color='rgb(255, 210, 0)')
    fig2.add_hline(y=-2, line_width=1, line_color='rgb(0, 255, 255)')
    fig2.add_hline(y=-4, line_width=1, line_color='rgb(0, 180, 255)')
    fig2.add_hline(y=-8, line_width=1, line_color='rgb(0, 0, 211)')

    return image_dict, fig, fig2

def get_size(img_path):
    im = Image.open(requests.get(img_path, stream=True).raw)
    width = im.width 
    height = im.height

    return (width, height)

def crop_image(url:str, left:int, top:int, right:int, bottom:int) -> object:
    # Opens a image in RGB mode
    im = Image.open(requests.get(url, stream=True).raw)
    
    # Cropped image of above dimension
    im_crop = im.crop((left, top, right, bottom))

    # save a image using extension
    url_crop = "./reports/figures/crop_image.png"
    im_crop.save(url_crop)
    color_ref = get_colors(url_crop)
    image_dict, fig, fig2 = create_image_entry(color_ref, f'coord_{left}_{top}_{right}_{bottom}')

    return im_crop, image_dict, fig, fig2
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


if __name__ == '__main__':
    pass