import time
import explorerhat

from industrial_informatic_assigment.orchestration.orchestrator_rpi import Orchestrator
from industrial_informatic_assigment.workstation.phone import Phone
#from industrial_informatic_assigment.enum.phone_color import PhoneColor
#from industrial_informatic_assigment.enum.phone_shape import PhoneShape

from industrial_informatic_assigment.enum.enum_variables import PhoneColor, PhoneShape


class OrchestratorInput:

    def __init__(self, orchestrator: Orchestrator):
        self.phone = Phone(PhoneShape.FRAME_1, PhoneShape.KEYBOARD_1, PhoneShape.SCREEN_1, PhoneColor.RED)
        self.state = 0
        self.selected = False
        self.orchestrator = orchestrator
        self.okButton = 1

    def startListening(self):
        explorerhat.touch.pressed(self.changeState)
        print("Listening to button inputs started")
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
                time.sleep(0.6)
                explorerhat.light[0].off()
                time.sleep(0.6)

    def changeState(self, channel, event):
        print("OrchestratorInput: Button pressed: " + str(channel))
        if self.state == 0:
            if channel == self.okButton:
                self.state = 1
        elif self.state == 1:
            self.state1(channel)
        elif self.state == 2:
            self.state2(channel)
        elif self.state == 3:
            self.state3(channel)
        elif self.state == 4:
            self.state4(channel)
        elif self.state == 5:
            if channel == self.okButton:
                print("OrchestratorInput: Phone")
                self.phone.printPhoneInfo()
                self.orchestrator.addOrder(self.phone)
                self.state = 0

    def state1(self, channel):
        print("OrchestratorInput: select frame shape")
        if channel == self.okButton and self.selected:
            self.state = 2
            self.selected = False
        elif channel == 2:
            self.phone.frameShape = PhoneShape.FRAME_1
            self.selected = True
        elif channel == 3:
            self.phone.frameShape = PhoneShape.FRAME_2
            self.selected = True
        elif channel == 4:
            self.phone.frameShape = PhoneShape.FRAME_3
            self.selected = True

    def state2(self, channel):
        print("OrchestratorInput: select screen shape")
        if channel == self.okButton and self.selected:
            self.state = 3
            self.selected = False
        elif channel == 2:
            self.phone.screenShape = PhoneShape.SCREEN_1
            self.selected = True
        elif channel == 3:
            self.phone.screenShape = PhoneShape.SCREEN_2
            self.selected = True
        elif channel == 4:
            self.phone.screenShape = PhoneShape.SCREEN_3
            self.selected = True

    def state3(self, channel):
        print("OrchestratorInput: select keyboard shape")
        if channel == self.okButton and self.selected:
            self.state = 4
            self.selected = False
        elif channel == 2:
            self.phone.keyboardShape = PhoneShape.KEYBOARD_1
            self.selected = True
        elif channel == 3:
            self.phone.keyboardShape = PhoneShape.KEYBOARD_2
            self.selected = True
        elif channel == 4:
            self.phone.keyboardShape = PhoneShape.KEYBOARD_3
            self.selected = True

    def state4(self, channel):
        print("OrchestratorInput: select phone color")
        if channel == self.okButton and self.selected:
            self.state = 5
            self.selected = False
        elif channel == 2:
            self.phone.color = PhoneColor.RED
            self.selected = True
        elif channel == 3:
            self.phone.color = PhoneColor.GREEN
            self.selected = True
        elif channel == 4:
            self.phone.color = PhoneColor.BLUE
            self.selected = True

    def resetPhone(self):
        self.state = 0
