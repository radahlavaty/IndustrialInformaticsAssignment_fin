import time
import explorerhat

from orchestrator_rpi import Orchestrator
from workstation import Phone
from enum_variables import PhoneColor, PhoneShape


class OrchestratorInput:

    def __init__(self, orchestrator: Orchestrator):
        self.phone = Phone(PhoneShape.FRAME_1, PhoneShape.KEYBOARD_1, PhoneShape.SCREEN_1)
        self.state = 0
        self.selected = False
        self.orchestrator = orchestrator
        self.okButton = 5

    def startWaitingForActions(self):
        explorerhat.touch.pressed(self.changeState)
        print("OrchestratorInput object: Listening to button inputs started")
        while True:
            if self.state == 0:
                explorerhat.light[0].off()
                time.sleep(0.1)
            elif self.state == 4:
                explorerhat.light[0].on()
                time.sleep(0.2)
                explorerhat.light[0].off()
                time.sleep(0.2)
            else:
                explorerhat.light[0].on()
                time.sleep(0.5)
                explorerhat.light[0].off()
                time.sleep(0.5)

    def changeState(self, button, event):
        print("OrchestratorInput object: Button pressed: " + str(button))
        if self.state == 0:
            if button == self.okButton:
                self.state = 1
        elif self.state == 1:
            self.selectFrameState(button)
        elif self.state == 2:
            self.selectScreenState(button)
        elif self.state == 3:
            self.selectKeyboardState(button)
        elif self.state == 4:
            if button == 6:
                print("OrchestratorInput object: Phone")
                self.phone.printPhoneInfo()
                self.orchestrator.addOrder(self.phone)
                self.state = 0

    def selectFrameState(self, button):
        print("OrchestratorInput object: select frame shape.")
        if button == 1:
            self.phone.frameShape = PhoneShape.FRAME_1
            self.state = 2
        elif button == 2:
            self.phone.frameShape = PhoneShape.FRAME_2
            self.state = 2
        elif button == 3:
            self.phone.frameShape = PhoneShape.FRAME_3
            self.state = 2

    def selectScreenState(self, button):
        print("OrchestratorInput object: select screen shape")

        if button == 1:
            self.phone.screenShape = PhoneShape.SCREEN_1
            self.state = 3
        elif button == 2:
            self.phone.screenShape = PhoneShape.SCREEN_2
            self.state = 3
        elif button == 3:
            self.phone.screenShape = PhoneShape.SCREEN_3
            self.state = 3

    def selectKeyboardState(self, button):
        print("OrchestratorInput object: select keyboard shape")
        if button == 1:
            self.phone.keyboardShape = PhoneShape.KEYBOARD_1
            self.state = 4
        elif button == 2:
            self.phone.keyboardShape = PhoneShape.KEYBOARD_2
            self.state = 4
        elif button == 3:
            self.phone.keyboardShape = PhoneShape.KEYBOARD_3
            self.state = 4

    def resetPhone(self):
        self.state = 0
