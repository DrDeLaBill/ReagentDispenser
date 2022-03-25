# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\BaseUserWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

import constants


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # Получить размер разрешения монитора
        self.desktop = QtWidgets.QDesktopWidget().screenGeometry(1)
        self.height = self.desktop.height()
        self.width = self.desktop.width()
        MainWindow.resize(self.height, self.width)
        # Main window
        MainWindow.setEnabled(True)
        MainWindow.resize(self.width, self.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.successBox = QtWidgets.QGroupBox(self.centralwidget)
        self.successBox.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.successBox.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.successBox.setTitle("")
        self.successBox.setObjectName("successBox")
        self.label_2 = QtWidgets.QLabel(self.successBox)
        self.label_2.setGeometry(QtCore.QRect(
            self.width // 2 - 120,
            self.height // 2 - 25,
            250,
            50
        ))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.successBox)
        self.label_3.setGeometry(QtCore.QRect(
            self.width // 2 - 180,
            self.height // 2 + 35,
            350,
            50
        ))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.mainBox = QtWidgets.QGroupBox(self.centralwidget)
        self.mainBox.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.mainBox.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.mainBox.setTitle("")
        self.mainBox.setObjectName("mainBox")
        self.label_4 = QtWidgets.QLabel(self.mainBox)
        self.label_4.setGeometry(QtCore.QRect(
            self.width // 2 - 220,
            self.height // 2 - 25,
            420,
            50
        ))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.alertBox = QtWidgets.QGroupBox(self.centralwidget)
        self.alertBox.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.alertBox.setStyleSheet("background-color: rgb(255, 72, 0);")
        self.alertBox.setTitle("")
        self.alertBox.setObjectName("alertBox")
        self.label_6 = QtWidgets.QLabel(self.alertBox)
        self.label_6.setGeometry(QtCore.QRect(
            self.width // 2 - 180,
            self.height // 2 - 25,
            370,
            50
        ))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.alertBox)
        self.label_7.setGeometry(QtCore.QRect(
            self.width // 2 - 170,
            self.height // 2 + 35,
            350,
            50
        ))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.warningBox = QtWidgets.QGroupBox(self.centralwidget)
        self.warningBox.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.warningBox.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.warningBox.setTitle("")
        self.warningBox.setObjectName("warningBox")
        self.label_5 = QtWidgets.QLabel(self.warningBox)
        self.label_5.setGeometry(QtCore.QRect(
            self.width // 2 - 190,
            self.height // 2 - 25,
            400,
            50
        ))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Проходите!"))
        self.label_3.setText(_translate("MainWindow", " Будьте здоровы!"))
        self.label_4.setText(_translate("MainWindow", "Поднесите руку к датчику"))
        self.label_6.setText(_translate("MainWindow", "Высокая температура!"))
        self.label_7.setText(_translate("MainWindow", "Обратитесь к врачу!"))
        self.label_5.setText(_translate("MainWindow", "Поднесите другую руку"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
