# spacy_ner_relation
This Binary Converter will work for data annotated with Label studio for relation extraction


---> rel_trf_cfg --TRANSFORMER CONFIG FILE CONSIST OF ADDITIONAL COMPONENTS TO TRAIN NER AND RELATION. USE ONLY THIS CONFIG TO TRAIN NER AND RELATION

----> image present in the repository shows the changes need to be done is rel_pipe.py file when you start training ner + relation together. Otherwise it will throw error of nlp.evaluate()

----> ner+relation.ipynb file has all the training steps for ner and relation together with prediction.

----> If you want to convert your data into spacy formate when you got your data annotated from label studio then use spacy_formate_converter.py file

----> follow the steps mentioned in the link to moves files in respective folders and to add data path to project.yaml file 

Link: https://towardsdatascience.com/how-to-train-a-joint-entities-and-relation-extraction-classifier-using-bert-transformer-with-spacy-49eb08d91b5c
