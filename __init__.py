import json
import logging
import threading

from flask import Flask, request



# Logging
from industrial_informatic_assigment.orchestration.orchestrator_input import OrchestratorInput
from industrial_informatic_assigment.orchestration.orchestrator_rpi import Orchestrator
from industrial_informatic_assigment.orchestration.orchestrator_status import OrchestratorStatus
from industrial_informatic_assigment.workstation.subsciber import Subscriber
from industrial_informatic_assigment.workstation.workstation import Workstation

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Workstations
w2BaseUrl = "http://192.168.2"
w2 = Workstation(w2BaseUrl, None)

# Subscribers
raspberryPiAddress = "http://192.168.0.114:5000"
sub = Subscriber(raspberryPiAddress)
#sub.subscribeToAllEventsOfWS(w2)

# Orchestration
orchestratorStatus = OrchestratorStatus()
orchestrator = Orchestrator(orchestratorStatus, w2)
orchestratorInput = OrchestratorInput(orchestrator)

# Flask Application
app = Flask(__name__)


def runFlaskApp():
    if __name__ == '__main__':
        app.run("0.0.0.0")


# Threads
threadOrchestration = threading.Thread(target=orchestrator.runOrchestration, args=())
threadOrchestrationInput = threading.Thread(target=orchestratorInput.startListening, args=())
threadOrchestrationStatus = threading.Thread(target=orchestratorStatus.blink, args=())
threadFlask = threading.Thread(target=runFlaskApp, args=())

threadOrchestration.start()
threadOrchestrationStatus.start()
threadFlask.start()
threadOrchestrationInput.start()


# API Event Endpoints
@app.route('/rest/events/ws/<string:wsId>/PenChangeEnd/info', methods=['POST'])
def penSelectedEndEvent(wsId):
    logging.debug("Event: Pen Selected End WS(" + wsId + ")")
    content = request.json
    orchestrator.penSelectedEndEvent()
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/PenChangeStart/info', methods=['POST'])
def penSelectedStartEvent(wsId):
    logging.debug("Event: Pen Selected Start WS(" + wsId + ")")
    orchestrator.penSelectedStartEvent()
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/DrawStartExecution/info', methods=['POST'])
def drawingStartEvent(wsId):
    logging.debug("Event: Drawing Start WS(" + wsId + ")")
    orchestrator.drawingStartEvent()
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/DrawEndExecution/info', methods=['POST'])
def drawingEndEvent(wsId):
    logging.debug("Event: Drawing End WS(" + wsId + ")")
    orchestrator.drawingEndEvent()
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z1_Changed/info', methods=['POST'])
def zone1ChangedEvent(wsId):
    logging.debug("Event: Zone 1 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    orchestrator.zone1ChangedEvent(payload["PalletID"])
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z2_Changed/info', methods=['POST'])
def zone2ChangedEvent(wsId):
    logging.debug("Event: Zone 2 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    orchestrator.zone2ChangedEvent(payload["PalletID"])
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z3_Changed/info', methods=['POST'])
def zone3ChangedEvent(wsId):
    logging.debug("Event: Zone 3 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    orchestrator.zone3ChangedEvent(payload["PalletID"])
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z4_Changed/info', methods=['POST'])
def zone4ChangedEvent(wsId):
    logging.debug("Event: Zone 4 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    orchestrator.zone4ChangedEvent(payload["PalletID"])
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


@app.route('/rest/events/ws/<string:wsId>/Z5_Changed/info', methods=['POST'])
def zone5ChangedEvent(wsId):
    logging.debug("Event: Zone 5 Changed WS(" + wsId + ")")
    content = request.json
    payload = content["payload"]
    orchestrator.zone5ChangedEvent(payload["PalletID"])
    cnvMsg = {}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str
