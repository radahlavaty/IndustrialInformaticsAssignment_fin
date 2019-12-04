import datetime
import json

from flask import Flask, render_template
from flask import request

from monitor_event_data import MonitoringEventDAO
from subscriber import Subscriber
from workstation import Workstation

# Workstation
workstationBaseUrl = "http://192.168.2"
ws = Workstation(workstationBaseUrl, None)

# Subscriber
locPort = 5000
serverAddress = "http://192.168.105.203:" + str(locPort)
subscriber = Subscriber(serverAddress)
subscriber.subscribeToAllEventsOfWsSimple(ws)

# DB
eventDAO = MonitoringEventDAO()

app = Flask(__name__)


@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)


# Events API

# Add event
@app.route('/rest/event', methods=['POST'])
def postEvent():
    eventDesc = request.json

    serverTime = datetime.datetime.now()
    eventDic = {"eventID": eventDesc['id'], "senderID": eventDesc['senderID'],
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


@app.route('/rest/events/time/<timestamp>', methods=['GET'])
def getEventsNewer(timestamp):
    print("Retrieving all the events...")
    allEvents = eventDAO.getNewerEvents(timestamp)
    allEventsJson = json.dumps(allEvents)
    return allEventsJson


if __name__ == '__main__':
    # checkTimeElapsedAlarms()

    app.run("0.0.0.0", locPort)
