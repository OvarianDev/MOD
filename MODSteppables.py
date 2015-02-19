from PySteppables import *
from PySteppablesExamples import MitosisSteppableBase
import CompuCell
import sys
from random import uniform
import math
from PlayerPython import *
from math import *

#Chemotaxis and volume parameters are defined in the xml file of this version
#
# class VolumeParamSteppable(SteppableBasePy):
#     def __init__(self,_simulator,_frequency=1):
#         SteppablePy.__init__(self,_frequency)
#         self.simulator=_simulator
#         self.inventory=self.simulator.getPotts().getCellInventory()
#         self.cellList=CellList(self.inventory)
#     def start(self):
#         for cell in self.cellList:
#             cell.targetVolume=20 
#             cell.lambdaVolume=1.0 
#     def step(self,mcs):
#         for cell in self.cellList:
#             cell.targetVolume+=1

class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,_simulator,_frequency=1):
        MitosisSteppableBase.__init__(self,_simulator, _frequency)                
        # 0 - parent child position will be randomized between mitosis event
        # negative integer - parent appears on the 'left' of the child
        # positive integer - parent appears on the 'right' of the child
        self.setParentChildPositionFlag(-1)       
    
    def step(self,mcs):
        # print "INSIDE MITOSIS STEPPABLE"
        cells_to_divide=[]
        for cell in self.cellListByType(1):
            if cell.volume> 7: #
                cells_to_divide.append(cell)
            if mcs > 400:
                self.frequency = 1000
                
        for cell in cells_to_divide:
            # to change mitosis mode leave one of the below lines uncommented
            self.divideCellRandomOrientation(cell)
            # self.divideCellOrientationVectorBased(cell,1,0,0)                 
            # self.divideCellAlongMajorAxis(cell)                               
            # self.divideCellAlongMinorAxis(cell)                              

    def updateAttributes(self):
        parentCell=self.mitosisSteppable.parentCell
        childCell=self.mitosisSteppable.childCell
        
        childCell.targetVolume=parentCell.targetVolume
        childCell.lambdaVolume=parentCell.lambdaVolume
        if parentCell.type==1:
            childCell.type=1 

class secretionSteppable(SecretionBasePy):
    def __init__(self,_simulator,_frequency=1):
        SecretionBasePy.__init__(self,_simulator,_frequency)

    def step(self,mcs):
        # Get the ckit field
        field=self.getConcentrationField('ckit')
        ckitSecretor=self.getFieldSecretor('ckit')        

        speed_of_signal = 100
        currentcell = ceil(mcs/speed_of_signal) + 1
        print currentcell
        # maybe if this variable is called "currentcell" and is equal to approximately 1/100 of the current mcs, then it would not need to be incremented each time
        # so currentcell = 1 for 1-100 mcs, 2 for 101-200 mcs, etc.
        # then every time we do something to currentcell, it will automatically be checking where we're at in the timestream
        # currentcell gets a secretion rate; currentcell-1 will get 0 secretion
        # what if currentcell = 1 and currencell-1 = 0?

        for cell in self.cellListByType(2): # iterate through only the signaling cells
            if cell.id ==currentcell:
                ckitSecretor.secreteOutsideCellAtBoundary(cell,10) # Secretion outside at boundary represents surface expression of ligand
#            if cell.id > 3
#                    ckitSecretor.secreteOutsideCellAtBoundary(cell,0) 
#            if currentcell > 1:
#                if cell.id == currentcell-1:
#                    ckitSecretor.secreteOutsideCellAtBoundary(cell,0) # turn off secretion
#            if currentcell == 1:
#                if cell.id == 3:
#                    ckitSecretor.secreteOutsideCellAtBoundary(cell,0) # turn off secretion
