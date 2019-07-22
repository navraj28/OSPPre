from USE import get_features, cosineSimilarity
from DependencyParser import getCoreIssues

THRESHOLD = 0.84

class WorkOrder:
    def __init__(self, manufacturer, productFamily, productLine, workOrderId, problemDescription):
        self.manufacturer = manufacturer
        self.productFamily = productFamily
        self.productLine = productLine
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
    def __init__(self, productId, symptomId, symptomText, symptomQuestion):
        self.productId = productId
        self.symptomId = symptomId
        self.symptomText = symptomText
        self.symptomQuestion = symptomQuestion
        self.textVectorForm = get_features( [symptomText] )

class PartsRecommendation:
    def __init__(self, partId, partName, probablityPercentage, numberOfParts):
        self.partId = partId
        self.partName = partName
        self.probablityPercentage = probablityPercentage
        self.numberOfParts = round(numberOfParts)
        
