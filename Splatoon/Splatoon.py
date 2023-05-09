import json
from urllib import request
from urllib.request import Request, urlopen
import pandas as pd
from datetime import datetime, timezone

"""
Python tool to get splatoon data schedule data from the web
"""


def main():
    df = get_json("https://splatoon3.ink/data/schedules.json")
    current_stages = df['data.regularSchedules.nodes'].tolist()
    current_stages = current_stages[0][0]
    stage_values: dict = get_stage_values_dict(current_stages)
    print(stage_values)


def get_cur_regular_stages() -> dict:
    """
    gets the current regular stage information from the web and returns it in a dictionary
    :return: regular stage information as a dictionary
    """
    df = get_json("https://splatoon3.ink/data/schedules.json")
    current_stages = df['data.regularSchedules.nodes'].tolist()
    current_stages = current_stages[0][0]
    stage_values: dict = get_stage_values_dict(current_stages)
    return stage_values


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
