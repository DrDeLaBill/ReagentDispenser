import sys

from PyQt5 import QtWidgets

from AdminWindow import Window

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui_1 = Window()
    ui_1.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
