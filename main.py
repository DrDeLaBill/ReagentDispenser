import sys
import threading
import time

import RPi.GPIO as GPIO
from PyQt5 import QtCore, QtWidgets
from smbus2 import SMBus
from mlx90614 import MLX90614

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
        self.dispenserEnable = False
        self.dispenserCycleTime = time.time()
        self.dispenserDelayTime = 0
        # Main
        self.workTime = time.time()

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
        # Distance
        GPIO.setup(constants.DISTANCE_GPIO_TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(constants.DISTANCE_GPIO_ECHO_PIN, GPIO.IN)
        # Pump
        GPIO.setup(constants.LIQUID_FULL_PIN, GPIO.OUT)
        GPIO.setup(constants.LIQUID_EMPTY_PIN, GPIO.OUT)
        GPIO.setup(constants.LIQUID_MAIN_TANK_PIN, GPIO.OUT)
        GPIO.setup(constants.LIQUID_PUMP_PIN, GPIO.IN)

    def loopUi(self):
        # GPIO actions
        while True:
            self.workTime = time.time()
            self.checkTemperature()
            self.checkLiquidLevel()
            self.checkDistanceSensor()

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
        if self.switchReagent.dPtr.position:
            self.dispenserEnable = False
        else:
            self.dispenserEnable = True

    def dispenserTurnOn(self):
        if self.coolerSlider.value() > 0 and self.dispenserEnable:
            if self.workTime - self.dispenserCycleTime >= constants.DISPENSER_MAX_DELAY_TIME:
                print("Dispenser off")
                self.dispenserOff()
            elif not self.dispenserInWork:
                self.dispenserCheckDelay()
        else:
            self.dispenserOff()

    def dispenserCheckDelay(self):
        delayTime = self.coolerSlider.value() * constants.DISPENSER_MAX_DELAY_TIME / 100
        if self.workTime >= delayTime + self.dispenserCycleTime:
            print("Dispenser on")
            self.dispenserOn()

    def dispenserOn(self):
        self.dispenserInWork = True
        GPIO.output(constants.DISPENSER_GPIO_PIN, GPIO.HIGH)

    def dispenserOff(self):
        self.dispenserCycleTime = time.time()
        self.dispenserInWork = False
        GPIO.output(constants.DISPENSER_GPIO_PIN, GPIO.LOW)

    def getDistance(self):
        # set Trigger to HIGH
        GPIO.output(constants.DISTANCE_GPIO_TRIGGER_PIN, GPIO.HIGH)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(constants.DISTANCE_GPIO_TRIGGER_PIN, GPIO.LOW)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(constants.DISTANCE_GPIO_ECHO_PIN) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(constants.DISTANCE_GPIO_ECHO_PIN) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance

    def checkDistanceSensor(self):
        if self.isSmallDistance():
            print("Small distance: " + str(self.getDistance()))
            self.dispenserTurnOn()

    def checkTemperature(self):
        if self.isSmallDistance():
            self.label_6.setText(f"{self.getTemperature()}°C")
        else:
            self.label_6.setText("--°C")

    def isSmallDistance(self):
        return self.getDistance() < constants.DISTANCE_MAX_VALUE

    def getTemperature(self):
        bus = SMBus(1)
        sensor = MLX90614(bus, address=constants.TEMPERATURE_SENSOR_CHANNEL)
        temperature = sensor.get_object_1()
        bus.close()
        return temperature

    def checkLiquidLevel(self):
        mainTankState = GPIO.input(constants.LIQUID_MAIN_TANK_PIN) == 1
        if GPIO.input(constants.LIQUID_FULL_PIN) == 1:
            GPIO.output(constants.LIQUID_PUMP_PIN, GPIO.LOW)
        elif GPIO.input(constants.LIQUID_EMPTY_PIN) == 1 and mainTankState:
            GPIO.output(constants.LIQUID_PUMP_PIN, GPIO.HIGH)
        elif not mainTankState:
            self.label_7.show()
        else:
            self.label_7.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
