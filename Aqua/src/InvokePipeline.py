from pathlib import Path
from Pipeline import PipelineFacade
from USEWithPlaceHolders import init

base_path = Path(__file__).parent
file_path = (base_path / "../SampleInput/IntegrationTest.csv").resolve()
print("Processing file " + str(file_path) + " ...")

init()
pipelineFacade = PipelineFacade(str(file_path))
pipelineFacade.processWOs()
print("Please check the outputs generated ...")