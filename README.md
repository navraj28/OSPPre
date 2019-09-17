# OSPPre (Open Source Parts Prediction) largely inspired by Aquant.io's Smart Triage & Parts Prediction
[A short read-up on Medium is here.](https://medium.com/@navraj28/parts-prediction-given-the-problem-description-6767c3d7e8ed) 
The Wiki has some additional insights.

## Installation
	Install the Anaconda Environment via AnacondaEnvironment.yml
	Create a MySQL DB Schema - as per DDL/DDL.sql
	Change the database connection properties in SQLHelper.py

## Usage
### Going from unstructured historical data to structured categorical data
	Get some historical data containing Work Orders & Problem Descriptions, for a specific machine, in the format shown in SampleInput/IntegrationTest.csv. Or use the sample file.
	By default, the outputs, MasterList.csv & WOsAndSymptoms.csv, are written to the folder /SampleOutput.
	Edit InvokePipeline.py to point to the file containing the historical data. 
	Invoke InvokePipeline.py.
	Review the outputs of the above process. MasterList.csv contains the Master list of Symptoms that can go wrong with the machine. Review & edit this file. Review the column symptom_text. This contains the Symptoms that are shown in the UI. Since this shows up on the UI, they should look good. Feel free to replace any value here with a semantically similar value from the column DuplicateSymptomsList. The column symptom_question should be edited to hold the question asked by the Call Center Agent during the Triage. For a Symptom_text like "Radiator leaking", the question can be something like "Is the Radiator leaking ?". WOsAndSymptoms.csv contains WO-Symptom co-occurrences and does not need to be edited.   
	Import MasterList.csv & WOsAndSymptoms.csv into the tables master_symptoms & wo_symptom_cooccurence, respectively. Note that the column DuplicateSymptomsList in MasterList.csv, does not reside in the database. Since MasterList.csv contains vectors, good import tools like Navicat or RazorSQL are required to perform the import.
	The table parts_master should contain the Parts Master data. Or use DDL/DummyPartsMaster.sql.
	The table wo_parts should contain the historical data associating the WOs & the Parts consumed. Or use DDL/DummyWOParts.sql
	Once the 4 tables are populated, start the REST service - RestService.py
  
  ### Getting Predictions
	Review the Swagger API spec under REST/openapi-client-generated
	There are just 3 APIs.
	1. Get the next Symptom question (Service used by the Triage UI)
	2. Get Predictions given the Symptom IDs
	3. Get Predictions given the Problem Description text

  [The API documentation is here](https://app.swaggerhub.com/apis/navraj28/OSPP/1.0)
