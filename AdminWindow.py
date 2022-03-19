import threading
import time

import RPi.GPIO as GPIO
from smbus2 import SMBus
from mlx90614 import MLX90614

import constants
from BaseAdminWindow import Ui_MainWindow


class AdminWindow(Ui_MainWindow):
    temperature = 0.0
    distance = 0.0
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
        # Main
        self.workTime = time.time()
        self.isAuth = False

        Ui_MainWindow.setupUi(self, MainWindow)

        self.setupGPIO()
        self.initButtonActions()
        print('init loop')
        self.loop = threading.Thread(target=self.loopUi, args=())
        self.loop.start()
        print('loop start')

        self.showPassword()

    def __del__(self):
        GPIO.cleanup()
        self.loop.terminate()

    def initButtonActions(self):
        self.coolerSlider.valueChanged.connect(self.coolerSliderAction)
        self.coolerSlider.setTickPosition(0)
        self.switchTemperature.clicked.connect(self.switchTemperatureAction)
        self.switchReagent.clicked.connect(self.switchReagentAction)
        self.pushButton.clicked.connect(self.auth)

    def setupGPIO(self):
        GPIO.setwarnings(False)
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
        AdminWindow.workStatus = True

    def loopUi(self):
        # GPIO actions
        while True:
            if self.isAuth:
                self.workTime = time.time()
                self.checkTemperature()
                self.checkLiquidLevel()
                self.checkDistanceSensor()

    def auth(self):
        if self.lineEdit.text() == constants.PASSWORD:
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

    def getSensorDistance(self):
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

        AdminWindow.distance = distance
        return distance

    def checkDistanceSensor(self):
        if self.isSmallDistance():
            self.dispenserTurnOn()

    def checkTemperature(self):
        if self.isSmallDistance():
            self.label_6.setText(f"{self.getSensorTemperature()}°C")
        else:
            self.label_6.setText("--°C")

    def isSmallDistance(self):
        return self.getDistance() < constants.DISTANCE_MAX_VALUE

    def getSensorTemperature(self):
        bus = SMBus(1)
        sensor = MLX90614(bus, address=constants.TEMPERATURE_SENSOR_CHANNEL)
        try:
            temperature = sensor.get_object_1()
            bus.close()
            AdminWindow.temperature = temperature
            return temperature
        except Exception:
            return "ERR"

    def checkLiquidLevel(self):
        mainTankState = GPIO.input(constants.LIQUID_MAIN_TANK_PIN) == 1
        if GPIO.input(constants.LIQUID_FULL_PIN) == 1:
            GPIO.output(constants.LIQUID_PUMP_PIN, GPIO.LOW)
        elif GPIO.input(constants.LIQUID_EMPTY_PIN) == 1 and mainTankState:
            GPIO.output(constants.LIQUID_PUMP_PIN, GPIO.HIGH)
        elif mainTankState:
            self.label_7.show()
        else:
            self.label_7.hide()

    @staticmethod
    def getDistance():
        return AdminWindow.distance

    @staticmethod
    def getTemperature():
        if AdminWindow.temperature < constants.TEMPERATURE_MIN_VALUE:
            return False
        return AdminWindow.temperature

    @staticmethod
    def getWorkStatus():
        return AdminWindow.workStatus
