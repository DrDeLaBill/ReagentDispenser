import sys

import RPi.GPIO as GPIO
from PyQt5 import QtCore, QtWidgets

from constants import COOLER_GPIO_PWM_PIN, COOLER_PWM_FREQ
from switch import Switch
from window import Ui_MainWindow


class Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        self.coolerPWM = None
        self.coolerInWork = False

        Ui_MainWindow.setupUi(self, MainWindow)
        self.switchReagent = Switch(MainWindow)
        self.switchTemperature = Switch(MainWindow)
        self.switchReagent.setGeometry(QtCore.QRect(360, 150, 75, 31))
        self.switchTemperature.setGeometry(QtCore.QRect(360, 210, 75, 31))
        self.label_7.hide()
        self.coolerSlider.valueChanged.connect(self.coolerSliderAction)
        self.coolerSlider.value(0)
        self.switchTemperature.clicked.connect(self.switchTemperatureAction)
        self.switchReagent.clicked.connect(self.switchReagentAction)

        self.initButtonActions()
        self.loopUi()
        self.setupGPIO()

    def initButtonActions(self):
        pass

    def setupGPIO(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        # Cooler settings
        GPIO.setup(COOLER_GPIO_PWM_PIN, GPIO.OUT)
        self.coolerPWM = GPIO.PWM(COOLER_GPIO_PWM_PIN, COOLER_PWM_FREQ)

    def loopUi(self):
        # GPIO actions
        pass

    def coolerSliderAction(self):
        print("Slider: " + str(self.coolerSlider.value()))
        if self.coolerSlider.value() == 0:
            self.coolerPWM.stop()
            self.coolerInWork = False
        elif not self.coolerInWork:
            self.coolerPWM.start(self.coolerSlider.value())
            self.coolerInWork = True
        else:
            self.coolerPWM.ChangeDutyCicle(self.coolerSlider.value())

    def switchTemperatureAction(self):
        print("switchTemperature: " + str(self.switchTemperature.dPtr.position))

    def switchReagentAction(self):
        print("switchReagent: " + str(self.switchReagent.dPtr.position))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
