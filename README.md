# OSPPre (Open Source Parts Prediction), largely inspired by Aquant.io's Smart Triage & Parts Prediction
[A short read-up on Medium is here.](https://medium.com/@navraj28/parts-prediction-given-the-problem-description-6767c3d7e8ed) 
The Wiki has some additional insights.

## Installation
	Install the Anaconda Environment via AnacondaEnvironment.yml
	Create a MySQL DB Schema - as per DDL/DDL.sql
	Change the database connection properties in SQLHelper.py

## Usage
### Going from unstructured historical data to structured categorical data
1. Get some historical data containing Work Orders & Problem Descriptions, for a specific machine, in the format shown in _SampleInput/IntegrationTest.csv_. Or use the sample file.
	
2. By default, the outputs, _MasterList.csv_ & _WOsAndSymptoms.csv_, are written to the folder _/SampleOutput_.
	
3. Edit _InvokePipeline.py_ to point to the file containing the historical data. 

4. Invoke _InvokePipeline.py_.
	
5. Review the outputs of the above process. _MasterList.csv_ contains the Master list of Symptoms that can go wrong with the machine. Review & edit this file. Review the column _symptom_text_. This contains the Symptoms that are shown in the UI. Since this shows up on the UI, they should look good. Feel free to replace any value here with a semantically similar value from the column _DuplicateSymptomsList_. The column symptom_question should be edited to hold the question asked by the Call Center Agent during the Triage. For a Symptom_text like _"Radiator leaking"_, the question can be something like _"Is the Radiator leaking ?"_. _WOsAndSymptoms.csv_ contains WO-Symptom co-occurrences and does not need to be edited.   
	
6. Import _MasterList.csv_ & _WOsAndSymptoms.csv_ into the tables _master_symptoms_ & _wo_symptom_cooccurence_, respectively. Note that the column _DuplicateSymptomsList_ in _MasterList.csv_, does not reside in the database. Since _MasterList.csv_ contains vectors, good import tools like _Navicat_ or _RazorSQL_ are required to perform the import.
	
7. The table _parts_master_ should contain the Parts Master data. Or use _DDL/DummyPartsMaster.sql_.
	
8. The table _wo_parts_ should contain the historical data associating the WOs & the Parts consumed. Or use _DDL/DummyWOParts.sql_
	
9. Once the 4 tables are populated, start the REST service - _RestService.py_

  ### Getting Predictions
	Review the Swagger API spec under REST/openapi-client-generated
	There are just 3 APIs.
	1. Get the next Symptom question (Service used by the Triage UI)
	2. Get Predictions given the Symptom IDs
	3. Get Predictions given the Problem Description text
  [The API documentation is here](https://app.swaggerhub.com/apis/navraj28/OSPP/1.0)
