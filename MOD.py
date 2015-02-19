import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])


import CompuCellSetup
sim,simthread = CompuCellSetup.getCoreSimulationObjects()

import CompuCell #notice importing CompuCell to main script has to be done after call to getCoreSimulationObjects()

CompuCellSetup.initializeSimulationObjects(sim,simthread)
            
# add extra attributes here            
# Definitions of additional Python-managed fields go here        
#Add Python steppables here

from PySteppablesExamples import SteppableRegistry
steppableRegistry=SteppableRegistry()      

# from mouseOvarianDevelopmentSteppables import VolumeParamSteppable
# volumeParamSteppable=VolumeParamSteppable(sim,10)
# steppableRegistry.registerSteppable(volumeParamSteppable)        

from MODSteppables import MitosisSteppable
mitosisSteppable=MitosisSteppable(sim,1)
steppableRegistry.registerSteppable(mitosisSteppable)

from MODSteppables import secretionSteppable
secretionSteppable=secretionSteppable(_simulator=sim,_frequency=1)
steppableRegistry.registerSteppable(secretionSteppable)


CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)
        
        
