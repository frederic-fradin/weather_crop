from PIL import Image, ImageDraw
import requests
import cv2
import extcolors
import os
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import date, datetime, timedelta


def_url = "https://www.worldagweather.com/fcstwx/tmp_gefs_day7_in_metric_2440.png"

os.environ["OMP_NUM_THREADS"] = "2"

color_legend = {
    "rgb(255,0,201)": 10,
    "rgb(255,0,0)": 8,
    "rgb(255,110,0)": 6,
    "rgb(255,160,0)": 4,
    "rgb(255,210,0)": 2,
    "rgb(255,255,0)": 1,
    "rgb(0,255,255)": -1,
    "rgb(0,180,255)": -2,
    "rgb(0,80,255)": -4,
    "rgb(0,0,211)": -6,
    "rgb(0,0,161)": -8,
    "rgb(60,0,120)": -10,
}

color_excluded = [
    "rgb(200,200,200)",
    "rgb(255,255,255)",
    "rgb(72,108,139)",
    "rgb(51,51,0)",
    "rgb(167,167,0)",
]


def get_colors(img_path):
    img = Image.open(img_path).convert("RGBA")
    return extcolors.extract_from_image(img, tolerance=25, limit=5)


def get_size(img_path):
    im = Image.open(requests.get(img_path, stream=True).raw)
    width = im.width
    height = im.height

    return (width, height)


def create_chart(df):

    # Create the bar chart
    pvt1 = pd.pivot_table(
        data=df[(df["percent"] != 0) & (df["date"] == df["date"].max())].copy(),
        aggfunc="sum",
        index="colorCode",
        values="percent",
        fill_value=0,
    ).reset_index()
    fig1 = px.bar(
        pvt1,
        x="colorCode",
        y="percent",
        color="colorCode",
        text="percent",
        color_discrete_sequence=pvt1["colorCode"],
        width=1080,
        height=480,
        text_auto=True,
    )

    fig1.update_layout(showlegend=False, yaxis_title=None, xaxis_title=None)
    fig1.update_traces(marker_line_color="rgb(200,200,200)", marker_line_width=1)

    # Create the line chart
    pvt2 = pd.pivot_table(
        data=df[df["score"] != 0],
        aggfunc="sum",
        index="date",
        values="score",
        fill_value=0,
    ).reset_index()

    fig2 = px.line(pvt2, x="date", y="score", width=1080, height=480)
    fig2.add_hline(y=8, line_width=1, line_color="rgb(255, 0, 0)", line_dash="dash")
    fig2.add_hline(y=4, line_width=1, line_color="rgb(255, 160, 0)", line_dash="dash")
    fig2.add_hline(y=2, line_width=1, line_color="rgb(255, 210, 0)", line_dash="dash")
    fig2.add_hline(y=-2, line_width=1, line_color="rgb(0, 255, 255)", line_dash="dash")
    fig2.add_hline(y=-4, line_width=1, line_color="rgb(0, 180, 255)", line_dash="dash")
    fig2.add_hline(y=-8, line_width=1, line_color="rgb(0, 0, 211)", line_dash="dash")

    return fig1, fig2


def crop_image(
    url: str, left: int, top: int, right: int, bottom: int, date: date, place: str
) -> object:
    # Opens a image in RGB mode
    im = Image.open(requests.get(url, stream=True).raw)

    # Cropped image of above dimension
    im_crop = im.crop((left, top, right, bottom))

    # save a image using extension
    url_crop = "./reports/figures/crop_image.png"
    im_crop.save(url_crop)
    img = Image.open(url_crop)

    # Identify main colors
    colors, pixel_count = extcolors.extract_from_image(img, tolerance=20, limit=5)
    flattened_data = [(rgb[0], rgb[1], rgb[2], value) for rgb, value in colors]
    df = pd.DataFrame(flattened_data, columns=["Red", "Green", "Blue", "Value"])
    df["colorCode"] = df.apply(
        lambda x: "rgb("
        + str(x["Red"])
        + ","
        + str(x["Green"])
        + ","
        + str(x["Blue"])
        + ")",
        axis=1,
    )
    df["pixels"] = pixel_count
    df["percent"] = df.apply(
        lambda row: (
            round(row["Value"] / row["pixels"], 4) * 100 if row["pixels"] != 0 else 0
        ),
        axis=1,
    )
    df["score"] = df["colorCode"].map(color_legend) * (df["percent"] / 100)

    df["date"] = date
    df["place"] = place
    df["left"] = left
    df["right"] = right
    df["top"] = top
    df["bottom"] = bottom

    df = df[(~df["colorCode"].isin(color_excluded))].copy()

    return im_crop, df


def add_rectangle(url: str, left: int, top: int, right: int, bottom: int):
    im = Image.open(requests.get(url, stream=True).raw).convert("RGBA")

    shape = [(left, top), (right, bottom)]

    # create  rectangleimage
    img1 = ImageDraw.Draw(im)
    img1.rectangle(shape, fill=None, outline="red", width=3)

    return im


def generate_date_serie(start_date: date, end_date: date, step: int):

    # List to hold the series of dates
    date_serie = [end_date]

    # Generate the date series, excluding weekends
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 4:  # 0-4 are Monday to Friday
            date_serie.append(current_date)  # Append the date (without time)
        current_date += timedelta(days=1)  # Move to the next day

    # filtered_date_serie = [date for index, date in enumerate(date_serie) if index % step == 0]

    return date_serie


if __name__ == "__main__":
    pass
