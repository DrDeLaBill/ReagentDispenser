import threading
import time

import constants
from AdminWindow import AdminWindow
from BaseUserWindow import Ui_MainWindow


class UserWindow(Ui_MainWindow):
    def setupUi(self, MainWindow):
        # Main
        self.isGPIO = False
        self.isWarningTemp = False
        self.waitForSecondHand = False
        self.delayTime = time.time()

        Ui_MainWindow.setupUi(self, MainWindow)

        self.loop = threading.Thread(target=self.loopUi, args=())
        self.loop.start()
        self.showMainScreen()

    def loopUi(self):
        while True:
            if self.isGPIO:
                self.checkUserTemperature()
            else:
                self.checkGPIOStatus()

    def checkGPIOStatus(self):
        self.isGPIO = AdminWindow.getWorkStatus()

    def checkUserTemperature(self):
        if self.isWaitForSecondHand():
            self.waitForSecondHand = True
        elif self.isAlertTemperature():
            self.delayTime = time.time()
            self.waitForSecondHand = False
            self.isWarningTemp = False
            self.showAlertScreen()
        elif self.isWarningTemperature():
            self.delayTime = time.time()
            self.isWarningTemp = True
            self.waitForSecondHand = False
            self.showWarningScreen()
        elif self.isNormalTemperature():
            self.delayTime = time.time()
            self.isWarningTemp = False
            self.waitForSecondHand = False
            self.showSuccesScreen()
        elif not self.isDelayTime():
            self.waitForSecondHand = False
            self.isWarningTemp = False
            self.showMainScreen()

    def isWaitForSecondHand(self):
        if self.isWarningTemp and AdminWindow.getDistance() > constants.DISTANCE_MAX_VALUE and self.isDelayTime():
            return True
        return False

    def isAlertTemperature(self):
        temperature = AdminWindow.getTemperature()
        if not temperature:
            return False
        elif self.isWarningTemp and self.waitForSecondHand and AdminWindow.getDistance() < constants.DISTANCE_MAX_VALUE and temperature > constants.TEMPERATURE_MAX_VALUE:
            return True
        return False

    def isWarningTemperature(self):
        if AdminWindow.getDistance() < constants.DISTANCE_MAX_VALUE and AdminWindow.getTemperature() > constants.TEMPERATURE_MAX_VALUE and not self.isDelayTime():
            return True
        return False

    def isNormalTemperature(self):
        if AdminWindow.getDistance() < constants.DISTANCE_MAX_VALUE and AdminWindow.getTemperature() < constants.TEMPERATURE_MAX_VALUE:
            return True
        return False

    def isDelayTime(self):
        if time.time() - self.delayTime < constants.TEMPERATURE_DELAY:
            return True
        return False

    def showMainScreen(self):
        self.warningBox.hide()
        self.alertBox.hide()
        self.successBox.hide()
        self.mainBox.show()

    def showWarningScreen(self):
        self.mainBox.hide()
        self.alertBox.hide()
        self.successBox.hide()
        self.warningBox.show()

    def showAlertScreen(self):
        self.mainBox.hide()
        self.warningBox.hide()
        self.successBox.hide()
        self.alertBox.show()

    def showSuccesScreen(self):
        self.mainBox.hide()
        self.warningBox.hide()
        self.alertBox.hide()
        self.successBox.show()

    def hideAll(self):
        self.mainBox.hide()
        self.warningBox.hide()
        self.alertBox.hide()
        self.successBox.hide()
