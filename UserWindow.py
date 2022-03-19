import threading
import time

import constants
from AdminWindow import AdminWindow
from BaseUserWindow import Ui_MainWindow


class UserWindow(Ui_MainWindow):
    def setupUi(self, MainWindow):
        # Main
        self.isGPIO = False
        self.firstHand = False
        self.waitForSecondHand = False
        self.delayTime = time.time()

        Ui_MainWindow.setupUi(self, MainWindow)

        self.loop = threading.Thread(target=self.loopUi, args=())
        self.loop.start()
        self.showMainScreen()

    def loopUi(self):
        while True:
            if self.isGPIO:
                self.checkVisitor()
            else:
                self.checkGPIOStatus()

    def checkGPIOStatus(self):
        self.isGPIO = AdminWindow.getWorkStatus()

    def checkVisitor(self):
        distance = AdminWindow.getDistance()
        if distance > constants.DISTANCE_MAX_VALUE and self.firstHand:
            self.waitForSecondHand = True
        if distance < constants.DISTANCE_MAX_VALUE:
            self.checkUserTemperature()
        elif not self.isDelayTime():
            self.showMainScreen()

    def checkUserTemperature(self):
        if self.isAlertTemperature() and not self.isDelayTime():
            self.showWarningScreen()
            self.firstHand = True
        elif self.isAlertTemperature() and self.isWaitForSecondHand():
            self.showAlertScreen()
            self.firstHand = False
            self.waitForSecondHand = False
        else:
            self.showSuccesScreen()

    def isDelayTime(self):
        return time.time() - self.delayTime < constants.TEMPERATURE_DELAY

    def isWaitForSecondHand(self):
        return self.firstHand and self.waitForSecondHand

    def isAlertTemperature(self):
        temperature = AdminWindow.getTemperature()
        if not temperature:
            return False
        return temperature > constants.TEMPERATURE_MAX_VALUE

    def showMainScreen(self):
        self.warningBox.hide()
        self.alertBox.hide()
        self.successBox.hide()
        self.mainBox.show()

    def showWarningScreen(self):
        self.mainBox.hide()
        self.alertBox.hide()
        self.successBox.hide()
        self.delayTime = time.time()
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
        self.delayTime = time.time()
        self.successBox.show()

    def hideAll(self):
        self.mainBox.hide()
        self.warningBox.hide()
        self.alertBox.hide()
        self.successBox.hide()
