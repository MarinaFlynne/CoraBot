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
    get_cur_stages("regular")
    # type = "anarchy"
    # df: pd.DataFrame = get_json("https://splatoon3.ink/data/schedules.json")
    # # print(df)
    # # print(df['data'].tolist())
    # # print(df)
    # if type == "regular":
    #     current_stages = df['data.regularSchedules.nodes'].tolist()
    # elif type == "anarchy":
    #     current_stages = df['data.regularSchedules.nodes']
    # else:
    #     raise Exception(f"type {type} is an invalid type.")

def merge_images(img1_url: str, img2_url: str):
    img1 = create_pil_image_from_url(img1_url)
    img2 = create_pil_image_from_url(img2_url)
    new_image = Image.new('RGB', (2 * img1.size[0] + 10, img1.size[1]), (0, 0, 0))
    new_image.paste(img1, (0, 0))
    new_image.paste(img2, (img1.size[0] + 10, 0))
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


def get_cur_stages(type: str) -> list:
    """
    gets the current regular stage information from the web
    :param type: the type of stage
    :return: stage information as a list of stage objects
    """
    df: pd.DataFrame = get_json("https://splatoon3.ink/data/schedules.json")
    thumbnail = ''
    title = ''
    if type == "regular":
        current_stages = df['data.regularSchedules.nodes'].tolist()
        thumbnail = 'https://www.seekpng.com/png/detail/41-416602_splatoon-turf-war-symbol.png'
        title = 'Regular Battle'
    elif type == "anarchy":
        current_stages = df['data.bankaraSchedules.nodes'].tolist()
        thumbnail = 'https://www.pngkit.com/png/detail/41-416320_make-your-rep-in-ranked-battles-ranked-battle.png'
        title = 'Anarchy Battle (Open)'
    else:
        raise Exception(f"type {type} is an invalid type.")
    current_stages = current_stages[0][0]
    vals: dict = get_stage_values_dict(current_stages, type)
    stage_1: Stage = Stage(vals['start_time'], vals['end_time'], vals['stage1_name'], vals['stage1_image'])
    stage_2: Stage = Stage(vals['start_time'], vals['end_time'], vals['stage2_name'], vals['stage2_image'])
    mode: str = vals['mode']
    return [stage_1, stage_2, mode, thumbnail, title]


def get_stage_values_dict(current_stages: pd.DataFrame, type: str) -> dict:
    """
    returns a dictionary containing the stage information from the given dataframe
    :param type: the type of stage
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

    # extract the stages values depending on the type
    if type == "regular":
        vs_stages = current_stages['regularMatchSetting']['vsStages']
        vs_rule = current_stages['regularMatchSetting']['vsRule']
    elif type == "anarchy":
        vs_stages = current_stages['bankaraMatchSettings'][0]['vsStages']
        vs_rule = current_stages['bankaraMatchSettings'][0]['vsRule']
    else:
        raise Exception(f"stage type {type} is an invalid stage type.")

    mode = vs_rule['name']

    stage1 = vs_stages[0]
    stage2 = vs_stages[1]

    stage1_name = stage1['name']
    stage1_image = stage1['image']['url']

    stage2_name = stage2['name']
    stage2_image = stage2['image']['url']

    dictionary = {'start_time': start_timestamp, 'end_time': end_timestamp, 'stage1_name': stage1_name,
                  'stage1_image': stage1_image, 'stage2_name': stage2_name, 'stage2_image': stage2_image, 'mode': mode}
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
    # df = df[['data.regularSchedules.nodes']].copy()
    return df


if __name__ == "__main__":
    main()
