import json
import threading

from flask import Flask, request

# Logging
from industrial_informatic_assigment.orchestration.orchestrator_input import OrchestratorInput
from industrial_informatic_assigment.orchestration.orchestrator_rpi import Orchestrator
from industrial_informatic_assigment.orchestration.orchestrator_status import OrchestratorStatus
from industrial_informatic_assigment.workstation.subsciber import Subscriber
from industrial_informatic_assigment.workstation.workstation import Workstation

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
    orchestrator.zone1Event(payload["PalletID"])
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z2_Changed/info', methods=['POST'])
def zone2EventAPI(wsId):
    print("Event: Zone 2 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    orchestrator.zone2Event(payload["PalletID"])
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z3_Changed/info', methods=['POST'])
def zone3EventAPI(wsId):
    print("Event: Zone 3 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    orchestrator.zone3Event(payload["PalletID"])
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z4_Changed/info', methods=['POST'])
def zone4EventAPI(wsId):
    print("Event: Zone 4 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    orchestrator.zone4Event(payload["PalletID"])
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z5_Changed/info', methods=['POST'])
def zone5EventAPI(wsId):
    print("Event: Zone 5 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    orchestrator.zone5Event(payload["PalletID"])
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str
