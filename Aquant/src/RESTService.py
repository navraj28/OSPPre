import mysql.connector
import pandas

from Pipeline import fromProblemDescriptionToPartsPrediction
from Pipeline import RootSymptom
from Pipeline import WorkOrder
from USEWithPlaceHolders import get_features, init
from SQLHelper import getPartsPredictiction

#from USE import cosineSimilarity
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from collections import namedtuple
import json
import tensorflow as tf
import tensorflow_hub as hub

app = Flask(__name__)
api = Api(app)

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

class HelloWorld(Resource):
    def get(self):
#        result1 = session.run(embedded_text, feed_dict={text_input: ["The Radiator is leaking"]})
#        result1 = result1.reshape(1 , 512)
#        result2 = session.run(embedded_text, feed_dict={text_input: ["The Radiator is vibrating"]})
#        result2 = result2.reshape(1 , 512)        

#        print( cosine_similarity(get_features("The Radiator is leaking"), get_features("The Radiator is vibrating")) )
        workOrder = WorkOrder('Manufacturer', 'ProductFamily', 'ProductLine', 'ID', 'Radiator is leaking and the battery needs to be replaced')
        pred = fromProblemDescriptionToPartsPrediction(workOrder)
        for part in pred:
            if part.partId == 2 and part.numberOfParts == 2 and part.probablityPercentage == 50:
                print(part.partName, part.probablityPercentage, "%, # of parts ", part.numberOfParts)
            elif part.partId == 3 and part.numberOfParts == 3 and part.probablityPercentage == 100:
                print(part.partName, part.probablityPercentage, "%, # of parts ", part.numberOfParts)
            elif part.partId == 1 and part.numberOfParts == 1 and part.probablityPercentage == 100:
                print(part.partName, part.probablityPercentage, "%, # of parts ", part.numberOfParts)
            else:
                print("ERROR!")

        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

@app.route('/PredictPartsGivenProblemDescription', methods=['POST'])
def predictPartsGivenProblemDescription():
    content = request.get_json()
    x = json2obj(request.data)

    #TODO Change WO Constructor
    workOrder = WorkOrder('Manufacturer', 'ProductFamily', 'ProductLine', 'ID', x.ProblemDescription)
    pred = fromProblemDescriptionToPartsPrediction(workOrder)
    jsonStr = json.dumps([ob.__dict__ for ob in pred])
    return jsonStr

@app.route('/PredictPartsGivenSymptoms', methods=['POST'])
def predictPartsGivenSymptoms():
    content = request.get_json()
    x = json2obj(request.data)

    print(x.SymptomsThatArePresent, type(x.SymptomsThatArePresent))
    #TODO Change WO Constructor
    workOrder = WorkOrder('Manufacturer', 'ProductFamily', 'ProductLine', 'ID', '')
    workOrder.rootSymptomIds = x.SymptomsThatArePresent
    workOrder.rootSymptomIdsNotPresent = x.SymptomsThatAreNOTPresent

    pred = getPartsPredictiction(workOrder)
    jsonStr = json.dumps([ob.__dict__ for ob in pred])
    return jsonStr

if __name__ == '__main__':
    init()
    app.run(debug=False)