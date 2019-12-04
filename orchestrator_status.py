import time
import explorerhat

from enum_variables import StatusCode


class OrchestratorStatus:

    def __init__(self):
        self.status = StatusCode.IDLE
        self.changeLightColor(self.status)

    def blink(self):
        print("Thread: Status Code Routine Started")
        while True:
            if self.status == StatusCode.WORKING:  # green blinking
                explorerhat.light[3].on()
                time.sleep(1)
                explorerhat.light[3].off()
            time.sleep(1)

    def changeLightColor(self, status: StatusCode):
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
