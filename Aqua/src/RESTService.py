from Pipeline import fromProblemDescriptionToPartsPrediction
from Pipeline import WorkOrder
from USEWithPlaceHolders import get_features, init
from SQLHelper import getPartsPredictiction, buildSymptomCooccurence, fetchRootSymptomsForUI
from Objects import UIPartsRecommendation, RemoteSolutions
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from collections import namedtuple
import json
import jsonpickle

app = Flask(__name__)
api = Api(app)

THRESHOLD_FOR_COOCCURENCE = 1

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
    try:
        content = request.get_json()
        x = json2obj(request.data)

        workOrder = WorkOrder(x.UniqueProductIdentifier, 'ID', x.ProblemDescription)
        pred = fromProblemDescriptionToPartsPrediction(workOrder)
#        jsonStr = json.dumps([ob.__dict__ for ob in pred])
#        return jsonStr

#        return json.dumps(pred)
#        return jsonify(pred)
        return jsonpickle.encode(pred)
#        return serialize('json', pred)
    except ValueError as err:
        jsonStr = json.dumps( str(err) )
        return jsonStr

@app.route('/PredictPartsGivenSymptoms', methods=['POST'])
def predictPartsGivenSymptoms():
    try:
        content = request.get_json()
        x = json2obj(request.data)

        workOrder = WorkOrder(x.UniqueProductIdentifier, 'ID', '')
        workOrder.rootSymptomIds = x.SymptomsThatArePresent
        workOrder.rootSymptomIdsNotPresent = x.SymptomsThatAreNOTPresent

        pred = getPartsPredictiction(workOrder)
#        jsonStr = json.dumps([ob.__dict__ for ob in pred])
#        return jsonStr
        uiPR = UIPartsRecommendation(pred, RemoteSolutions())
        return jsonpickle.encode(uiPR)
    except ValueError as err:
        jsonStr = json.dumps( str(err) )
        return jsonStr

@app.route('/GetNextSymptomQuestion', methods=['POST'])
def getNextSymptomQuestion():
    content = request.get_json()
    x = json2obj(request.data)

    arr = buildSymptomCooccurence(x.UniqueProductIdentifier, x.SymptomsThatArePresent, x.SymptomsThatAreNOTPresent, THRESHOLD_FOR_COOCCURENCE)
    j = 0
    while j < len(arr[0]):
        if arr[0][j] in x.SymptomsThatArePresent:
            j += 1
            continue
        if arr[0][j] in x.SymptomsThatAreNOTPresent:
            j += 1
            continue
        if arr[0][j] in x.SymptomsThatWereSkipped:
            j += 1
            continue

        ret = {}
        ret['symptomId'] = arr[0][j]
        ret['symptomQuestion'] = arr[1][j]
        jsonStr = json.dumps(ret)
        return jsonStr
        j += 1    

    ret = {}
    ret['symptomId'] = -1
    ret['symptomQuestion'] = "Done with the Triage."
    jsonStr = json.dumps(ret)
    return jsonStr

@app.route('/GetRootSymptoms', methods=['POST'])
def getRootSymptoms():
    try:
        content = request.get_json()
        x = json2obj(request.data)

        symptoms = fetchRootSymptomsForUI(x.UniqueProductIdentifier)
        jsonStr = json.dumps([ob.__dict__ for ob in symptoms])
        return jsonStr
    except ValueError as err:
        jsonStr = json.dumps( str(err) )
        return jsonStr

if __name__ == '__main__':
    init()
    app.run(debug=False, host= '0.0.0.0')
