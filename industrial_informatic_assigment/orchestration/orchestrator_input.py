import logging
import time

import explorerhat

from industrial_informatic_assigment.orchestration.orchestrator_rpi import Orchestrator
from industrial_informatic_assigment.workstation.phone import Phone
from industrial_informatic_assigment.enum.phone_color import PhoneColor
from industrial_informatic_assigment.enum.phone_shape import PhoneShape


class OrchestratorInput:

    def __init__(self, orchestrator: Orchestrator):
        self.phone = Phone(PhoneShape.FRAME_1, PhoneShape.KEYBOARD_1,
                           PhoneShape.SCREEN_1, PhoneColor.RED)
        self.state = 0
        self.selected = False
        self.orchestrator = orchestrator
        self.okButton = 3

    def startListening(self):
        explorerhat.touch.pressed(self.changeState)
        print("Waiting for button actions")
        #lights
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

    def changeState(self, button):
        print("Button pressed: " + str(button))
        if self.state == 0:
            if button == self.okButton:
                self.state = 1
        elif self.state == 1:
            self.state1(button)
        elif self.state == 2:
            self.state2(button)
        elif self.state == 3:
            self.state3(button)
        elif self.state == 4:
            self.state4(button)
        elif self.state == 5:
            if button == self.okButton:
                logging.debug("OrchestratorInput: Phone")
                self.phone.printPhone()
                self.orchestrator.addNewOrder(self.phone) #TODO
                self.state = 0

    def state1(self, button):
        print("Select frame shape")
        if button == self.okButton and self.selected:
            self.state = 2
            self.selected = False
        elif button == 0:
            print('FRAME_1 selected')
            self.phone.frameShape = PhoneShape.FRAME_1
            self.selected = True
        elif button == 1:
            print('FRAME_2 selected')
            self.phone.frameShape = PhoneShape.FRAME_2
            self.selected = True
        elif button == 2:
            print('FRAME_3 selected')
            self.phone.frameShape = PhoneShape.FRAME_3
            self.selected = True

    def state2(self, button):
        print("OSelect screen shape")
        if button == self.okButton and self.selected:
            self.state = 3
            self.selected = False
        elif button == 0:
            print('SCREEN_1 selected')
            self.phone.screenShape = PhoneShape.SCREEN_1
            self.selected = True
        elif button == 1:
            print('SCREEN_2 selected')
            self.phone.screenShape = PhoneShape.SCREEN_2
            self.selected = True
        elif button == 2:
            print('SCREEN_3 selected')
            self.phone.screenShape = PhoneShape.SCREEN_3
            self.selected = True

    def state3(self, button):
        print("Select keyboard shape")
        if button == self.okButton and self.selected:
            self.state = 4
            self.selected = False
        elif button == 0:
            print('KEYBOARD_1 selected')
            self.phone.keyboardShape = PhoneShape.KEYBOARD_1
            self.selected = True
        elif button == 1:
            print('KEYBOARD_2 selected')
            self.phone.keyboardShape = PhoneShape.KEYBOARD_2
            self.selected = True
        elif button == 2:
            print('KEYBOARD_3 selected')
            self.phone.keyboardShape = PhoneShape.KEYBOARD_3
            self.selected = True

    def state4(self, button):
        print("Select phone color")
        if button == self.okButton and self.selected:
            self.state = 5
            self.selected = False
        elif button == 0:
            print('PhoneColor.RED selected')
            self.phone.color = PhoneColor.RED
            self.selected = True
        elif button == 1:
            print('PhoneColor.GREEN selected')
            self.phone.color = PhoneColor.GREEN
            self.selected = True
        elif button == 2:
            print('PhoneColor.BLUE selected')
            self.phone.color = PhoneColor.BLUE
            self.selected = True

    def resetPhone(self):
        self.state = 0
