import unittest 
import pandas

from Pipeline import getUniqueSymptoms
from Pipeline import PipelineFacade

class TestPipeline(unittest.TestCase): 
      
    def setUp(self): 
        pass

    def test_UniqueSymptoms(self): 
        input = pandas.read_csv('C:\\SAM\\data\\UnitTests\\UnitTestUniqueSymptoms.csv')
        data_processed = input['Symptoms'].values
        masterList = getUniqueSymptoms(data_processed)
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
        pipelineFacade = PipelineFacade('C:\\SAM\\data\\UnitTests\\IntegrationTest.csv')
        pipelineFacade.processWOs()
        for workOrder in pipelineFacade.WOs:
            if workOrder.workOrderId == "WO-1":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Radiator leaking"))
                self.assertTrue( len(workOrder.rootSymptoms) == 1)

            if workOrder.workOrderId == "WO-2":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Water leaking over"))
                self.assertTrue( len(workOrder.rootSymptoms) == 1)

            if workOrder.workOrderId == "WO-3":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Compressor is jammed"))
                self.assertTrue( len(workOrder.rootSymptoms) == 1)

            if workOrder.workOrderId == "WO-4":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Compressor is jammed"))
                self.assertTrue( len(workOrder.rootSymptoms) == 1)

            if workOrder.workOrderId == "WO-5":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Battery is dead"))
                self.assertTrue( len(workOrder.rootSymptoms) == 1)

            if workOrder.workOrderId == "WO-6":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Radiator leaking"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("Battery is dead"))
                self.assertTrue( len(workOrder.rootSymptoms) == 2)

            if workOrder.workOrderId == "WO-7":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Radiator vibrating"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("Compressor is jammed"))
                self.assertTrue( len(workOrder.rootSymptoms) == 2)

            if workOrder.workOrderId == "WO-8":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Compressor is jammed"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("Battery is dead"))
                self.assertTrue( len(workOrder.rootSymptoms) == 2)

            if workOrder.workOrderId == "WO-9":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Radiator leaking"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("Compressor is jammed"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("Battery is dead"))
                self.assertTrue( len(workOrder.rootSymptoms) == 3)

            if workOrder.workOrderId == "WO-10":
                self.assertTrue( workOrder.rootSymptoms.__contains__("Water leaking over"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("Compressor is jammed"))
                self.assertTrue( workOrder.rootSymptoms.__contains__("Battery is dead"))
                self.assertTrue( len(workOrder.rootSymptoms) == 3)

if __name__ == '__main__': 
    unittest.main() 
    
