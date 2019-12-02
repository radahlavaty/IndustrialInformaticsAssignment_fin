import json
import logging
import sqlite3
from threading import Lock

from industrial_informatic_assigment.enum.events import Events

class EventWS:
    def __init__(self, dbId, eventID, ws, senderID, payload, serverTime):
        self.id = dbId
        self.eventID = eventID
        self.ws = ws
        self.senderID = senderID
        self.payload = payload
        self.serverTime = serverTime

class MonitoringEventDAO:

    def __init__(self, inMemory):
        if inMemory:
            self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        else:
            self.conn = sqlite3.connect('monitoring.db', check_same_thread=False)

        self.conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        self.lock = Lock()
        self.c = self.conn.cursor()
        self.lock.acquire(True)
        self.c.execute("""CREATE TABLE IF NOT EXISTS event (
                     id INTEGER PRIMARY KEY,
                     eventID text,
                     ws text,
                     senderID text,
                     payload text,
                     serverTime timestamp
                     )""")
        self.lock.release()

    # DB operations
    def insert_event(self, event):
        print("MonitoringEventDAO: inserting new event")
        print(event)
        payload = json.dumps(event["payload"])

        with self.conn:
            self.lock.acquire(True)
            self.c.execute("""INSERT INTO event VALUES (NULL, :eventID, :ws, :senderID, :payload, :serverTime)""",
                           {'eventID': event["eventID"], 'ws': event["ws"], 'senderID': event['senderID'],
                            'payload': payload, 'serverTime': event["serverTime"]})
            self.lock.release()

    def display_all_events(self):
        print("Displaying all events in the DB...")
        allEvents = self.get_all_events()
        print(allEvents)

    def get_all_events(self):
        self.lock.acquire(True)
        self.c.execute("""SELECT * FROM event WHERE 1""")
        events = self.c.fetchall()
        self.lock.release()
        return events

    def getLastEvent(self, event: Events):
        self.lock.acquire(True)
        self.c.execute("SELECT * FROM event WHERE eventID = :eventID ORDER BY serverTime DESC LIMIT 1",
                       {"eventID": str(event.value)})
        eventDict = self.c.fetchone()
        self.lock.release()
        if eventDict is None:
            return None
        return EventWS(eventDict["id"], eventDict["eventID"], eventDict["ws"], eventDict["senderID"],
                       eventDict["payload"], eventDict["serverTime"])