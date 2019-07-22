import unittest 
import pandas

from Objects import WorkOrder, RootSymptom, PartsRecommendation
from SQLHelper import fetchRootSymptomsFromDB, getPartsPredictiction

class TestSQLHelper(unittest.TestCase): 
      
    def setUp(self): 
        pass

    def test_SQLGivenSymptoms(self):
        workOrder = WorkOrder('Manufacturer', 'ProductFamily', 'ProductLine', 'ID', 'Radiator is leaking and the battery needs to be replaced')
        workOrder.rootSymptomIds = [3,2,1]
        pred = getPartsPredictiction(workOrder)
        #Parts 1,2,3 are in quantities 1,2,3 with 100% Probablity
        for part in pred:
            if part.partId == 1:
                self.assertTrue(part.numberOfParts == 1)
                self.assertTrue(part.probablityPercentage == 100)
            elif part.partId == 2:
                self.assertTrue(part.numberOfParts == 2)
                self.assertTrue(part.probablityPercentage == 100)
            elif part.partId == 3:
                self.assertTrue(part.numberOfParts == 3)
                self.assertTrue(part.probablityPercentage == 100)
            else:
                self.assertFalse(True)

        workOrder = WorkOrder('Manufacturer', 'ProductFamily', 'ProductLine', 'ID', 'Radiator is leaking and the battery needs to be replaced')
        workOrder.rootSymptomIds = [3]
        workOrder.rootSymptomIdsNotPresent = [1,2]
        pred = getPartsPredictiction(workOrder)
        for part in pred:
            if part.partId == 1:
                self.assertTrue(part.numberOfParts == 1)
                self.assertTrue(part.probablityPercentage == 50)
            elif part.partId == 3:
                self.assertTrue(part.numberOfParts == 3)
                self.assertTrue(part.probablityPercentage == 100)
            else:
                self.assertFalse(True)

        workOrder = WorkOrder('Manufacturer', 'ProductFamily', 'ProductLine', 'ID', 'Radiator is leaking and the battery needs to be replaced')
        workOrder.rootSymptomIds = [2]
        workOrder.rootSymptomIdsNotPresent = [1,3]
        pred = getPartsPredictiction(workOrder)
        for part in pred:
            print('Part No. ' + str(part.partId) + ' ' + part.partName + ' Quantity ' + str(part.numberOfParts) + ' PROBABLITY ' + str(part.probablityPercentage) + "%")
        for part in pred:
            if part.partId == 2:
                self.assertTrue(part.numberOfParts == 2)
                self.assertTrue(part.probablityPercentage == 100)
            elif part.partId == 4:
                self.assertTrue(part.numberOfParts == 4)
                self.assertTrue(part.probablityPercentage == 33)
            else:
                self.assertFalse(True)

        workOrder = WorkOrder('Manufacturer', 'ProductFamily', 'ProductLine', 'ID', 'Radiator is leaking and the battery needs to be replaced')
        workOrder.rootSymptomIds = [2,3]
        workOrder.rootSymptomIdsNotPresent = [1]
        pred = getPartsPredictiction(workOrder)
        for part in pred:
            if part.partId == 2:
                self.assertTrue(part.numberOfParts == 2)
                self.assertTrue(part.probablityPercentage == 100)
            elif part.partId == 3:
                self.assertTrue(part.numberOfParts == 3)
                self.assertTrue(part.probablityPercentage == 100)
            elif part.partId == 1:
                self.assertTrue(part.numberOfParts == 1)
                self.assertTrue(part.probablityPercentage == 50)
            else:
                self.assertFalse(True)

if __name__ == '__main__': 
    unittest.main() 
