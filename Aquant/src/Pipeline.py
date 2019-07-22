from USE import get_features, cosineSimilarity
from DependencyParser import getCoreIssues
from Objects import WorkOrder, RootSymptom, THRESHOLD, PartsRecommendation
from SQLHelper import fetchRootSymptomsFromDB, getPartsPredictiction
import pandas
import csv

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

    return masterList

def getSymptomIdForeignKey(rootSymptom, rootSymptoms):
    for row in rootSymptoms:
        if row[4] == rootSymptom:
            return row[3]
    return -1

class PipelineFacade:
    def __init__(self, fileName):
        self.fileName = fileName
        self.WOs = []
        input = pandas.read_csv(fileName)
        for index, row in input.iterrows():
            self.WOs.append( WorkOrder(row['Manufacturer'], row['ProductFamily'], row['ProductLine'], row['ID'], row['Description']) )
        
    def processWOs(self):
        allSymptoms = []
        for wo in self.WOs:
            allSymptoms.extend( wo.originalSymptoms)
        masterList = getUniqueSymptoms(allSymptoms)
        for wo in self.WOs:
            mapSymptomsToRootSymptoms(masterList, wo)
            print(wo.workOrderId, " ", wo.rootSymptoms)

        #Write the Master Symptom List to CSV
        rootSymptoms = []
        for index, key in enumerate(masterList):
            row = []
            row.append( self.WOs[0].manufacturer)
            row.append( self.WOs[0].productFamily)
            row.append( self.WOs[0].productLine)
            row.append(index)
            row.append(key)
            row.append("ToDo")
            array = masterList.get(key)
            row.append( array )
            rootSymptoms.append(row)

        with open('C:\\SAM\\data\\UnitTests\\MasterList.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(["Manufacturer", "ProductFamily", "ProductLine", "SymptomId", "SymptomText", "SymptomQuestion","DuplicateSymptomsList"])
            writer.writerows(rootSymptoms)
        writeFile.close()

        #Write the WO-Root Symptom Co-Occurence CSV. Parts will get appended later
        rows = []
        for wo in self.WOs:
            for rootSymptom in wo.rootSymptoms:
                row = []
                row.append( wo.manufacturer)
                row.append( wo.productFamily)
                row.append( wo.productLine)
                row.append( wo.workOrderId)
                row.append( getSymptomIdForeignKey(rootSymptom, rootSymptoms))
                rows.append(row)

        with open('C:\\SAM\\data\\UnitTests\\WOsAndSymptoms.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(rows)
        writeFile.close()

def fromProblemDescriptionToPartsPrediction(workOrder):
    #Fetch Root Symptoms from DB
    #TODO Needs to be cached
    rootSymptoms = fetchRootSymptomsFromDB()

    #Loop thru the Original Symptoms to map them to their Root symptoms
    workOrder.mapToRootSymptoms(rootSymptoms)
    for indx, val in enumerate(workOrder.rootSymptoms) :
        print( val, workOrder.rootSymptomIds[indx])
    
    pred = getPartsPredictiction(workOrder)
    for part in pred:
        print('Part No. ' + str(part.partId) + ' ' + part.partName + ' Quantity ' + str(part.numberOfParts) + ' PROBABLITY ' + str(part.probablityPercentage) + "%")
    return pred
    
workOrder = WorkOrder('Manufacturer', 'ProductFamily', 'ProductLine', 'ID', 'Radiator is leaking and the battery needs to be replaced')
pred = fromProblemDescriptionToPartsPrediction(workOrder)
