import sys
import threading
from time import time

import RPi.GPIO as GPIO
from PyQt5 import QtCore, QtWidgets

import constants
from switch import Switch
from window import Ui_MainWindow


class Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        # Cooler
        self.coolerPWM = None
        self.coolerInWork = False
        # Dispenser
        self.dispenserInWork = False
        self.dispenserCycleTime = time()
        self.dispenserDelayTime = 0
        # Main
        self.workTime = time()

        Ui_MainWindow.setupUi(self, MainWindow)
        self.switchReagent = Switch(MainWindow)
        self.switchTemperature = Switch(MainWindow)
        self.switchReagent.setGeometry(QtCore.QRect(360, 150, 75, 31))
        self.switchTemperature.setGeometry(QtCore.QRect(360, 210, 75, 31))
        self.label_7.hide()

        self.setupGPIO()
        self.initButtonActions()
        print('init loop')
        self.loop = threading.Thread(target=self.loopUi, args=())
        self.loop.start()
        print('loop start')

    def initButtonActions(self):
        self.coolerSlider.valueChanged.connect(self.coolerSliderAction)
        self.coolerSlider.setTickPosition(0)
        self.switchTemperature.clicked.connect(self.switchTemperatureAction)
        self.switchReagent.clicked.connect(self.switchReagentAction)

    def setupGPIO(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        # Cooler settings
        GPIO.setup(constants.COOLER_GPIO_PWM_PIN, GPIO.OUT)
        self.coolerPWM = GPIO.PWM(constants.COOLER_GPIO_PWM_PIN, constants.COOLER_PWM_FREQ)
        # Dispenser
        GPIO.setup(constants.DISPENSER_GPIO_PIN, GPIO.OUT)

    def loopUi(self):
        # GPIO actions
        while True:
            self.checkDispenserWorkTime()
            self.workTime = time()

    def coolerSliderAction(self):
        print("Slider: " + str(self.coolerSlider.value()))
        if self.coolerSlider.value() == 0:
            print("Cooler stop")
            self.coolerPWM.stop()
            self.coolerInWork = False
        elif not self.coolerInWork:
            print("Cooler start")
            self.coolerPWM.start(self.coolerSlider.value())
            self.coolerInWork = True
        else:
            print("Cooler change")
            self.coolerPWM.ChangeDutyCycle(self.coolerSlider.value())

    def switchTemperatureAction(self):
        print("switchTemperature: " + str(self.switchTemperature.dPtr.position))

    def switchReagentAction(self):
        print("switchReagent: " + str(self.switchReagent.dPtr.position))

    def checkDispenserWorkTime(self):
        controlValue = self.coolerSlider.value()
        delayTime = controlValue * constants.DISPENSER_MAX_DELAY_TIME / 100
        if controlValue > 0:
            if self.workTime - self.dispenserCycleTime >= constants.DISPENSER_MAX_DELAY_TIME:
                print("Dispenser off")
                self.dispenserOff()
            elif not self.dispenserInWork:
                self.dispenserCheckDelay(delayTime)
        else:
            self.dispenserOff()

    def dispenserCheckDelay(self, delayTime):
        print("Check delay")
        if self.workTime >= delayTime + self.dispenserCycleTime:
            print("Dispenser on")
            self.dispenserOn()

    def dispenserOn(self):
        self.dispenserInWork = True

    def dispenserOff(self):
        self.dispenserCycleTime = time()
        self.dispenserInWork = False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
