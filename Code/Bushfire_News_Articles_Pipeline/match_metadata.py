#this script allows me to load in information from other stories

import pandas as pd
import time

entities_df = pd.read_csv('/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/Sections/Bushfire_Literature/Cleaned_Data/Bushfire_Literature_Input_Disambiguator_Output.csv')
metadata_df = pd.read_csv('/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/Sections/Bushfire_Literature/Cleaned_Data/Bushfire_Location_Spreadsheet_July_19.csv')

merged_df = entities_df.set_index('article_id').join(metadata_df.set_index('article_id'))
#merged_df.rename({'Unnamed: 0': 'article_id'}, axis=1, inplace=True)

merged_df.to_csv('/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/Sections/Bushfire_Literature/Cleaned_Data/Bushfire_Literature_Metadata_Disambiguated.csv', index=False)

