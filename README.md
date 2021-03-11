Readme.md   
<<<<<<< HEAD
All articles in 19th century regarding bushfires to run NER. 
making changes INITIAL COMMOIT

#working from within the NER directory this is the command that works. 
java -mx600m -cp "*:lib/*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -outputFormat tabbedEntities -textFile sample.txt>sample.tsv



-outputDirectory 
cannot batch!
=======
interface that approximates the Fires Near Me App with locations from the 19th century. 
>>>>>>> a33fd400189ff8554fc6496fe0db5859a9a1bedb


make sure this is on your class path

echo $CLASSPATH
:/Users/fiannualamorgan/Documents/stanford-ner-2020-11-17/stanford-ner.jar