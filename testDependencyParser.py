import unittest 
from DependencyParser import getCoreIssues
  
class TestDependencyParser(unittest.TestCase): 
      
    def setUp(self): 
        pass

    def test_DependencyParser(self): 
        coreIssues =  getCoreIssues("Printer is not flashing")
        self.assertEqual(coreIssues[0], "Printer not flashing")
        self.assertEqual(len(coreIssues), 1)

        coreIssues =  getCoreIssues("Reader lost connection")
        self.assertEqual( coreIssues[0] , "Reader lost connection")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Script kill error")
        self.assertEqual( coreIssues[0] , "Script kill error")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("The Rack is bent")
        self.assertEqual( coreIssues[0] , "Rack is bent")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Cartridge showing bubbles")
        self.assertEqual( coreIssues[0] , "Cartridge showing bubbles")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Unit is leaking")
        self.assertEqual( coreIssues[0] , "Unit leaking")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Pressure is low")
        self.assertEqual( coreIssues[0] , "Pressure is low")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Pump failure")
        self.assertEqual( coreIssues[0] , "Pump failure")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Bent rack")
        self.assertEqual( coreIssues[0] , "Bent rack")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Event rate issue")
        self.assertEqual( coreIssues[0] , "Event rate issue")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Power issue")
        self.assertEqual( coreIssues[0] , "Power issue")
        self.assertEqual( len(coreIssues) , 1)

        phrases = getCoreIssues("The Radiator is leaking, battery is overflowing, and the tubes are rusted.")
        self.assertEqual( phrases[0] , "Radiator leaking")
        self.assertEqual( phrases[1] , "battery overflowing")
        self.assertEqual( phrases[2] , "tubes rusted")
        self.assertEqual( len(phrases) , 3)

        coreIssues =  getCoreIssues("Unable to print")
        self.assertEqual( coreIssues[0] , "Unable print")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Replace front disc brakes.")
        self.assertEqual( coreIssues[0] , "Replace front disc brakes")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Refurbish the cycle.")
        self.assertEqual( coreIssues[0] , "Refurbish cycle")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Refurbish")
        self.assertEqual( coreIssues[0] , "Refurbish")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Mudguard missing.")
        self.assertEqual( coreIssues[0] , "Mudguard missing")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Mudguards are missing.")
        self.assertEqual( coreIssues[0] , "Mudguards missing")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues =  getCoreIssues("Replace rear disc brakes.")
        self.assertEqual( coreIssues[0] , "Replace rear disc brakes")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues = getCoreIssues("Cartridge showing Power issue.")
        self.assertEqual( coreIssues[0] , "Cartridge showing Power issue")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues = getCoreIssues('The Pressure indicator is showing Low')
        self.assertEqual( coreIssues[0] , "Pressure indicator showing Low")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues = getCoreIssues(u"The delivery was very late!")
        self.assertEqual( coreIssues[0] , "delivery was late")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues = getCoreIssues(u"Create new work orders")
        self.assertEqual( coreIssues[0] , "Create orders")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues = getCoreIssues(u"A strange vomiting sensation")
        self.assertEqual( coreIssues[0] , "strange vomiting sensation")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues = getCoreIssues(u"Feel like throwing up")
        self.assertEqual( coreIssues[0] , "throwing up")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues = getCoreIssues(u"Water leaking all over")
        self.assertEqual( coreIssues[0] , "Water leaking")
        self.assertEqual( len(coreIssues) , 1)

        coreIssues = getCoreIssues(u"Radiator is leaking and the battery needs to be replaced")
        self.assertEqual( coreIssues[0] , "Radiator leaking")
        self.assertEqual( coreIssues[1] , "battery needs replaced")
        self.assertEqual( len(coreIssues) , 2)

        coreIssues = getCoreIssues(u"Water leaking all over the place, the Compressor is not starting and the battery needs replacement")
        self.assertEqual( coreIssues[0] , "Water leaking")
        self.assertEqual( coreIssues[1] , "Compressor not starting")
        self.assertEqual( coreIssues[2] , "battery needs replacement")
        self.assertEqual( len(coreIssues) , 3)

if __name__ == '__main__': 
    unittest.main() 