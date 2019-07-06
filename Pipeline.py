from USE import get_features, cosineSimilarity
from DependencyParser import getCoreIssues

import pandas

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
                if cosineSimilarity(BASE_VECTORS[idx], BASE_VECTORS[innerIdx]) > 0.84 :
                #These 2 issues are duplicates  
                    duplicateSymptoms.append(innerVal)

        if not alreadyTracked(masterList, val):
            masterList[val] = duplicateSymptoms

    return masterList

class WorkOrder:
    def __init__(self, workOrderId, problemDescription):
        self.workOrderId = workOrderId
        self.problemDescription = problemDescription
        self.originalSymptoms = getCoreIssues(problemDescription)
        self.rootSymptoms = []

class PipelineFacade:
    def __init__(self, fileName):
        self.fileName = fileName
        self.WOs = []
        input = pandas.read_csv(fileName)
        for index, row in input.iterrows():
            self.WOs.append( WorkOrder(row['ID'], row['Description']) )
        
    def processWOs(self):
        allSymptoms = []
        for wo in self.WOs:
            allSymptoms.extend( wo.originalSymptoms)
        masterList = getUniqueSymptoms(allSymptoms)
        for wo in self.WOs:
            mapSymptomsToRootSymptoms(masterList, wo)
            print(wo.workOrderId, " ", wo.rootSymptoms)