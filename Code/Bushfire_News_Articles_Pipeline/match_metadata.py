#this script allows me to load in information from other stories

import pandas as pd
import time

entities_df = pd.read_csv('PATH_NAME')
metadata_df = pd.read_csv('PATH_NAME')

merged_df = entities_df.set_index('article_id').join(metadata_df.set_index('article_id'))
#merged_df.rename({'Unnamed: 0': 'article_id'}, axis=1, inplace=True)

merged_df.to_csv('PATH_NAME', index=False)

