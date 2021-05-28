
# test article that contains mention of one bush-fire '/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/output/Bushfire_News_Articles/text_Bushfire_News_Articles/18331221-6-641728.txt'
# test article that contains mention of two bush-fires ('/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/code/sample_bushfire_text.txt')

# open bushfire article
f = open('/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/code/sample_bushfire_text.txt')
text = f.read()

for i in range:
#locate index of 'bush-fire' in text
    bushfire_index = text.find("bush-fire")
# turn index location into a string to establish extraction range
    range_2 = (int(bushfire_index) + 608)
#use bushfire_index and range_2 location to extract 600 characters and establish second half of extraction.
    extract_2 = text[bushfire_index:range_2]
#find range_1 - the first half of the extraction
    range_1 = (int(bushfire_index) - 608)
#use bushfire_index and range_2 location to extract 609 (should match up) characters 
    extract_1 = text[range_1:bushfire_index]
    extract = str(extract_1 + extract_2)
return(extract)




"""
constraints: 
- each mention of bushfire needs to be turned into its own file. Two mentions in one article means two files with similar filenames? (1 and 2)
- append onto file increasing integer?
"""
