import pandas as pd
import globals as g
from typing import List, Dict
pd.options.mode.chained_assignment = None  # suppress warning for q3

class CalculateAnswers:
    '''Answers all questions'''

    def q1(self, df: pd.DataFrame) -> int:
        # 1. How many companies are there which match the search term “sono”?
        a1 = df.shape[0] # number of dataframe rows will equal number of companies with "sono"
        return a1

    def q2(self, df: pd.DataFrame) -> int:
        # 2. Of these how many are active?
        a2 = df.loc[df['company_status'] == 'active'].shape[0] # number of rows with filter for active companies
        return a2

    def q3(self, df: pd.DataFrame) -> int:
        # 3. Of those dissolved what is the average life of the company
        # (incorporation date to cessation date) in days? 
        dissolved_df = df.loc[df['company_status'] == 'dissolved'] # filter for dissolved companies
        dissolved_df['company_lifespan'] = (dissolved_df['date_of_cessation']
                                            - dissolved_df['date_of_creation']).dt.days # calculate company lifespan
        a3 = round(dissolved_df['company_lifespan'].mean()) # find average value of company lifespan
        return a3

    def q4(self, df: pd.DataFrame) -> str:
        # 4. When was the first limited-partnership created? 
        lp_df  = df.loc[df['company_type'] == 'limited-partnership'] # filter for "limited-partnership" companies
        a4 = lp_df['date_of_creation'].min().strftime('%Y-%m-%d')    # find earliest date
        return a4

    def q5(self, df: pd.DataFrame) -> List[str]:
        # 5. Which companies also have “vate” in their title? 
        a5df = df.loc[df['title'].str.contains('vate', case=False)] # check company titles if they contain "vate"
        a5 = a5df['title'].values.tolist()
        return a5

    def q6(self, df: pd.DataFrame) -> Dict[str, str]:
        # 6. Taking the digits from the premises part of the address to 
        # make a number for each company (e.g. 6-8 = 68, 14b = 14, 1 st
        # Floor 45 Main St= 145 etc) what is the sum for each company type?
        a6df = df
        # remove all characters for premises
        a6df['address.premises'] = df['address.premises'].str.replace('\D', '', regex=True)
        # convert string to int for calculation
        a6df['address.premises'] = pd.to_numeric(df['address.premises']).astype('Int64')
        # group by company type then find the sum of each
        a6df = a6df.groupby('company_type')['address.premises'].sum()
        a6 = a6df.to_dict() # convert from dataframe to dict
        return a6


def collate_answers(df: pd.DataFrame) -> None:
    print(f"Q1: {CalculateAnswers().q1(df)} companies match the search term \"{g.term_search}\".\n")
    print(f'Q2: There are {CalculateAnswers().q2(df)} active.\n')
    print(f'Q3: Average life of dissolved companies is {CalculateAnswers().q3(df)} days.\n')
    print(f'Q4: The first limited-partnership was created in {CalculateAnswers().q4(df)}.\n')
    print(f"Q5: The following companies also have \"vate\" in their title: {', '.join(str(x) for x in CalculateAnswers().q5(df))}.\n")
    print(f"Q6: The sum for each company type is the following: {CalculateAnswers().q6(df)}.")