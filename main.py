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
    monitor_1 = QtWidgets.QDesktopWidget().screenGeometry(0)
    monitor_2 = QtWidgets.QDesktopWidget().screenGeometry(1)
    MainWindow_1.move(monitor_1.left(), monitor_1.top())
    MainWindow_2.move(monitor_2.left(), monitor_2.top())
    ui_1.setupUi(MainWindow_1)
    ui_2.setupUi(MainWindow_2)
    MainWindow_1.showFullScreen()
    MainWindow_2.showFullScreen()
    sys.exit(app.exec_())
