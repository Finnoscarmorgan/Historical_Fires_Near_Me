import re
import os
import fuzzysearch as fs
import attr


folder = 'FILE_NAME'
outfolder = 'FILE_NAME' #cannot be in same directory as folder, must be adjacent 

file_counter = 0 

for path in os.listdir(folder):
    f = open (folder + path,'r', encoding='utf-8')
    #f = open ('ADD_PATH_TO_TEXT_FILES_HERE.txt','r', encoding='utf-8')
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

