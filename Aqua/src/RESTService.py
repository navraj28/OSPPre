from Pipeline import fromProblemDescriptionToPartsPrediction
from Pipeline import WorkOrder
from USEWithPlaceHolders import get_features, init
from SQLHelper import getPartsPredictiction, buildSymptomCooccurence, fetchRootSymptomsForUI
from Objects import UIPartsRecommendation, RemoteSolutions
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from collections import namedtuple
import json
import jsonpickle

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

THRESHOLD_FOR_COOCCURENCE = 1

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

@app.route('/PredictPartsGivenProblemDescription', methods=['POST'])
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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

@app.route('/')
def main():
    return render_template('home.html')

@app.route("/OSPPre")
def index():
    api_variable = 'ManufacturerProductFamilyProductLine'
    url = 'http://Osppre-Test.eba-vi3z5hvq.us-east-2.elasticbeanstalk.com'
    caseid = '567896789'
    productType = 'Molecular Diagnostics'
    manufacturer = 'Johnson Medical'
    productNumber = 'Quantum 3300'
    return render_template('index.html', variable=api_variable,
                            api_url = url,
                            case_id=caseid,
                            product_type=productType,
                            Manufacturer=manufacturer,
                            product_number=productNumber)

if __name__ == '__main__':
    init()
#    app.run(debug=False, host= '0.0.0.0')
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)