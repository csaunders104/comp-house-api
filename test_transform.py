import pandas as pd
import numpy as np
from utils import DataManipulation

dm = DataManipulation()

test_data = {
            'date_of_creation': ['2015-05-02', '2015-08-11'],
            'date_of_cessation': ['2020-04-04','2020-06-04']
            }

test_df = pd.DataFrame.from_dict(test_data)
test_transform = dm.transform(test_df)

cessation_result = test_transform['date_of_cessation']
creation_result = test_transform['date_of_creation']

expected_result = np.datetime64('2023-01-01', 'ns')

assert cessation_result.dtype == expected_result.dtype
assert creation_result.dtype == expected_result.dtype