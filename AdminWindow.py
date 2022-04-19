import threading
import time

import subprocess
import os
import RPi.GPIO as GPIO
from smbus2 import SMBus
from mlx90614 import MLX90614

import constants
from BaseAdminWindow import Ui_MainWindow


class AdminWindow(Ui_MainWindow):
    temperature = 0.0
    distance = 999.9
    workStatus = False

    def setupUi(self, MainWindow):
        # Cooler
        self.coolerPWM = None
        self.coolerInWork = False
        # Dispenser
        self.dispenserInWork = False
        self.dispenserEnable = False
        self.dispenserCycleTime = time.time()
        self.dispenserDelayTime = 0
        # Temperature
        self.temperatureSensorInWork = False
        self.lastTempTime = 0
        # Main
        self.workTime = time.time()
        self.quitDelayTime = time.time()
        self.isAuth = False

        Ui_MainWindow.setupUi(self, MainWindow)

        self.setupGPIO()
        self.initButtonActions()
        self.loop = threading.Thread(target=self.loopUi, args=())
        self.loop.start()
        print('loop start')

        self.showPassword()

    def __del__(self):
        GPIO.cleanup()

    def initButtonActions(self):
        self.coolerSlider.valueChanged.connect(self.coolerSliderAction)
        self.coolerSlider.setTickPosition(0)
        self.switchTemperature.clicked.connect(self.switchTemperatureAction)
        self.switchReagent.clicked.connect(self.switchReagentAction)
        self.b0.clicked.connect(self.b0Action)
        self.b1.clicked.connect(self.b1Action)
        self.b2.clicked.connect(self.b2Action)
        self.b3.clicked.connect(self.b3Action)
        self.b4.clicked.connect(self.b4Action)
        self.b5.clicked.connect(self.b5Action)
        self.b6.clicked.connect(self.b6Action)
        self.b7.clicked.connect(self.b7Action)
        self.b8.clicked.connect(self.b8Action)
        self.b9.clicked.connect(self.b9Action)
        self.bDel.clicked.connect(self.bDelAction)
        self.bOK.clicked.connect(self.auth)
        self.bQuit.clicked.connect(self.quit)
        self.bOff.clicked.connect(self.showConfirmWindow)
        self.bConfirmOk.clicked.connect(self.shutdown)
        self.bCancel.clicked.connect(self.hideConfirmWindow)
        self.bSliderMinus.clicked.connect(self.sliderMinus)
        self.bSliderPlus.clicked.connect(self.sliderPlus)

    def setupGPIO(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # Cooler settings
        GPIO.setup(constants.COOLER_GPIO_PWM_PIN, GPIO.OUT, initial=GPIO.LOW)
        self.coolerPWM = GPIO.PWM(constants.COOLER_GPIO_PWM_PIN, constants.COOLER_PWM_FREQ)
        # Dispenser
        GPIO.setup(constants.DISPENSER_GPIO_PIN, GPIO.OUT, initial=GPIO.LOW)
        # Distance
        GPIO.setup(constants.DISTANCE_GPIO_TRIGGER_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(constants.DISTANCE_GPIO_ECHO_PIN, GPIO.IN)
        # Pump
        GPIO.setup(constants.LIQUID_FULL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(constants.LIQUID_EMPTY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(constants.LIQUID_MAIN_TANK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(constants.LIQUID_PUMP_PIN, GPIO.OUT, initial=GPIO.LOW)
        # AdminWindow.workStatus = True

    def loopUi(self):
        # GPIO actions
        while True:
            if self.isAuth:
                self.workTime = time.time()
                self.checkTemperature()
                self.checkLiquidLevel()
                self.checkQuitDelay()
            else:
                self.quitDelayTime = time.time()

    def auth(self):
        if self.lineEdit.text() == constants.PASSWORD:
            self.lineEdit.setText("")
            self.isAuth = True
            self.showMainWindow()

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
        if self.switchTemperature.dPtr.position:
            self.temperatureSensorInWork = False
            AdminWindow.workStatus = False
        else:
            self.temperatureSensorInWork = True
            AdminWindow.workStatus = True

    def switchReagentAction(self):
        if self.switchReagent.dPtr.position:
            self.dispenserEnable = False
            self.dispenserOff()
        else:
            self.dispenserEnable = True
            self.dispenserOn()


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

    def getSensorDistance(self):
        # set Trigger to HIGH
        GPIO.output(constants.DISTANCE_GPIO_TRIGGER_PIN, GPIO.HIGH)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(constants.DISTANCE_GPIO_TRIGGER_PIN, GPIO.LOW)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(constants.DISTANCE_GPIO_ECHO_PIN) == 0 and self.isNotTimeout():
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(constants.DISTANCE_GPIO_ECHO_PIN) == 1 and self.isNotTimeout():
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        AdminWindow.distance = distance
        return distance

    def isNotTimeout(self):
        return time.time() - self.workTime < 0.05

    def checkDistanceSensor(self):
        #if self.isSmallDistance():
        #    self.dispenserTurnOn()
        return

    def checkTemperature(self):
        if self.isSmallDistance() and self.temperatureSensorInWork:
            self.getSensorTemperature()
            if time.time() - self.lastTempTime >= constants.TEMPERATURE_DELAY:
                self.showTempTime = time.time()
                self.label_6.setText("{:.1f}°C".format(AdminWindow.temperature))
        else:
            AdminWindow.temperature = 0.0
            self.label_6.setText("--°C")

    def isSmallDistance(self):
        if self.getSensorDistance() < constants.DISTANCE_MAX_VALUE:
            return True
        return False

    def getSensorTemperature(self):
        bus = SMBus(1)
        sensor = MLX90614(bus, address=constants.TEMPERATURE_SENSOR_CHANNEL)
        try:
            summ = 0
            for i in range(20):
                summ += sensor.get_object_1()
                time.sleep(0.01)

            AdminWindow.temperature = summ / 20
            bus.close()
            return AdminWindow.temperature
        except Exception:
            return "ERR"

    def checkLiquidLevel(self):
        mainTankState = GPIO.input(constants.LIQUID_MAIN_TANK_PIN) == GPIO.HIGH
        if GPIO.input(constants.LIQUID_FULL_PIN) == GPIO.LOW:
            GPIO.output(constants.LIQUID_PUMP_PIN, GPIO.LOW)
        elif GPIO.input(constants.LIQUID_EMPTY_PIN) == GPIO.LOW and mainTankState:
            GPIO.output(constants.LIQUID_PUMP_PIN, GPIO.HIGH)
        elif mainTankState:
            self.label_7.show()
        else:
            self.label_7.hide()

    def checkQuitDelay(self):
        if self.quitDelayTime + constants.QUIT_DELAY < time.time():
            self.isAuth = False
            self.showPassword()

    @staticmethod
    def getDistance():
        return AdminWindow.distance

    @staticmethod
    def getTemperature():
        return AdminWindow.temperature

    @staticmethod
    def getWorkStatus():
        return AdminWindow.workStatus

    def quit(self):
        self.showPassword()

    def shutdown(self):
        print('shutdown')
        os.system('sudo shutdown -h now')

    def b0Action(self):
        self.appendSignInLine('0')

    def b1Action(self):
        self.appendSignInLine('1')

    def b2Action(self):
        self.appendSignInLine('2')

    def b3Action(self):
        self.appendSignInLine('3')

    def b4Action(self):
        self.appendSignInLine('4')

    def b5Action(self):
        self.appendSignInLine('5')

    def b6Action(self):
        self.appendSignInLine('6')

    def b7Action(self):
        self.appendSignInLine('7')

    def b8Action(self):
        self.appendSignInLine('8')

    def b9Action(self):
        self.appendSignInLine('9')

    def appendSignInLine(self, sign):
        self.lineEdit.setText(str(self.lineEdit.text() + sign))

    def bDelAction(self):
        self.lineEdit.setText(self.lineEdit.text()[:-1])

    def sliderMinus(self):
        sliderValue = self.coolerSlider.value() - 10
        if sliderValue < 0:
            sliderValue = 0
        self.coolerSlider.setValue(sliderValue)
        self.coolerSliderAction()

    def sliderPlus(self):
        sliderValue = self.coolerSlider.value() + 10
        if sliderValue > 100:
            sliderValue = 100
        self.coolerSlider.setValue(sliderValue)
        self.coolerSliderAction()
