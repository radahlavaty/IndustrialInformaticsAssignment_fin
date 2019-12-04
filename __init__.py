import json
import threading

from flask import Flask, request

# Logging
from enum_variables import Zone
from enum_variables import PalletStatus
from orchestrator_input import OrchestratorInput
from orchestrator_rpi import Orchestrator
from orchestrator_status import OrchestratorStatus
from subscriber import Subscriber
from workstation import Workstation

# Workstations
workstationBaseUrl = "http://192.168.2"
workstation_obj = Workstation(workstationBaseUrl, None)

# Subscribers
raspberryPiAddress = "http://192.168.0.114:5000"
sub = Subscriber(raspberryPiAddress)
#sub.subscribeToAllEventsOfWS(workstation_obj)

# Orchestration
orchestratorStatus = OrchestratorStatus()
orchestrator = Orchestrator(orchestratorStatus, workstation_obj)
orchestratorInput = OrchestratorInput(orchestrator)

# Flask Application
app = Flask(__name__)


def runFlaskApp():
    if __name__ == '__main__':
        app.run("0.0.0.0")


# Threads
threadOrchestration = threading.Thread(target=orchestrator.runOrchestration, args=())
threadOrchestrationInput = threading.Thread(target=orchestratorInput.startWaitingForActions, args=())
threadOrchestrationStatus = threading.Thread(target=orchestratorStatus.blink, args=())
threadFlask = threading.Thread(target=runFlaskApp, args=())

threadOrchestration.start()
threadOrchestrationStatus.start()
threadFlask.start()
threadOrchestrationInput.start()


# API Event Endpoints
@app.route('/rest/events/ws/<string:wsId>/PenChangeEnd/info', methods=['POST'])
def penSelectEndEventAPI(wsId):
    print("Event: Pen Selected End WS(" + wsId + ")")
    content = request.json
    orchestrator.penSelectEndEvent()
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/PenChangeStart/info', methods=['POST'])
def penSelectStartEventAPI(wsId):
    print("Event: Pen Selected Start WS(" + wsId + ")")
    orchestrator.penSelectStartEvent()
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/DrawStartExecution/info', methods=['POST'])
def drawStartEventAPI(wsId):
    print("Event: Drawing Start WS(" + wsId + ")")
    orchestrator.drawStartEvent()
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/DrawEndExecution/info', methods=['POST'])
def drawEventAPI(wsId):
    print("Event: Drawing End WS(" + wsId + ")")
    orchestrator.drawEndEvent()
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z1_Changed/info', methods=['POST'])
def zone1EventAPI(wsId):
    print("Event: Zone 1 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    if payload["PalletID"] == -1:
        return cnvMsg_str
    if orchestrator.testIfZoneFree(Zone.Z1):
        return cnvMsg_str
    if len(orchestrator.bufferOrder) >= 1:
        orchestrator.addPhoneToPallet(payload["PalletID"], orchestrator.bufferOrder.pop())
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z2_Changed/info', methods=['POST'])
def zone2EventAPI(wsId):
    print("Event: Zone 2 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    if payload["PalletID"] == -1:
        return cnvMsg_str
    pallet = orchestrator.getPalletWithStatus(PalletStatus.MOVING_TO_Z2)
    if pallet is None:
        return cnvMsg_str
    pallet.locationZone = Zone.Z2
    pallet.status = PalletStatus.WAITING
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z3_Changed/info', methods=['POST'])
def zone3EventAPI(wsId):
    print("Event: Zone 3 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    if payload["PalletID"] == -1:
        return cnvMsg_str
    pallet = orchestrator.getPalletWithStatus(PalletStatus.MOVING_TO_Z3)
    if pallet is None:
        return cnvMsg_str
    pallet.locationZone = Zone.Z3
    pallet.status = PalletStatus.WAITING
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z4_Changed/info', methods=['POST'])
def zone4EventAPI(wsId):
    print("Event: Zone 4 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    if payload["PalletID"] == -1:
        return cnvMsg_str
    pallet = orchestrator.getPalletWithStatus(PalletStatus.MOVING_TO_Z4)
    if pallet is None:
        return cnvMsg_str
    pallet.locationZone = Zone.Z4
    pallet.status = PalletStatus.WAIT_FOR_MOVING
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z5_Changed/info', methods=['POST'])
def zone5EventAPI(wsId):
    print("Event: Zone 5 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    if payload["PalletID"] == -1 or payload["PalletID"] == str("-1"):
        pallet = orchestrator.getPalletWithStatus(PalletStatus.WAITING)
        if pallet is None:
            return cnvMsg_str
        orchestrator.ws.pallets.remove(pallet)
        print("Orchestrator object: remove Pallet")
        return cnvMsg_str
    pallet = orchestrator.getPalletWithStatus(PalletStatus.MOVING_TO_Z5)
    if pallet is None:
        return cnvMsg_str
    pallet.locationZone = Zone.Z5
    pallet.status = PalletStatus.WAITING
    return cnvMsg_str
