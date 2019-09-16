# OSPP (Open Source Parts Prediction) largely inspired by Aquant.io's Smart Triage & Parts Prediction
[A short read-up on Medium is here.](https://medium.com/@navraj28/parts-prediction-given-the-problem-description-6767c3d7e8ed) 
The Wiki has some additional insights.

## Installation
	Install the Anaconda Environment via AnacondaEnvironment.yml
	Create a MySQL DB Schema - as per DDL/DDL.sql
	Change the database connection properties in SQLHelper.py

## Usage
### Going from unstructured historical data to structured categorical data
	Get some historical data containing Work Orders & Problem Descriptions, for a specific machine, in the format shown in SampleInput/IntegrationTest.csv
	Edit Pipeline.py to change the directory into which the outputs, MasterList.csv & WOsAndSymptoms.csv, are written.
	Edit InvokePipeline.py to point to the file containing the historical data. 
	Invoke InvokePipeline.py.
	Review the output of the above process. Edit MasterList.csv to add questions specific to the Symptoms.
	Import MasterList.csv & WOsAndSymptoms.csv into the tables master_symptoms & wo_symptom_cooccurence, respectively.
	The tables parts_master should contain the Parts Master data.
	The table wo_parts should contain the historical data associating the WOs & the Parts consumed.
	Once the 4 tables are populated, start the REST service - RestService.py
  
  ### Getting Predictions
	Review the Swagger API spec under REST/openapi-client-generated
	There are just 3 APIs.
	1. Get the next Symptom question (Service used by the Triage UI)
	2. Get Predictions given the Symptom IDs
	3. Get Predictions given the Problem Description text

  [The API documentation is here](https://app.swaggerhub.com/apis/navraj28/OSPP/1.0)
