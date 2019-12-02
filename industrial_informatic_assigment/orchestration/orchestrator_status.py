import logging
import time
import explorerhat

#from industrial_informatic_assigment.enum.status_code import StatusCode
from industrial_informatic_assigment.enum.enum_variables import StatusCode


class OrchestratorStatus:

    def __init__(self):
        self.status = StatusCode.IDLE
        self.changeColor(self.status)

    def blink(self):
        print("Thread: Status Code Routine Started")
        while True:
            if self.status == StatusCode.WORKING:  # green blinking
                explorerhat.light[3].on()
                time.sleep(1)
                explorerhat.light[3].off()
            time.sleep(1)

    def changeColor(self, status: StatusCode):
        self.status = status
        if status == StatusCode.WORKING:
            explorerhat.light[1].off()
            explorerhat.light[2].off()
        elif status == StatusCode.ERROR:
            explorerhat.light[1].off()
            explorerhat.light[2].on()
            explorerhat.light[3].off()
        elif status == StatusCode.IDLE:
            explorerhat.light[1].on()
            explorerhat.light[2].off()
            explorerhat.light[3].off()
