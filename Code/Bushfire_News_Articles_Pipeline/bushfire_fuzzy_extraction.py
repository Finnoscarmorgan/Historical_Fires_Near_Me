import re
import os
import fuzzysearch as fs
import attr

# test article that contains mention of one bush-fire '/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/output/Bushfire_News_Articles/text_Bushfire_News_Articles/18331221-6-641728.txt'
# test article that contains mention of two bush-fires ('/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/code/sample_bushfire_text.txt')

folder = '/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/Sections/Bushfire_News_Articles_19th_Century/Source_Data/text_Bushfire_News_Articles/'
outfolder = '/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/Sections/Bushfire_News_Articles_19th_Century/Generated_Data/Fuzzy_Output_200_Characters/' #cannot be in same directory as folder, must be adjacent 

file_counter = 0 

for path in os.listdir(folder):
    f = open (folder + path,'r', encoding='utf-8')
    #f = open ('/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/output/Bushfire_News_Articles/text_Bushfire_News_Articles/18351121-6-640652.txt','r', encoding='utf-8')
    print(path)
    if path == '.DS_Store':
        continue

    file_counter = file_counter + 1 
    text = f.read()

    #max_l_dist is the maximum levenshtein distance between the string you're looking for and those found in
    #text you're searching. It is just the number of character swaps, insertions or deletions allowed before
    #you consider it not to be the same word - e.g. bush-fire and bushfire have a distance of 1, bushfire and
    #busgfire should have a distance of 2. This is the setting you need to change (only accepts whole integers) 
    #to make the search more or less strict. You can also specify the maximum tolerance for substitutions, deletions
    #and insertions alongside the max_l_dist if you want to make it more precise given patterns you have seen in the text,
    #but this should work just fine. Keeping in mind that it considers upper and lower case characters to be different, 
    #so just write any word you want to search in lower case and convert the text you are searching to lower case with the
    # this_text.lower() method
    matches = fs.find_near_matches('bushfire', text.lower(), max_deletions=1, max_insertions=1, max_l_dist=2, max_substitutions=1)
    numMatch=len(matches)
    index=1


    for m in matches:
        of = open(outfolder + path[0:-4] + ' (' +str(index) + ' of ' + str(numMatch) + ')'+path[-4:], 'w')
        of.write(text[max(0, m.start-608):min(len(text), m.start+608)])
        index=index+1
        
    of.close()
    
print(file_counter)
    
#bushfire
#bushfires
#bush-fire
#bush-fires
#bush fire
#bush fires


#locate index of 'bush-fire' in text
#bushfire_index = text.find("bush-fire")
# turn index location into a string to establish extraction range
#range_2 = (int(bushfire_index) + 608)
#use bushfire_index and range_2 location to extract 600 characters and establish second half of extraction.
#extract_2 = text[bushfire_index:range_2]
#find range_1 - the first half of the extraction
#range_1 = (int(bushfire_index) - 608)
#use bushfire_index and range_2 location to extract 609 (should match up) characters 
#extract_1 = text[range_1:bushfire_index]
#extract = str(extract_1 + extract_2)

# write to new text file with appended .extract
# if more than one mention append .extract2 (increasing if more)







"""
constraints: 
- each mention of bushfire needs to be turned into its own file. Two mentions in one article means two files with similar filenames? (1 and 2)
- append onto file increasing integer?
"""
