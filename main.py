import sys

from PyQt5 import  QtCore, QtGui, QtWidgets

from switch import Switch
from window import Ui_MainWindow


class Window(Ui_MainWindow):
    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)
        self.switchReagent = Switch(MainWindow)
        self.switchTemperature = Switch(MainWindow)
        self.switchReagent.setGeometry(QtCore.QRect(360, 150, 75, 31))
        self.switchTemperature.setGeometry(QtCore.QRect(360, 210, 75, 31))
        self.label_7.hide()
        self.horizontalSlider.valueChanged.connect(self.horizontalSliderAction)
        self.switchTemperature.clicked.connect(self.switchTemperatureAction)
        self.switchReagent.clicked.connect(self.switchReagentAction)

        self.initButtonActions()
        self.loopUi()

    def initButtonActions(self):
        pass

    def loopUi(self):
        # GPIO actions
        pass

    def horizontalSliderAction(self):
        print("Slider: " + str(self.horizontalSlider.value()))

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
