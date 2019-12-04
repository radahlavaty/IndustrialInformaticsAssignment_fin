import uuid
import requests

# from industrial_informatic_assigment.workstation.conveyor import Conveyor
# from industrial_informatic_assigment.workstation.robot import Robot
# from industrial_informatic_assigment.workstation.phone import Phone
from industrial_informatic_assigment.enum.enum_variables import PhoneShape, PhoneColor, Zone, PalletStatus

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


class Robot:
    def __init__(self, hostIP):
        self.robotID = uuid.uuid4()     # generate new ID
        self.hostIP = hostIP
        self.baseService = "/rest/services"
        print("Initialization - New robot  with ID: (" + str(self.robotID) + ")")

    def calibrateRobot(self):
        URL = self.hostIP + self.baseService + "/Calibrate"
        header = { 'content-type': 'application/json' }
        rqst = requests.post(URL, json = {}, headers = header)

    def getPenColor(self):
        print("Robot: get pen color")

        URL = self.hostIP + self.baseService + "/GetPenColor"

        rqst = requests.post(URL, json={})
        print(rqst.json())

        response = rqst.json()

        if response["CurrentPen"] == "red":
            return PhoneColor.RED

        if response["CurrentPen"] == "green":
            return PhoneColor.GREEN

        if response["CurrentPen"] == "blue":
            return PhoneColor.BLUE

    def selectPen(self, color: PhoneColor):
        colorUrlValue = ""

        if color == PhoneColor.RED:
            colorUrlValue = "ChangePenRED"
        elif color == PhoneColor.GREEN:
            colorUrlValue = "ChangePenGREEN"
        elif color == PhoneColor.BLUE:
            colorUrlValue = "ChangePenBLUE"

        URL = self.hostIP + self.baseService + "/" + colorUrlValue

        rqst = requests.post(URL, json = {"destUrl": ""})

        if rqst.status_code == 202:
            print("Robot: select pen SUCCESS, color: " + str(color.name))
        else:
            print("Robot: select pen FAIL, color: " + str(color.name) + ", Status Code: " + str(rqst.status_code))

    def executeDrawing(self, shape: PhoneShape, color: PhoneColor):
        if color != self.getPenColor():
            print("Robot: color selection FAIL")

        URL = self.hostIP + self.baseService + "/" + shape.value

        rqst = requests.post(URL, json={"destUrl": ""})

        if rqst.status_code == 202:
            print("Robot: execute drawing SUCCESS, color: " + str(color.name))
        else:
            print("Robot: execute drawing FAIL, color: " + str(color.name) + ", shape: " + str(shape.name) + " Status Code: " + str(rqst.status_code))

class Conveyor:

    def __init__(self, hostIP):
        self.conveyorID = uuid.uuid4()      # generate new ID
        self.hostIP = hostIP
        self.baseService = "/rest/services"
        print("Initialization: New conveyor with ID: (" + str(self.conveyorID) + ")")

    def movePallet(self, zoneStart: Zone, zoneEnd: Zone):
        URL = self.hostIP + self.baseService + "/TransZone" + str(zoneStart.value) + str(zoneEnd.value)
        rqst = requests.post(URL, json={"destUrl": ""})

        if rqst.status_code == 202:
            print("Conveyor object: move pallet successful (Z" + str(zoneStart.value) + " to " + str(zoneEnd.value) + ")")
        else:
            print("Conveyor object: move pallet error (Z" + str(zoneStart.value) + " to " + str(zoneEnd.value) + ") Status Code: " + str(rqst.status_code))

    def getZoneStatus(self, zone: Zone):
        URL = self.hostIP + self.baseService + "/Z" + str(zone.value)
        rqst = None

        if zone == Zone.Z1:
            rqst = requests.get(URL, json={"destUrl": ""})
        else:
            rqst = requests.post(URL, json={"destUrl": ""})

        if rqst.status_code != 200:
            print("Conveyor object: get zone status FAIL (Z: " + str(zone.value) + ")")

        reqMsg = rqst.json()
        palletID = reqMsg["PalletID"]

        return palletID


class Phone:
    def __init__(self, frameShape: PhoneShape, keyboardShape: PhoneShape, screenShape: PhoneShape, color: PhoneColor):
        self.frameShape = frameShape
        self.keyboardShape = keyboardShape
        self.screenShape = screenShape
        self.color = color

    def printPhoneInfo(self):
        print("PHONE -  Frame: " + str(self.frameShape.value) + " Keyboard: " + str(self.keyboardShape.value) + " Screen: " + str(self.screenShape.value) + " Color:" + str(self.color.name))



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
        print("PALLET - palletID:" + str(self.palletID) + " Zone: " + str(self.locationZone) + " Status: " + str(self.status.name))