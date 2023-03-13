import requests
import json
import pandas as pd
from typing import List, Dict
pd.options.mode.chained_assignment = None  # default='warn'

api_key = "3d6b75e2-6d88-47bc-af9c-08ba88093c56"

term_search = "sono"
items_per_page = 100

api_url = "https://api.company-information.service.gov.uk/search/companies?q=" \
        + term_search + "&items_per_page=" + str(items_per_page)

result: List[str] = []

# loop to create full response
for start_index in range(0, 1000, 100): # review this
    # use if start_index < total_results to prevent over looping?

    url = api_url + "&start_index=" + str(start_index)

    response = requests.get(url, auth=(api_key, ''))
    json_result = response.json()

    result = result + json_result['items'] # append all results with the previous to create one master result

# TRANSFORMATIONS
df = pd.json_normalize(result) # convert to dataframe for ease of analysis
df['date_of_cessation'] = pd.to_datetime(df['date_of_cessation'], format='%Y-%m-%d') # convert date columns from str to datetime
df['date_of_creation']  = pd.to_datetime(df['date_of_creation'], format='%Y-%m-%d')


# output to json file for reference to data
# with open('data.json', 'w') as outfile:
#     json.dump(result, outfile, indent=3, sort_keys=True)


######### ANSWERS #########
# 1. How many companies are there which match the search term “sono”?
q1 = len(result)
print(f"{q1} companies match the search term \"{term_search}\".\n")

# 2. Of these how many are active?
q2 = df.loc[df['company_status'] == 'active'].shape[0]
print(f'There are {q2} active.\n')

# 3. Of those dissolved what is the average life of the company (incorporation date to cessation date) in days? 
dissolved_df = df.loc[df['company_status'] == 'dissolved']
dissolved_df['company_lifespan'] = (dissolved_df['date_of_cessation'] - dissolved_df['date_of_creation']).dt.days
q3 = round(dissolved_df['company_lifespan'].mean())
print(f'Average life of dissolved companies is {q3} days.\n')

# 4. When was the first limited-partnership created? 
lp_df  = df.loc[df['company_type'] == 'limited-partnership']
q4 = lp_df['date_of_creation'].min().strftime('%Y-%m-%d')
print(f'The first limited-partnership was created in {q4}.\n')

# 5. Which companies also have “vate” in their title? 
q5df = df.loc[df['title'].str.contains('vate', case=False)]
q5 = q5df['title'].values.tolist()
print(f"The following companies also have \"vate\" in their title: {', '.join(str(x) for x in q5)}.\n")

# 6. Taking the digits from the premises part of the address to make a number for each company
# (e.g. 6-8 = 68, 14b = 14, 1 st Floor 45 Main St= 145 etc) what is the sum for each company type?
q6df = df
q6df['address.premises'] = df['address.premises'].str.replace('\D', '', regex=True) # remove all character for premises
q6df['address.premises'] = pd.to_numeric(df['address.premises']).astype('Int64') # convert string to int
q6df = q6df.groupby('company_type')['address.premises'].sum() # group by compant type then find the sum of each

q6 = q6df.to_dict()

print(f"The sum for each company type is the following: {q6}.")
