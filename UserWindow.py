import threading
import time

import constants
from AdminWindow import AdminWindow
from BaseUserWindow import Ui_MainWindow


class UserWindow(Ui_MainWindow):
    def setupUi(self, MainWindow):
        # Main
        self.isGPIO = False
        self.delayTime = time.time()

        Ui_MainWindow.setupUi(self, MainWindow)

        self.loop = threading.Thread(target=self.loopUi, args=())
        self.loop.start()
        self.showMainScreen()

    def __del__(self):
        self.loop.terminate()

    def loopUi(self):
        while True:
            if self.isGPIO:
                self.checkVisitor()
            else:
                self.checkGPIOStatus()

    def checkGPIOStatus(self):
        self.isGPIO = AdminWindow.workStatus

    def checkVisitor(self):
        if AdminWindow.distance < constants.DISTANCE_MAX_VALUE:
            self.checkUserTemperature()
        elif not self.isSecondMesurement():
            self.showMainScreen()

    def checkUserTemperature(self):
        if self.isAlertTemperature() and not self.isSecondMesurement():
            self.showWarningScreen()
        elif self.isAlertTemperature():
            self.showAlertScreen()
        else:
            self.showSuccesScreen()

    def isSecondMesurement(self):
        return time.time() - self.delayTime < constants.TEMPERATURE_DELAY

    def isAlertTemperature(self):
        return AdminWindow.temperature > constants.TEMPERATURE_MAX_VALUE

    def showMainScreen(self):
        self.hideAll()
        self.mainBox.show()

    def showWarningScreen(self):
        self.hideAll()
        self.delayTime = time.time()
        self.warningBox.show()

    def showAlertScreen(self):
        self.hideAll()
        self.alertBox.show()

    def showSuccesScreen(self):
        self.hideAll()
        self.successBox.show()

    def hideAll(self):
        self.mainBox.hide()
        self.warningBox.hide()
        self.alertBox.hide()
        self.successBox.hide()
