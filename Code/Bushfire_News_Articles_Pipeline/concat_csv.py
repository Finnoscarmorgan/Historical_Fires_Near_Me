
import os
import pandas as pd

path = '/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/output/Bushfire_News_Articles/Fuzzy_Output/Test_Extraction_NER_Output/'
# path = '/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/output/Bushfire_News_Articles/Bushfire_Extracts/Extraction_NER_Output/Test_NER_Output/'
out_folder = '/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/output/Bushfire_News_Articles/Fuzzy_Output/Test_Extraction_NER_Output/Output/'

master_df = pd.DataFrame()

for file in os.listdir(path):
    check_file = os.path.getsize(path + file)
    if check_file == 0:
        continue
    if file == '.DS_Store':
        continue
    if file == 'Output':
        continue
    data_to_add = pd.read_csv(path + file, header = None)
    master_df = pd.concat([master_df, data_to_add])
        

master_df.to_csv(out_folder + "complete_output.csv", index=False)
#print(master_df)
"""
merge = []

# find all files bigger than 0 bytes and read as df
for root, dirs, files in os.walk(path):
  for name in files:
    filename = os.path.join(root, name)
    if os.stat(filename).st_size > xsize:
        merge.append(pd.read_csv(filename))

result = pd.concat([merge], , join='outer', ignore_index=False)


dfs = []
for filename in filenames:
    dfs.append(pd.read_csv(filename))



    df = pd.read_csv(filename)
"""
