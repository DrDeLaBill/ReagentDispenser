import threading
import time

from PyQt5 import QtWidgets

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
        self.temperature = 0

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

    def updateTemperature(self):
        self.temperature = AdminWindow.getTemperature()
        self.label_alert.setText(str(self.temperature) + '°C')
        self.label_warning.setText(str(self.temperature) + '°C')
        self.label_success.setText(str(self.temperature) + '°C')
        self.label_main.setText(str(self.temperature) + '°C')

    def isWaitForSecondHand(self) -> bool:
        return self.isWarningTemp and not self.waitForSecondHand and AdminWindow.getDistance() > constants.DISTANCE_MAX_VALUE and self.isDelayTime()

    def isAlertTemperature(self) -> bool:
        return self.isWarningTemp and self.waitForSecondHand and AdminWindow.getDistance() < constants.DISTANCE_MAX_VALUE and AdminWindow.getTemperature() > constants.TEMPERATURE_MAX_VALUE

    def isWarningTemperature(self) -> bool:
        return AdminWindow.getDistance() < constants.DISTANCE_MAX_VALUE and AdminWindow.getTemperature() > constants.TEMPERATURE_MAX_VALUE and not self.isDelayTime()

    def isNormalTemperature(self) -> bool:
        return AdminWindow.getDistance() < constants.DISTANCE_MAX_VALUE and AdminWindow.getTemperature() < constants.TEMPERATURE_MAX_VALUE

    def isDelayTime(self) -> bool:
        return (time.time() - self.delayTime) < constants.TEMPERATURE_DELAY


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    sys.exit(app.exec_())