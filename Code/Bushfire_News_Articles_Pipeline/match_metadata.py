#this script allows me to load in information from other stories

import pandas as pd
import time

entities_df = pd.read_csv('/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/Sections/Bushfire_News_Articles_19th_Century/Transformed_Data/Geocoded_LOCATION_Mappify_API/Transformed/Mappify_Results_Fuzzy_Wuzzy_Validation/cleaned_mappify_perfect_results.csv')
metadata_df = pd.read_csv('/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/Sections/Bushfire_News_Articles_19th_Century/19th_Century_Bushfire_Articles.csv')

merged_df = entities_df.set_index('article_id').join(metadata_df.set_index('article_id'))

# merged_df.rename({'Unnamed: 0': 'article_id'}, axis=1, inplace=True)

merged_df.to_csv('/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/Sections/Bushfire_News_Articles_19th_Century/merged_placenames_metadata_articles.csv', index=False)




