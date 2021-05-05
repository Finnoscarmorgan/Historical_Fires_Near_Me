import os
import nltk
# import pandas as pd #No idea why these don't import on my machine :(
# import numpy as np #No idea why these don't import on my machine :(
import csv
import time

#TRY DELETING THE BELOW TWO LINES FIRST!!!!!!
# java_path = os.path.normpath("C:/Program Files/Java/jre1.8.0_291/bin/java.exe") #Change the local path for JAVA
# os.environ['JAVAHOME'] = java_path #You might need to delete this - I just added this because JAVE RTE wasn't on my computer

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

st = StanfordNERTagger(os.path.normpath(
    '/Users/fiannualamorgan/Documents/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz'),
    os.path.normpath(
        '/Users/fiannualamorgan/Documents/stanford-ner-2020-11-17/stanford-ner.jar')) #As before make sure these link to your local versions of the libaries

textdirectory = (os.path.normpath("/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/Test_Folder/")) #You need to keep your TEXTS in wherever this folder is - you can set it on your computer
csvdirectory = (os.path.normpath("/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/Test_Folder/CSVOutput")) #Okay, so you need to make this folder in your PROJECT directory before you start!

def textcheck(filename):
    start = time.time()
    print("Working on | ",filename)
    textlocation = (os.path.normpath(os.path.join(textdirectory,filename))) #sets the specific path for the 'filename' which is basically working through a list of everything that is in the folder
    text = open(textlocation, encoding='utf-8').read()

    textfilename = os.path.basename(textlocation)

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)

    locations = []

    for i in classified_text:
        if i[1] != 'O':  # Returning only named entities!
            locations.append(i)

    plusfile = [xs + (textfilename,) for xs in locations] #this adds the FILEName into the CSV file

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
