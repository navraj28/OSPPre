import mysql.connector
import pandas

from Pipeline import fromProblemDescriptionToPartsPrediction
from Pipeline import RootSymptom
from Pipeline import WorkOrder

from flask import Flask
app = Flask(__name__)

workOrder = WorkOrder('Manufacturer', 'ProductFamily', 'ProductLine', 'ID', 'Radiator is leaking and the battery needs to be replaced')
fromProblemDescriptionToPartsPrediction(workOrder)
    
