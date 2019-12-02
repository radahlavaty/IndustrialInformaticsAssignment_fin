import uuid

from industrial_informatic_assigment.workstation.workstation import Workstation
from industrial_informatic_assigment.workstation.phone import Phone
from industrial_informatic_assigment.enum.zone import Zone
#from industrial_informatic_assigment.enum.pallet_status import PalletStatus

from industrial_informatic_assigment.enum.enum_variables import Zone, PalletStatus

class Pallet:

    def __init__(self, phone: Phone, locationWS: Workstation, locationZone: Zone):
        self.palletID = uuid.uuid4()        # generate new ID
        self.phone = phone
        self.locationWS = locationWS
        self.locationZone = locationZone
        self.frameDone = False
        self.screenDone = False
        self.keyboardDone = False
        self.status = PalletStatus.WAITING
        print("Initialization: new pallet with ID:(" + str(self.palletID) + ")")

    def printPalletInfo(self):
        print("PALLET - palletID:" + str(self.palletID) +
                        " Zone: " + str(self.locationZone) +
                        " Status: " + str(self.status.name))
