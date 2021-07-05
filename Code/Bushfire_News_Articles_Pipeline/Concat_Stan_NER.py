#This code will take in a number of txt files and extract LOCATIONS, and print the filename in column 0 of csv
#and print LOCATION in column 2

import os
from pickle import NONE
import nltk
import csv
import time

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

st = StanfordNERTagger(os.path.normpath(
    '/Users/fiannualamorgan/Documents/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz'),
    os.path.normpath(
        '/Users/fiannualamorgan/Documents/stanford-ner-2020-11-17/stanford-ner.jar')) #As before make sure these link to your local versions of the libaries

textdirectory = (os.path.normpath("/Users/fiannualamorgan/Documents/GitHub/Text_to_Test_for_Hugh/The_Golden_South_NER_Test/")) #You need to keep your TEXTS in wherever this folder is - you can set it on your computer
csvdirectory = (os.path.normpath("/Users/fiannualamorgan/Documents/GitHub/Text_to_Test_for_Hugh/The_Golden_South_NER_Test/Output/")) #Okay, so you need to make this folder in your PROJECT directory before you start!

def textcheck(filename):
    start = time.time()
    print("Working on | ",filename)
    textlocation = (os.path.normpath(os.path.join(textdirectory,filename))) # sets the specific path for the 'filename' which is basically working through a list of everything that is in the folder
    text = open(textlocation, encoding='utf-8').read()

    textfilename = os.path.basename(textlocation)

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)

    entities = [] #this means entities, not locations
    p_item = ('gibberish', '-1') # ('New South Wales': 'LOCATION') (of, )


    for i in classified_text:
        if p_item[1] != '-1' and i[1] != p_item[1] and p_item[1] != 'O':
         # Returning only named entities!
            entities.append(p_item) 
        if p_item[1] != 'O' and p_item[1] != '-1' and p_item[1] == i[1]:
            p_item = (p_item[0] + ' ' + i[0], i[1])
            continue
        p_item = i 
    if p_item[1] != 'O':
        entities.append(p_item) 
        
        
    plusfile = [xs + (textfilename,) for xs in entities] #this adds the FILEName into the CSV file

    #print(locations)

    with open(os.path.normpath(os.path.join(csvdirectory,filename + ".csv")), 'w') as f: #Writing these to a CSV file that has the same name as the text file
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerows(plusfile)
    end = time.time()
    print("Time elapsed | ", round(end - start,2),"seconds")
    print("CSV written")


def startup(): #gets all the file names of the TEXT file and works through each of them iteratively
    for file in os.listdir(textdirectory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            #print(filename)
            textcheck(filename)
            continue
        else:
            pass

startup()
