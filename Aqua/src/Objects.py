#from USE import get_features, cosineSimilarity

from USEWithPlaceHolders import get_features, cosineSimilarity
from DependencyParser import getCoreIssues
import numpy, json

THRESHOLD = 0.84

class WorkOrder:
    def __init__(self, unique_product_id, workOrderId, problemDescription):
        self.unique_product_id = unique_product_id
        self.workOrderId = workOrderId
        self.problemDescription = problemDescription
        self.originalSymptoms = getCoreIssues(problemDescription)
        self.rootSymptoms = []
        self.rootSymptomIds = []
        self.rootSymptomIdsNotPresent = []

    def mapToRootSymptoms(self, rootSymptoms):
        originalSymptomsVector = get_features(self.originalSymptoms)
        for index, value in enumerate(self.originalSymptoms):
            for rootIndex, rootValue in enumerate(rootSymptoms):
                if cosineSimilarity(originalSymptomsVector[index], rootValue.textVectorForm[0]) > THRESHOLD :
                    self.rootSymptoms.append(rootValue.symptomText) 
                    self.rootSymptomIds.append(rootValue.symptomId)
                    break

    def addSymptomThatIsPresent(self, symptomId):
        self.rootSymptomIds.append(symptomId)

    def removeSymptomThatIsPresent(self, symptomId):
        self.rootSymptomIds.remove(symptomId)

    def addSymptomThatIsNotPresent(self, symptomId):
        self.rootSymptomIdsNotPresent.append(symptomId)

    def removeSymptomThatIsNotPresent(self, symptomId):
        self.rootSymptomIdsNotPresent.remove(symptomId)

class RootSymptom:
    def __init__(self, productId, symptomId, symptomText, symptomQuestion, vector):
        self.productId = productId
        self.symptomId = symptomId
        self.symptomText = symptomText
        self.symptomQuestion = symptomQuestion
#        if vector is None:
#            self.textVectorForm = get_features( [symptomText] )
#        else:
#            self.textVectorForm = numpy.array(json.loads(vector))
#        self.textVectorForm = get_features( [symptomText] )
        self.textVectorForm = numpy.array(json.loads(vector)).reshape(1 , 512)

class PartsRecommendation:
    def __init__(self, partId, partName, probablityPercentage, numberOfParts):
        self.partId = partId
        self.partName = partName
        self.probablityPercentage = probablityPercentage
        self.numberOfParts = round(numberOfParts)
        
class UIRootSymptom:
    def __init__(self, symptomId, symptomText):
        self.symptomId = symptomId
        self.symptomText = symptomText

class RemoteSolutions:
    def __init__(self):
        self.remoteSolutions = ["Try a reboot.", "Recalibrate the machibe."]

class UIPartsRecommendation:
    def __init__(self, partsRecommendation, remoteSolutions):
        self.partsRecommendation = partsRecommendation
        self.remoteSolutions = remoteSolutions
