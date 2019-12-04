import requests

from industrial_informatic_assigment.workstation.workstation import Workstation
from industrial_informatic_assigment.enum.enum_variables import Zone

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
            print("Subscriber object: subscribe to Zone " + str(zone.value) + ", IP: " + hostIP + " Status Code: " + str(rqst.status_code))
        else:
            print("Subscriber object: subscribe to Zone " + str(zone.value) + "SUCCESS")

    def subscribeToPenChangeStart(self, hostIP, endpoint):
        URL = hostIP + self.port + self.baseService + "/PenChangeStarted/notifs"
        destUrl = self.ownAdress + endpoint
        rqst = requests.post(URL, json={"destUrl": destUrl})

        if rqst.status_code != 200:
            print("Subscriber object: subscribe to pen change start FAIL, IP: " + hostIP + " Status Code: " + str(rqst.status_code))
        else:
            print("Subscriber object: subscribe to  pen change start SUCCESS")

    def subscribeToPenChangeEnd(self, hostIP, endpoint):
        URL = hostIP + self.port + self.baseService + "/PenChangeEnded/notifs"
        destUrl = self.ownAdress + endpoint
        rqst = requests.post(URL, json={"destUrl": destUrl})

        if rqst.status_code != 200:
            print("Subscriber object: subscribe to pen change end FAIL, IP: " + hostIP + " Status Code: " + str(rqst.status_code))
        else:
            print("Subscriber object: subscribe to  pen change end SUCCESS")

    def subscribeToDrawingStart(self, hostIP, endpoint):
        URL = hostIP + self.port + self.baseService + "/DrawStartExecution/notifs"
        destUrl = self.ownAdress + endpoint
        rqst = requests.post(URL, json={"destUrl": destUrl})

        if rqst.status_code != 200:
            print("Subscriber object: subscribe to drawing start FAIL, IP: " + hostIP + " Status Code: " + str(rqst.status_code))
        else:
            print("Subscriber object: subscribe to drawing start SUCCESS")

    def subscribeToDrawingEnd(self, hostIP, endpoint):
        URL = hostIP + self.port + self.baseService + "/DrawEndExecution/notifs"
        destUrl = self.ownAdress + endpoint
        rqst = requests.post(URL, json={"destUrl": destUrl})

        if rqst.status_code != 200:
            print("Subscriber object: subscribe to drawing FAIL IP: " + hostIP + " Status Code: " + str(rqst.status_code))
        else:
            print("Subscriber object: subscribe to drawing end SUCCESS")


    def subscribeToAllEventsOfWS(self, ws: Workstation):
        self.subscribeToPenChangeEnd(ws.baseIp + ".1", "/rest/events/ws/" + str(ws.getUUID()) + "/PenChangeEnd/info")
        self.subscribeToPenChangeStart(ws.baseIp + ".1",
                                       "/rest/events/ws/" + str(ws.getUUID()) + "/PenChangeStart/info")
        self.subscribeToDrawingStart(ws.baseIp + ".1",
                                     "/rest/events/ws/" + str(ws.getUUID()) + "/DrawStartExecution/info")
        self.subscribeToDrawingEnd(ws.baseIp + ".1", "/rest/events/ws/" + str(ws.getUUID()) + "/DrawEndExecution/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z1,
                                   "/rest/events/ws/" + str(ws.getUUID()) + "/Z1_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z2,
                                   "/rest/events/ws/" + str(ws.getUUID()) + "/Z2_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z3,
                                   "/rest/events/ws/" + str(ws.getUUID()) + "/Z3_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z4,
                                   "/rest/events/ws/" + str(ws.getUUID()) + "/Z4_Changed/info")
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z5,
                                   "/rest/events/ws/" + str(ws.getUUID()) + "/Z5_Changed/info")

    def subscribeToAllEventsOfWsSimple(self, ws: Workstation):
        endpointName = "/event"
        self.subscribeToPenChangeEnd(ws.baseIp + ".1", "/rest/ws/" + str(ws.getUUID()) + endpointName)
        self.subscribeToPenChangeStart(ws.baseIp + ".1", "/rest/ws/" + str(ws.getUUID()) + endpointName)
        self.subscribeToDrawingStart(ws.baseIp + ".1", "/rest/ws/" + str(ws.getUUID()) + endpointName)
        self.subscribeToDrawingEnd(ws.baseIp + ".1", "/rest/ws/" + str(ws.getUUID()) + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z1, "/rest/ws/" + str(ws.getUUID()) + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z2, "/rest/ws/" + str(ws.getUUID()) + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z3, "/rest/ws/" + str(ws.getUUID()) + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z4, "/rest/ws/" + str(ws.getUUID()) + endpointName)
        self.subscribeToZoneChange(ws.baseIp + ".2", Zone.Z5, "/rest/ws/" + str(ws.getUUID()) + endpointName)
