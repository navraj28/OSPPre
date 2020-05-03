import unittest 
import pandas
import csv
from pathlib import Path

from Pipeline import getUniqueSymptoms, fromProblemDescriptionToPartsPrediction, PipelineFacade
from Objects import WorkOrder, RootSymptom, PartsRecommendation
from USEWithPlaceHolders import init

class TestPipeline(unittest.TestCase): 
      
    def setUp(self): 
        init()
        pass

    def test_UniqueSymptoms(self):
        base_path = Path(__file__).parent
        file_path = (base_path / "../SampleInput/UnitTestUniqueSymptoms.csv").resolve()
        input = pandas.read_csv(str(file_path))
        data_processed = input['Symptoms'].values
        masterList, BASE_VECTORS = getUniqueSymptoms(data_processed)
        print("Set of Unique Symptoms ", masterList.keys())
        self.assertEqual( len(masterList.keys()) , 5)
        self.assertTrue( "Radiator leaking" in masterList)
        self.assertTrue( "Water leaking over" in masterList)
        self.assertTrue( "Compressor is jammed" in masterList)
        self.assertTrue( "Battery is dead" in masterList)
        self.assertTrue( "Radiator vibrating" in masterList)

        for key in masterList.keys():
            array = masterList.get(key)
            print("Duplicate Symptoms for ", key, " are ", array)
            if key == "Radiator leaking":
                self.assertTrue( len(array) == 2)
            if key == "Water leaking over":
                self.assertTrue( len(array) == 1)
            if key == "Compressor is jammed":
                self.assertTrue( len(array) == 5)
            if key == "Battery is dead":
                self.assertTrue( len(array) == 4)
            if key == "Radiator vibrating":
                self.assertTrue( len(array) == 0)

    def test_PipelineFacade(self):
        base_path = Path(__file__).parent
        file_path = (base_path / "../SampleInput/IntegrationTest.csv").resolve()
        pipelineFacade = PipelineFacade(str(file_path))
        pipelineFacade.processWOs()
        for workOrder in pipelineFacade.WOs:
            if workOrder.workOrderId == "WO-1":
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Radiator leaking"))
                self.assertTrue( len(workOrder.rootSymptoms) == 1)

            if workOrder.workOrderId == "WO-2":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Water leaking over"))
                self.assertTrue( len(workOrder.rootSymptoms) == 1)

            if workOrder.workOrderId == "WO-3":
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Compressor is jammed"))
                self.assertTrue( len(workOrder.rootSymptoms) == 1)

            if workOrder.workOrderId == "WO-4":
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Compressor not starting"))
                self.assertTrue( len(workOrder.rootSymptoms) == 1)

            if workOrder.workOrderId == "WO-5":
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Battery is dead"))
                self.assertTrue( len(workOrder.rootSymptoms) == 1)

            if workOrder.workOrderId == "WO-6":
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Radiator leaking"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Battery is dead"))
                self.assertTrue( len(workOrder.rootSymptoms) == 2)

            if workOrder.workOrderId == "WO-7":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Radiator vibrating"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Compressor is jammed"))
                self.assertTrue( len(workOrder.rootSymptoms) == 2)

            if workOrder.workOrderId == "WO-8":
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Compressor is jammed"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Battery is dead"))
                self.assertTrue( len(workOrder.rootSymptoms) == 2)

            if workOrder.workOrderId == "WO-9":
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Radiator leaking"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Compressor is jammed"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Battery is dead"))
                self.assertTrue( len(workOrder.rootSymptoms) == 3)

            if workOrder.workOrderId == "WO-10":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Water leaking over"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Compressor not starting"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("The Battery is dead"))
#                self.assertTrue( len(workOrder.rootSymptoms) == 3)

    def test_PartsReccoGivenProblemDescription(self):
        workOrder = WorkOrder('ManufacturerProductFamilyProductLine', 'ID', 'Radiator is leaking and the battery needs to be replaced')
        pred = fromProblemDescriptionToPartsPrediction(workOrder)
        for part in pred:
            if part.partId == 2:
                self.assertTrue(part.numberOfParts == 2)
                self.assertTrue(part.probablityPercentage == 50)
            elif part.partId == 3:
                self.assertTrue(part.numberOfParts == 3)
                self.assertTrue(part.probablityPercentage == 100)
            elif part.partId == 1:
                self.assertTrue(part.numberOfParts == 1)
                self.assertTrue(part.probablityPercentage == 100)
            else:
                self.assertFalse(True)
            
            print(part.partName, part.probablityPercentage, "%, # of parts ", part.numberOfParts)

if __name__ == '__main__': 
    unittest.main() 
    
