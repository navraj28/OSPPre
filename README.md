# OSPP (Open Source Parts Prediction) largely inspired by Aquant.io's Smart Triage & Parts Prediction
[A short read-up on Medium is here.](https://medium.com/@navraj28/parts-prediction-given-the-problem-description-6767c3d7e8ed) 

This is an attempt at Reverse engineering Aquant.io's Smart Triage Feature. It is a solution that uses AI to assist a Call Center Agent in the Field Service Domain, in trouble shooting a Problem based on reported issues & also recommends what Parts are required to fix the issue. It uses Spacy to parse the Problem Description & extract details. It uses TensorFlow Universal Sentence Encoder to eliminate duplicate symptoms i.e. "Battery is dead" is the same as "Battery needs to be replaced". Basically, unstructured text ends up as structured entities in a relational database.

Below images illustrate the concepts:

![alt text](https://github.com/navraj28/aquant/blob/master/Aquant1.png)
![alt text](https://github.com/navraj28/aquant/blob/master/Aquant2.png)
## Spacy is used to identify the main entities & related problems
![alt text](https://github.com/navraj28/aquant/blob/master/spacy.jpg)
![alt text](https://github.com/navraj28/aquant/blob/master/Aquant3.png)
## TensorFlow's Universal Sentence Encode is used for Semantic comparison and elimination of Duplicates.
![alt text](https://github.com/navraj28/aquant/blob/master/Aquant4.png)
![alt text](https://github.com/navraj28/aquant/blob/master/Aquant5.png)

# Parts Prediction Flow
#### Now that the data is imported into Relational database, Predicting Parts - either via Symptoms or full Problem Description is trivial
##### Predicting via actual Problem Description - Identify Root Symptoms & then query DB
![alt text](https://github.com/navraj28/aquant/blob/master/PredictionFlow1.png)
##### Predicting via Symptom Co-occurence, just the queries are different
