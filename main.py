import sys

from PyQt5 import QtWidgets

from AdminWindow import AdminWindow
from UserWindow import UserWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow_1 = QtWidgets.QMainWindow()
    MainWindow_2 = QtWidgets.QMainWindow()
    ui_1 = AdminWindow()
    ui_2 = UserWindow()
    ui_1.setupUi(MainWindow_1)
    ui_2.setupUi(MainWindow_2)
    MainWindow_1.show()
    MainWindow_2.show()
    sys.exit(app.exec_())
