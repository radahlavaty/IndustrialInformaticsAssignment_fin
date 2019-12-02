import uuid
import requests

#rom industrial_informatic_assigment.enum.phone_color import PhoneColor
#from industrial_informatic_assigment.enum.phone_shape import PhoneShape

from industrial_informatic_assigment.enum.enum_variables import PhoneShape, PhoneColor

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
            print(
                "Robot: select pen FAIL, color: " + str(color.name) + ", Status Code: " + str(rqst.status_code))

    def executeDrawing(self, shape: PhoneShape, color: PhoneColor):
        if color != self.getPenColor():
            print("Robot: color selection FAIL")

        URL = self.hostIP + self.baseService + "/" + shape.value

        rqst = requests.post(URL, json={"destUrl": ""})

        if rqst.status_code == 202:
            print("Robot: execute drawing SUCCESS, color: " + str(color.name))
        else:
            print("Robot: execute drawing FAIL, color: " + str(color.name) +
                  ", shape: " + str(shape.name) +
                  " Status Code: " + str(rqst.status_code))