Readme.md   
All articles in 19th century regarding bushfires to run NER. 
making changes INITIAL COMMOIT

#working from within the NER directory this is the command that works. 
java -mx600m -cp "*:lib/*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -outputFormat tabbedEntities -textFile sample.txt>sample.tsv



-outputDirectory 
cannot batch!
