import time
import explorerhat

from orchestrator_rpi import Orchestrator
from workstation import Phone
from enum_variables import PhoneColor, PhoneShape


class OrchestratorInput:

    def __init__(self, orchestrator: Orchestrator):
        self.phone = Phone(PhoneShape.FRAME_1, PhoneShape.KEYBOARD_1, PhoneShape.SCREEN_1, PhoneColor.RED)
        self.state = 0
        self.selected = False
        self.orchestrator = orchestrator
        self.okButton = 1

    def startWaitingForActions(self):
        explorerhat.touch.pressed(self.changeState)
        print("OrchestratorInput object: Listening to button inputs started")
        while True:
            if self.state == 0:
                explorerhat.light[0].off()
                time.sleep(0.1)
            elif self.state == 5:
                explorerhat.light[0].on()
                time.sleep(0.2)
                explorerhat.light[0].off()
                time.sleep(0.2)
            elif self.selected:
                explorerhat.light[0].on()
                time.sleep(0.1)
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
            self.selectColorState(button)
        elif self.state == 5:
            if button == self.okButton:
                print("OrchestratorInput object: Phone")
                self.phone.printPhoneInfo()
                self.orchestrator.addOrder(self.phone)
                self.state = 0

    def selectFrameState(self, button):
        print("OrchestratorInput object: select frame shape.")
        if button == self.okButton and self.selected:
            self.state = 2
            self.selected = False
        elif button == 2:
            self.phone.frameShape = PhoneShape.FRAME_1
            self.selected = True
        elif button == 3:
            self.phone.frameShape = PhoneShape.FRAME_2
            self.selected = True
        elif button == 4:
            self.phone.frameShape = PhoneShape.FRAME_3
            self.selected = True

    def selectScreenState(self, button):
        print("OrchestratorInput object: select screen shape")
        if button == self.okButton and self.selected:
            self.state = 3
            self.selected = False
        elif button == 2:
            self.phone.screenShape = PhoneShape.SCREEN_1
            self.selected = True
        elif button == 3:
            self.phone.screenShape = PhoneShape.SCREEN_2
            self.selected = True
        elif button == 4:
            self.phone.screenShape = PhoneShape.SCREEN_3
            self.selected = True

    def selectKeyboardState(self, button):
        print("OrchestratorInput object: select keyboard shape")
        if button == self.okButton and self.selected:
            self.state = 4
            self.selected = False
        elif button == 2:
            self.phone.keyboardShape = PhoneShape.KEYBOARD_1
            self.selected = True
        elif button == 3:
            self.phone.keyboardShape = PhoneShape.KEYBOARD_2
            self.selected = True
        elif button == 4:
            self.phone.keyboardShape = PhoneShape.KEYBOARD_3
            self.selected = True

    def selectColorState(self, button):
        print("OrchestratorInput object: select phone color")
        if button == self.okButton and self.selected:
            self.state = 5
            self.selected = False
        elif button == 2:
            self.phone.color = PhoneColor.RED
            self.selected = True
        elif button == 3:
            self.phone.color = PhoneColor.GREEN
            self.selected = True
        elif button == 4:
            self.phone.color = PhoneColor.BLUE
            self.selected = True

    def resetPhone(self):
        self.state = 0
