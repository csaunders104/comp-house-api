import requests
import json
import pandas as pd
import globals as g
from decouple import config
from typing import List


def read_from_api() -> pd.DataFrame:
    '''Reads data from api'''

    api_key: str = config("api_key", default = "")
    result: List[str] = []

    # loop to create full response
    for start_index in range(0, 1000, 100): # review this

        url = g.api_url + "&start_index=" + str(start_index)

        response = requests.get(url, auth=(api_key, ''))
        json_result = response.json()

        # append all results with the previous to create one master result
        result = result + json_result['items']

    # output to json file for reference to data
    with open('data.json', 'w') as outfile:
        json.dump(result, outfile, indent=3, sort_keys=True)

    df = transform(result)

    return df

def read_from_json() -> pd.DataFrame:
    '''Reads data from json file to save time'''

    file = open('data.json') # replace path to variable in .env
    # returns JSON object as dictionary
    result = json.load(file)

    df = transform(result)

    return df

def transform(result: List[str]) -> pd.DataFrame:
    df = pd.json_normalize(result) # convert to dataframe for ease of analysis

    # convert date columns from str to datetime
    df['date_of_cessation'] = pd.to_datetime(df['date_of_cessation'], format='%Y-%m-%d')
    df['date_of_creation']  = pd.to_datetime(df['date_of_creation'], format='%Y-%m-%d')

    return df