#from USE import get_features, cosineSimilarity
from USEWithPlaceHolders import get_features, cosineSimilarity
from DependencyParser import getCoreIssues
from Objects import WorkOrder, RootSymptom, THRESHOLD, PartsRecommendation, RemoteSolutions, UIPartsRecommendation
from SQLHelper import fetchRootSymptomsFromDB, getPartsPredictiction
import pandas
import csv
import numpy as np
import json
from pathlib import Path
import re

def mapSymptomToQuestion(symptom):
	insensitive = re.compile(re.escape('The'), re.IGNORECASE)
	str = insensitive.sub("", symptom)
	insensitive = re.compile(re.escape('iS'), re.IGNORECASE)
	str = insensitive.sub("", str)
	return "Is the " + str.strip() + "?"

def mapSymptomsToRootSymptoms(masterList, wo):    
    for symptom in wo.originalSymptoms:
        if symptom in masterList.keys():
            wo.rootSymptoms.append(symptom)
            continue
        for key in masterList.keys():
            array = masterList.get(key)
            for duplicate in array:
                if duplicate in wo.originalSymptoms:
                    if not wo.rootSymptoms.__contains__(key):
                        wo.rootSymptoms.append(key)
                        break


def alreadyTracked(masterList, innerVal):
    if innerVal in masterList.keys():
        return True
    for key in masterList.keys():
        array = masterList.get(key)
        if innerVal in array:
            return True
    return False

def getUniqueSymptoms(data_processed):
    BASE_VECTORS = get_features(data_processed)
    print(BASE_VECTORS.shape)
    print(type(BASE_VECTORS))

    masterList = {} #A Dict (Keys are unique Symptoms) containing an array of Duplicates symptoms (Child)
    for idx, val in enumerate(data_processed):
        duplicateSymptoms = []

        for innerIdx, innerVal in enumerate(data_processed):
            if idx == innerIdx:
                continue
            #Check that innerVal does not already exist in the Dict
            if not alreadyTracked(masterList, innerVal): 
                if cosineSimilarity(BASE_VECTORS[idx], BASE_VECTORS[innerIdx]) > THRESHOLD :
                #These 2 issues are duplicates  
                    duplicateSymptoms.append(innerVal)

        if not alreadyTracked(masterList, val):
            masterList[val] = duplicateSymptoms

    return masterList, BASE_VECTORS

def getSymptomIdForeignKey(rootSymptom, rootSymptoms):
    for row in rootSymptoms:
        if row[2] == rootSymptom:
            return row[1]
    return -1

class PipelineFacade:
    def __init__(self, fileName):
        self.fileName = fileName
        self.WOs = []
        input = pandas.read_csv(fileName)
        for index, row in input.iterrows():
            self.WOs.append( WorkOrder(row['unique_product_id'], row['ID'], row['Description']) )
        
    def processWOs(self):
        allSymptoms = []
        for wo in self.WOs:
            allSymptoms.extend( wo.originalSymptoms)
        masterList, BASE_VECTORS = getUniqueSymptoms(allSymptoms)
        for wo in self.WOs:
            mapSymptomsToRootSymptoms(masterList, wo)
            print(wo.workOrderId, " ", wo.rootSymptoms)

        #Write the Master Symptom List to CSV
        rootSymptoms = []
        for index, key in enumerate(masterList):
            row = []
            row.append( self.WOs[0].unique_product_id)
            row.append(index)
            row.append(key)
            row.append(mapSymptomToQuestion(key))
            array = masterList.get(key)
            row.append( array )
            #Store the Vector Value as-well
            for ind2, symp in enumerate(allSymptoms):
                if symp == key:
#                    vecAsString = np.ndarray.dumps( BASE_VECTORS[ind2] )
                    vecAsString = json.dumps(BASE_VECTORS[ind2].tolist())
                    row.append( vecAsString )
                    break
            rootSymptoms.append(row)

        base_path = Path(__file__).parent
        file_path = (base_path / "../SampleOutput/MasterList.csv").resolve()

        with open(str(file_path), 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(["unique_product_id", "symptom_id", "symptom_text", "symptom_question","DuplicateSymptomsList", "vector"])
            writer.writerows(rootSymptoms)
        writeFile.close()

        #Write the WO-Root Symptom Co-Occurence CSV. Parts will get appended later
        rows = []
        for wo in self.WOs:
            for rootSymptom in wo.rootSymptoms:
                row = []
                row.append( wo.unique_product_id)
                row.append( wo.workOrderId)
                row.append( getSymptomIdForeignKey(rootSymptom, rootSymptoms))
                rows.append(row)

        file_path = (base_path / "../SampleOutput/WOsAndSymptoms.csv").resolve()
        with open(str(file_path), 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(["unique_product_id", "work_order_id", "symptom_id"])
            writer.writerows(rows)
        writeFile.close()

def fromProblemDescriptionToPartsPrediction(workOrder):
    #Fetch Root Symptoms from DB
    #TODO Needs to be cached
    rootSymptoms = fetchRootSymptomsFromDB(workOrder.unique_product_id)

    #Loop thru the Original Symptoms to map them to their Root symptoms
    workOrder.mapToRootSymptoms(rootSymptoms)
    for indx, val in enumerate(workOrder.rootSymptoms) :
        print( val, workOrder.rootSymptomIds[indx])
    
    pred = getPartsPredictiction(workOrder)
    for part in pred:
        print('Part No. ' + str(part.partId) + ' ' + part.partName + ' Quantity ' + str(part.numberOfParts) + ' PROBABLITY ' + str(part.probablityPercentage) + "%")
#    return pred

#    jsonStr1 = json.dumps([ob.__dict__ for ob in pred])
#    rs = [RemoteSolutions()]
#    jsonStr2 = json.dumps(ob.__dict__ for ob in rs)
#    dict = {'PartsRecommendations': jsonStr1, 'RemoteSolutions': jsonStr2}
#    return dict
    uiPR = UIPartsRecommendation(pred, RemoteSolutions())
    return uiPR