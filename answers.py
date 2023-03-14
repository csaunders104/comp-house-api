import pandas as pd
import globals as g
from typing import List, Dict
pd.options.mode.chained_assignment = None  # suppress warning for q3

class Answers:
    '''Answers to all questions'''

    def q1(self, df: pd.DataFrame) -> int:
        # 1. How many companies are there which match the search term “sono”?
        a1 = df.shape[0]
        return a1

    def q2(self, df: pd.DataFrame) -> int:
        # 2. Of these how many are active?
        a2 = df.loc[df['company_status'] == 'active'].shape[0]
        return a2

    def q3(self, df: pd.DataFrame) -> int:
        # 3. Of those dissolved what is the average life of the company
        # (incorporation date to cessation date) in days? 
        dissolved_df = df.loc[df['company_status'] == 'dissolved']
        dissolved_df['company_lifespan'] = (dissolved_df['date_of_cessation']
                                            - dissolved_df['date_of_creation']).dt.days
        a3 = round(dissolved_df['company_lifespan'].mean())
        return a3

    def q4(self, df: pd.DataFrame) -> str:
        # 4. When was the first limited-partnership created? 
        lp_df  = df.loc[df['company_type'] == 'limited-partnership']
        a4 = lp_df['date_of_creation'].min().strftime('%Y-%m-%d')
        return a4

    def q5(self, df: pd.DataFrame) -> List[str]:
        # 5. Which companies also have “vate” in their title? 
        a5df = df.loc[df['title'].str.contains('vate', case=False)]
        a5 = a5df['title'].values.tolist()
        return a5

    def q6(self, df: pd.DataFrame) -> Dict[str, str]:
        # 6. Taking the digits from the premises part of the address to 
        # make a number for each company (e.g. 6-8 = 68, 14b = 14, 1 st
        # Floor 45 Main St= 145 etc) what is the sum for each company type?
        a6df = df
        # remove all character for premises
        a6df['address.premises'] = df['address.premises'].str.replace('\D', '', regex=True)
        # convert string to int
        a6df['address.premises'] = pd.to_numeric(df['address.premises']).astype('Int64')
        # group by compant type then find the sum of each
        a6df = a6df.groupby('company_type')['address.premises'].sum()
        a6 = a6df.to_dict() # convert from dataframe to dict
        return a6

    def collate_answers(self, df: pd.DataFrame):
        print(f"{self.q1(df)} companies match the search term \"{g.term_search}\".\n")
        print(f'There are {self.q2(df)} active.\n')
        print(f'Average life of dissolved companies is {self.q3(df)} days.\n')
        print(f'The first limited-partnership was created in {self.q4(df)}.\n')
        print(f"The following companies also have \"vate\" in their title: {', '.join(str(x) for x in self.q5(df))}.\n")
        print(f"The sum for each company type is the following: {self.q6(df)}.")