import sys

from PyQt5 import QtWidgets

# from AdminWindow import AdminWindow
from UserWindow import UserWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui_1 = UserWindow()
    ui_1.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
