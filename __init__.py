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
sub.subscribeToAllEventsOfWS(workstation_obj)

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
@app.route('/rest/events/DrawEndExecution', methods=['POST'])
def drawEventAPI():
    print("Event: Drawing End")
    orchestrator.drawEndEvent()
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/Z1_Changed', methods=['POST'])
def zone1EventAPI():
    print("Event: Zone 1 Changed")
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


@app.route('/rest/events/Z2_Changed', methods=['POST'])
def zone2EventAPI():
    print("Event: Zone 2 Changed")
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


@app.route('/rest/events/Z3_Changed', methods=['POST'])
def zone3EventAPI():
    print("Event: Zone 3 Changed")
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


@app.route('/rest/events/Z4_Changed', methods=['POST'])
def zone4EventAPI():
    print("Event: Zone 4 Changed")
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
    pallet.status = PalletStatus.WAITING
    return cnvMsg_str


@app.route('/rest/events/Z5_Changed', methods=['POST'])
def zone5EventAPI():
    print("Event: Zone 5 Changed")
    content = request.json
    payload = content["payload"]
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    if payload["PalletID"] == -1 or payload["PalletID"] == str("-1"):
        pallet = orchestrator.getPalletFromZone(Zone.Z5)
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
