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
        self.checkTempState = 0
        self.workStatus = False

        Ui_MainWindow.setupUi(self, MainWindow)

        self.loop = threading.Thread(target=self.loopUi, args=())
        self.loop.start()
        self.showSuccesScreen()

    def loopUi(self):
        while True:
            self.checkGPIOStatus()
            
            if self.isGPIO != self.workStatus:
                if self.isGPIO:
                    self.showMainScreen()
                    self.checkTempState = 0
                else:
                    self.label_success.setText("")
                    self.showSuccesScreen()
                self.workStatus = self.isGPIO

            elif self.isGPIO:
                self.checkUserTemperature()
            

    def checkGPIOStatus(self):
        self.isGPIO = AdminWindow.getWorkStatus()


    def checkUserTemperature(self):
        # 4 состояния? 
        # 1 - желтый экран, ждем пока сработает датчик
        #  датчик сработал, проверяем и показываем температуру. 
        # 2 - температура нормальная, зеленый экран
        # 3 - температура высокая, красный экран
        # 4 - ждем некоторое время и возвращаемся на начальный экран
        #


        if self.checkTempState == 0: 
            # начальный экран, проверяем расстояние
            dist = AdminWindow.getDistance()
            self.updateTemperature()

            if dist < constants.DISTANCE_MAX_VALUE and self.temperature > 0.0:

                if self.temperature < constants.TEMPERATURE_MAX_VALUE:
                    self.checkTempState = 1
                else:
                    self.checkTempState = 2
                self.delayTime = time.time()

        elif self.checkTempState == 1:
            # температура нормальная, включаем зеленый экран
            self.showSuccesScreen()
            self.checkTempState = 3

        elif self.checkTempState == 2:
            # температура высокая включаем красный экран
            self.showAlertScreen()
            self.checkTempState = 3

        elif self.checkTempState == 3:
                # сколько-то ждем
                if (time.time() - self.delayTime >= constants.TEMPERATURE_DELAY):
                    self.showMainScreen()
                    self.checkTempState = 0


    def updateTemperature(self):
        self.temperature = AdminWindow.getTemperature()
        self.label_alert.setText("{:.1f}°C".format(self.temperature))
        self.label_warning.setText("{:.1f}°C".format(self.temperature))
        self.label_success.setText("{:.1f}°C".format(self.temperature))
        

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