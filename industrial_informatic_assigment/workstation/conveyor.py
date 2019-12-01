import uuid
import requests
from industrial_informatic_assigment.enum.zone import Zone


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
            print("Conveyor: move pallet successful (Z" + str(zoneStart.value) + " to " + str(zoneEnd.value) + ")")
        else:
            print("Conveyor: move pallet error (Z" +
                  str(zoneStart.value) + " to " +
                  str(zoneEnd.value) + ") Status Code: " +
                  str(rqst.status_code))

    def getZoneStatus(self, zone: Zone):
        URL = self.hostIP + self.baseService + "/Z" + str(zone.value)
        rqst = None

        if zone == Zone.Z1:
            rqst = requests.get(URL, json={"destUrl": ""})
        else:
            rqst = requests.post(URL, json={"destUrl": ""})

        if rqst.status_code != 200:
            print("Conveyor: get zone status FAIL (Z: " + str(zone.value) + ")")

        reqMsg = rqst.json()
        palletID = reqMsg["PalletID"]

        return palletID
