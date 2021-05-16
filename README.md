Readme.md   

This repository contains all the data required to build the Fires_Near_Me App.  Currently some data is held in another repository that will require export when it has been cleaned.
Currently held data are all articles in 19th century regarding bushfires and csv outputs with location of same material. 

# 6/5/2021
- NER has been run on all articles pertaining to bushfires and are located at /Users/fiannualamorgan/Documents/GitHub/Historical_Fires_Near_Me/data/1615182084/text/CSVOutput
# 5/5/2021 
Contents contain:
- all 5000 articles that mention bushfires derived from Trove across the 19th century. 
- script to extract NER using Stanford. 
- There is a "test folder" that needs to be removed, this was simply to make sure the script was working. 
# 16/5/2021
- ran 'Test_NER_Stanford.py' on 500 articles and produced output.


record of Fellowship Meetings:
- recommendations:
- produce script that collates placenames back together


# Running Stanford NER from the Command Line
# working from within the NER directory this is the command that works. 
java -mx600m -cp "*:lib/*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -outputFormat tabbedEntities -textFile sample.txt>sample.tsv
# to execute from the command line the following directory needs to be added to your classpath, commands below:
echo $CLASSPATH
:/Users/fiannualamorgan/Documents/stanford-ner-2020-11-17/stanford-ner.jar


