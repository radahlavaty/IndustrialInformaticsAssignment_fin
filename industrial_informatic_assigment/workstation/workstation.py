import uuid
from industrial_informatic_assigment.workstation.conveyor import Conveyor
from industrial_informatic_assigment.workstation.robot import Robot


class Workstation:

    def __init__(self, baseIp, nextWS):
        self.workstationID = uuid.uuid4()       # generate new ID

        self.robot = Robot(baseIp + ".1")
        self.conveyor = Conveyor(baseIp + ".2")
        self.pallets = []
        self.baseIp = baseIp
        self.nextWS = nextWS

        print("Initialization: new workstation  (" + str(self.workstationID) + ")")

    def addPallet(self, pallet):
        if len(self.pallets) >= 5:
            print("MAXIMUM PALLETS in a workstation!")
            return False
        else:
            self.pallets.append(pallet)
            return True

    def removePallet(self):
        if len(self.pallets) > 0:
            return self.pallets.pop(0)
        else:
            print("NO PALLET in a workstation")
            return

    def getUUID(self):
        return str(self.workstationID)
