
from industrial_informatic_assigment.enum.enum_variables import PhoneShape, PhoneColor


class Phone:
    def __init__(self, frameShape: PhoneShape, keyboardShape: PhoneShape, screenShape: PhoneShape, color: PhoneColor):
        self.frameShape = frameShape
        self.keyboardShape = keyboardShape
        self.screenShape = screenShape
        self.color = color

    def printPhoneInfo(self):
        print("PHONE -  Frame: " + str(self.frameShape.value) + " Keyboard: " + str(self.keyboardShape.value) + " Screen: " + str(self.screenShape.value) + " Color:" + str(self.color.name))
