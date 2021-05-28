import os
import nltk
import pandas as pd
import csv


from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

# set directory for classifiers
st = StanfordNERTagger(os.path.normpath(
    '/Users/fiannualamorgan/Documents/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz'),
    os.path.normpath(
        '/Users/fiannualamorgan/Documents/stanford-ner-2020-11-17/stanford-ner.jar'))

# open directory with text files
directory = (os.path.normpath('/Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/output/Bushfire_News_Articles/text_Bushfire_News_Articles/'))

# establish list of locations (not sure if this makes sense)
locations = []

# iterate over files in that directory and run classifier
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
    # open file and run classifier
        text = open(f).read()
        tokenized_text = word_tokenize(text)
        classified_text = st.tag(tokenized_text)
    
#implement rule here?
    

        

