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
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    current_stage = df['data.regularSchedules.nodes'].tolist()
    current_stage = current_stage[0][0]
    start_time = datetime.strptime(current_stage['startTime'], "%Y-%m-%dT%H:%M:%SZ")
    start_time = start_time.replace(tzinfo=timezone.utc)  # convert time to utc

    end_time = datetime.strptime(current_stage['endTime'], "%Y-%m-%dT%H:%M:%SZ")
    end_time = end_time.replace(tzinfo=timezone.utc)  # convert time to utc
    end_timestamp = int(end_time.timestamp())

    print(f'end_timestamp: {end_timestamp}')
    print(f'start: {start_time}, end: {end_time}')
    stage1 = current_stage['regularMatchSetting']['vsStages'][0]['name']
    print(stage1)
    print(current_stage)


def get_json(url: str) -> pd.DataFrame:
    """
    returns a string of json data retrieved from the given url
    :param url: the url to retrieve json data from
    :return: string of json data
    """
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})

    response = urlopen(request_site)
    data_json = json.loads(response.read())
    # print(data_json)
    df = pd.json_normalize(data_json)
    df = df[['data.regularSchedules.nodes']].copy()
    return df


if __name__ == "__main__":
    main()
