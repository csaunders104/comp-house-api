import requests
import json
import os.path
import pandas as pd
import globals as g
from decouple import config
from typing import List


class DataManipulation:

    def read_from_api(self) -> List[str]:
        '''Reads data from api'''

        api_key: str = config("api_key", default = "")
        result: List[str] = [] # init json result var

        # loop to create full response
        for start_index in range(0, 1000, 100): # max range is 1000 as max start_index value is 999

            url = g.api_url + "&start_index=" + str(start_index)

            response = requests.get(url, auth=(api_key, ''))
            json_result = response.json() # convert response into readable json

            # append all results with the previous to create one master result
            result = result + json_result['items']

        return result

    def read_from_csv(self) -> pd.DataFrame:
        '''Reads data from csv file to save time'''

        df = pd.read_csv(g.csv_file)

        return df

    def json_to_df(self, result: List[str]) -> pd.DataFrame:
        '''Convert json result into dataframe'''
        '''Extra search for term made'''

        df = pd.json_normalize(result) # convert to dataframe for ease of analysis

        # extra search for "sono" as API result gives all companies that previously had company name
        # with term "sono" but also companies such as S.O.N.O.S which does not fit question
        df = df.loc[df['title'].str.contains(g.term_search, case=False)]

        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        '''Transformations to date are done here'''

        # convert relevant date columns from str to datetime
        df['date_of_cessation'] = pd.to_datetime(df['date_of_cessation'], format='%Y-%m-%d')
        df['date_of_creation']  = pd.to_datetime(df['date_of_creation'], format='%Y-%m-%d')

        return df

    def output_csv(self, df: pd.DataFrame) -> None:
        '''Output dataframe to csv'''
        df.to_csv(g.csv_file, index=False, header=True)

    def handler_file_not_exists(self) -> pd.DataFrame:
        '''Handles part of code if csv file does NOT exist'''
        result = self.read_from_api() # read from api
        df = self.json_to_df(result)  # convert json result into dataframe
        df = self.transform(df)       # transform dataframe data
        self.output_csv(df)           # outputs datframe to csv for future reference

        return df

    def handler_file_exists(self) -> pd.DataFrame:
        '''Handles part of code if csv file does exist'''
        df = self.read_from_csv() # read from csv file
        df = self.transform(df)   # transform dataframe data

        return df


def handler() -> pd.DataFrame:
    file_exists: bool = os.path.exists(g.csv_file)

    # checks if csv file exists then chooses appropriate handler
    if file_exists is False:
        df = DataManipulation().handler_file_not_exists()
    if file_exists is True:
        df = DataManipulation().handler_file_exists()
    
    return df