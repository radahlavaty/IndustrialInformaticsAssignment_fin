import datetime
import json
import threading
import time

from flask import Flask, render_template
from flask import request

#from industrial_informatic_assigment.monitoring.monitoring_alarm_dao import MonitoringAlarmDAO
from industrial_informatic_assigment.monitoring.monitor_event_data import MonitoringEventDAO
#from industrial_informatic_assigment.monitoring.monitoring_service import MonitoringService
from industrial_informatic_assigment.workstation.subsciber import Subscriber
from industrial_informatic_assigment.workstation.workstation import Workstation


# Workstation
workstationBaseUrl = "http://192.168.2"
ws = Workstation(workstationBaseUrl, None)

# Subscriber
locPort = 5000
serverAddress = "http://192.168.101.200:" + str(locPort)
subscriber = Subscriber(serverAddress)
subscriber.subscribeToAllEventsOfWsSimple(ws)

# DB
eventDAO = MonitoringEventDAO(False)
#alarmDAO = MonitoringAlarmDAO(False)
# Service
# monitoringService = MonitoringService(eventDAO, alarmDAO)


app = Flask(__name__)


@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)

# Events API

# Add event
@app.route('/rest/ws/<string:wsId>/event', methods=['POST'])
def index(wsId):
    eventDesc = request.json

    serverTime = datetime.datetime.now()
    eventDic = {"eventID": eventDesc['id'], "ws": wsId, "senderID": eventDesc['senderID'],
                "payload": eventDesc['payload'], "serverTime": serverTime}
    eventDAO.insert_event(eventDic)

    resp = json.dumps({'thank': 'yes'}), 200, {'ContentType': 'application/json'}
    return resp


@app.route('/rest/events', methods=['GET'])
def getEvents():
    print("Retrieving all the events...")
    allEvents = eventDAO.get_all_events()
    allEventsJson = json.dumps(allEvents)
    return allEventsJson


# @app.route('/rest/ws/status', methods=['GET'])
# def getWsStatus():
#     status = monitoringService.getStatusOfWS()
#     cnvMsg_str = json.dumps(vars(status))
#     return cnvMsg_str


# @app.route('/rest/alarm', methods=['GET'])
# def getAllAlarms():
    # alarms = monitoringService.getAllAlarms()
    # cnvMsg_str = json.dumps(alarms)
    # return cnvMsg_str


# def detect_time_elapsed_alarms():
#     pass
    # logging.debug("Checking for time elapsed alarms...")
    # sqlSt="SELECT * FROM event WHERE 1"
    # c.execute(sqlSt)
    # allRobots=c.fetchall()
    # logging.info(allRobots)


# Find alarms
# def checkTimeElapsedAlarms():
    # logging.debug("Checking DB for alarms")
    # monitoringService.checkForNewAlarms()
    # threading.Timer(5.0, checkTimeElapsedAlarms).start()


if __name__ == '__main__':
    # checkTimeElapsedAlarms()

    app.run("0.0.0.0", locPort)
