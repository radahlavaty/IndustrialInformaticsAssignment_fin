import requests

from workstation import Workstation
from enum_variables import Zone


class Subscriber:
    def __init__(self, ownAdress):
        self.ownAdress = ownAdress
        self.baseService = "/rest/events"
        self.port = ""

    def subscribeToZoneChange(self, hostIP, zone: Zone, endpoint):
        URL = hostIP + self.port + self.baseService + "/Z" + str(zone.value) + "_Changed/notifs"
        destUrl = self.ownAdress + endpoint
        rqst = requests.post(URL, json={"destUrl": destUrl})

        if rqst.status_code != 200:
            print(
                "Subscriber object: subscribe to Zone " + str(zone.value) + ", IP: " + hostIP + " Status Code: " + str(
                    rqst.status_code))
        else:
            print("Subscriber object: subscribe to Zone " + str(zone.value) + " SUCCESS")

    def subscribeToPenChangeStart(self, hostIP, endpoint):
        URL = hostIP + self.port + self.baseService + "/PenChangeStarted/notifs"
        destUrl = self.ownAdress + endpoint
        rqst = requests.post(URL, json={"destUrl": destUrl})

        if rqst.status_code != 200:
            print("Subscriber object: subscribe to pen change start FAIL, IP: " + hostIP + " Status Code: " + str(
                rqst.status_code))
        else:
            print("Subscriber object: subscribe to  pen change start SUCCESS")

    def subscribeToPenChangeEnd(self, hostIP, endpoint):
        URL = hostIP + self.port + self.baseService + "/PenChangeEnded/notifs"
        destUrl = self.ownAdress + endpoint
        rqst = requests.post(URL, json={"destUrl": destUrl})

        if rqst.status_code != 200:
            print("Subscriber object: subscribe to pen change end FAIL, IP: " + hostIP + " Status Code: " + str(
                rqst.status_code))
        else:
            print("Subscriber object: subscribe to  pen change end SUCCESS")

    def subscribeToDrawingStart(self, hostIP, endpoint):
        URL = hostIP + self.port + self.baseService + "/DrawStartExecution/notifs"
        destUrl = self.ownAdress + endpoint
        rqst = requests.post(URL, json={"destUrl": destUrl})

        if rqst.status_code != 200:
            print("Subscriber object: subscribe to drawing start FAIL, IP: " + hostIP + " Status Code: " + str(
                rqst.status_code))
        else:
            print("Subscriber object: subscribe to drawing start SUCCESS")

    def subscribeToDrawingEnd(self, hostIP, endpoint):
        URL = hostIP + self.port + self.baseService + "/DrawEndExecution/notifs"
        destUrl = self.ownAdress + endpoint
        rqst = requests.post(URL, json={"destUrl": destUrl})

        if rqst.status_code != 200:
            print(
                "Subscriber object: subscribe to drawing FAIL IP: " + hostIP + " Status Code: " + str(rqst.status_code))
        else:
            print("Subscriber object: subscribe to drawing end SUCCESS")

    def subscribeToAllEventsOfWS(self, ws: Workstation):
        self.subscribeToDrawingEnd(ws.baseIp + ".1", "/rest/events/DrawEndExecution")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z1, "/rest/events/Z1_Changed")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z2, "/rest/events/Z2_Changed")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z3, "/rest/events/Z3_Changed")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z4, "/rest/events/Z4_Changed")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z5, "/rest/events/Z5_Changed")

    def subscribeToAllEventsOfWsSimple(self, ws: Workstation):
        endpointName = "/event"
        self.subscribeToPenChangeEnd(ws.baseIp + ".1", "/rest" + endpointName)
        self.subscribeToPenChangeStart(ws.baseIp + ".1", "/rest" + endpointName)
        self.subscribeToDrawingStart(ws.baseIp + ".1", "/rest" + str(ws.getUUID()) + endpointName)
        self.subscribeToDrawingEnd(ws.baseIp + ".1", "/rest" + str(ws.getUUID()) + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z1, "/rest" + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z2, "/rest" + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z3, "/rest" + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z4, "/rest" + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z5, "/rest" + endpointName)
