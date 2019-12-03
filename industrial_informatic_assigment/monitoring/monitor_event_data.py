import json
import sqlite3
from threading import Lock

from industrial_informatic_assigment.enum.enum_variables import Events

class EventWS:
    def __init__(self, dbId, eventID, ws, senderID, payload, serverTime):
        self.id = dbId
        self.eventID = eventID
        self.ws = ws
        self.senderID = senderID
        self.payload = payload
        self.serverTime = serverTime

class MonitoringEventDAO:

    # connection to database
    def __init__(self, inMemory):
        #if inMemory:
        #   self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        #else:
        #   self.conn = sqlite3.connect('monitoring.db', check_same_thread=False)

        self.conn = sqlite3.connect('monitoring.db', check_same_thread=False)   # getting connection to database

        # easier to access a dictionary - { "1" , "txt" } vs {"id":"1", "description":"txt"}
        self.conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        self.lock = Lock()  #important in multithreading
        self.c = self.conn.cursor() # getting cursor in a database
        self.lock.acquire(True) # acquire semaphore

        # SQL - executing in database - CREATE A TABLE
        # if already exist - dont do it again "IF NOT EXISTS"
        self.c.execute("""CREATE TABLE IF NOT EXISTS event (
                     id INTEGER PRIMARY KEY,
                     eventID text,
                     ws text,
                     senderID text,
                     payload text,
                     serverTime timestamp
                     )""")

        self.lock.release() # release semaphore

    # DB operations
    def insert_event(self, event):
        print("MonitoringEventDAO: inserting new event")
        print(event)
        payload = json.dumps(event["payload"])

        with self.conn:
            self.lock.acquire(True)

            #SQL statement - id = NULL, eventID - from rquist... possible to put string together
            self.c.execute("""INSERT INTO event VALUES (NULL, :eventID, :ws, :senderID, :payload, :serverTime)""",
                           {'eventID': event["eventID"], 'ws': event["ws"], 'senderID': event['senderID'],
                            'payload': payload, 'serverTime': event["serverTime"]})

            self.lock.release()

    # dont need this !!! - just showing events on console
    def display_all_events(self):
        print("Displaying all events in the DB...")
        allEvents = self.get_all_events()
        print(allEvents)



    def get_all_events(self):
        self.lock.acquire(True) # from threading library - acquire

        # 1 - possible without "WHERE 1" - but possible error
        self.c.execute("""SELECT * FROM event WHERE 1""")
        events = self.c.fetchall() # say to database that I want all data form database to me

        self.lock.release() #

        return events

    # if I need current event = last event
    def getLastEvent(self, event: Events):
        self.lock.acquire(True)

        # take all events and put them to order
        self.c.execute("SELECT * FROM event WHERE eventID = :eventID ORDER BY serverTime DESC LIMIT 1",
                       {"eventID": str(event.value)})
        eventDict = self.c.fetchone() # same like fetchall, but I will get just one last

        self.lock.release()

        if eventDict is None:
            return None

        return EventWS(eventDict["id"], eventDict["eventID"], eventDict["ws"], eventDict["senderID"],
                       eventDict["payload"], eventDict["serverTime"])






