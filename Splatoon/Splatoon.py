import json
from io import BytesIO
from typing import NamedTuple
from urllib import request
from urllib.request import Request, urlopen
import pandas as pd
from datetime import datetime, timezone
import discord

import requests
from PIL import Image

"""
Python tool to get splatoon data schedule data from the web
"""


def main():
    img1 = "https://splatoon3.ink/assets/splatnet/v1/stage_img/icon/low_resolution/f14c2a64e49d243679fc0884af91e1a07dc65600f9b90aefe92d7790dcffb191_1.png"
    img2 = "https://splatoon3.ink/assets/splatnet/v1/stage_img/icon/low_resolution/a8ba96c3dbd015b7bc6ea4fa067245c4e9aee62b6696cb41e02d35139dd21fe7_1.png"
    merged_img = merge_images(img1, img2)
    return merged_img


def merge_images(img1_url: str, img2_url: str):
    img1 = create_pil_image_from_url(img1_url)
    img2 = create_pil_image_from_url(img2_url)
    new_image = Image.new('RGB', (2 * img1.size[0]+10, img1.size[1]), (0, 0, 0))
    new_image.paste(img1, (0, 0))
    new_image.paste(img2, (img1.size[0]+10, 0))
    return new_image


def create_pil_image_from_url(url: str) -> Image.Image:
    response = requests.get(url)
    image_data = response.content
    pil_image = Image.open(BytesIO(image_data))
    return pil_image


class Stage(NamedTuple):
    """class that represents a splatoon stage"""
    start_time: int
    end_time: int
    name: str
    img: str

    def __str__(self) -> str:
        return f'<t:{self.start_time}:t>-<t:{self.end_time}:t>\n{self.name}\n{self.img}\n'


def get_cur_regular_stages() -> list:
    """
    gets the current regular stage information from the web
    :return: regular stage information as a list of stages
    """
    df = get_json("https://splatoon3.ink/data/schedules.json")
    current_stages = df['data.regularSchedules.nodes'].tolist()
    current_stages = current_stages[0][0]
    vals: dict = get_stage_values_dict(current_stages)
    stage_1 = Stage(vals['start_time'], vals['end_time'], vals['stage1_name'], vals['stage1_image'])
    stage_2 = Stage(vals['start_time'], vals['end_time'], vals['stage2_name'], vals['stage2_image'])
    return [stage_1, stage_2]


def get_stage_values_dict(current_stages: pd.DataFrame) -> dict:
    """
    returns a dictionary containing the stage information from the given dataframe
    :param current_stages:
    :return: dictionary containing the stage information
    """
    # beginning unix timestamp
    start_time = datetime.strptime(current_stages['startTime'], "%Y-%m-%dT%H:%M:%SZ")
    start_time = start_time.replace(tzinfo=timezone.utc)  # convert time to utc
    start_timestamp = int(start_time.timestamp())

    # ending unix timestamp
    end_time = datetime.strptime(current_stages['endTime'], "%Y-%m-%dT%H:%M:%SZ")
    end_time = end_time.replace(tzinfo=timezone.utc)  # convert time to utc
    end_timestamp = int(end_time.timestamp())

    stages = current_stages['regularMatchSetting']['vsStages']
    stage1 = stages[0]
    stage2 = stages[1]

    stage1_name = stage1['name']
    stage1_image = stage1['image']['url']

    stage2_name = stage2['name']
    stage2_image = stage2['image']['url']

    dictionary = {'start_time': start_timestamp, 'end_time': end_timestamp, 'stage1_name': stage1_name,
                  'stage1_image': stage1_image, 'stage2_name': stage2_name, 'stage2_image': stage2_image}
    return dictionary


def get_json(url: str) -> pd.DataFrame:
    """
    returns a string of json data retrieved from the given url
    :param url: the url to retrieve json data from
    :return: string of json data
    """
    request_site = Request(url, headers={"User-Agent": "me@marinaflynne.com"})

    response = urlopen(request_site)
    data_json = json.loads(response.read())
    # print(data_json)
    df = pd.json_normalize(data_json)
    df = df[['data.regularSchedules.nodes']].copy()
    return df


if __name__ == "__main__":
    main()
