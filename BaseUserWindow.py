# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\BaseUserWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QApplication

import constants


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # Получить размер разрешения монитора
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry(1)
        # При отладке:
        # self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
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
        self.label_2.setGeometry(QtCore.QRect(0, 10, self.width, self.height-(constants.FONT_SIZE+50)))
        self.label_2.setWordWrap(True)
        self.label_2.setAlignment(Qt.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(constants.FONT_SIZE)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_success = QtWidgets.QLabel(self.successBox)
        self.label_success.setGeometry(QtCore.QRect(0, self.height-(constants.FONT_SIZE+50), self.width, constants.FONT_SIZE+50))
        self.label_success.setAlignment(Qt.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(constants.FONT_SIZE)
        self.label_success.setFont(font)
        self.label_success.setObjectName("label_success")
        
        self.mainBox = QtWidgets.QGroupBox(self.centralwidget)
        self.mainBox.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.mainBox.setStyleSheet(constants.USER_BACKGROUND_COLOR)
        self.mainBox.setTitle("")
        self.mainBox.setObjectName("mainBox")
        self.label_4 = QtWidgets.QLabel(self.mainBox)
        self.label_4.setGeometry(QtCore.QRect(0, 10, self.width, self.height-(constants.FONT_SIZE+50)))
        self.label_4.setWordWrap(True)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(constants.FONT_SIZE)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.alertBox = QtWidgets.QGroupBox(self.centralwidget)
        self.alertBox.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.alertBox.setStyleSheet("background-color: rgb(255, 72, 0);")
        self.alertBox.setTitle("")
        self.alertBox.setObjectName("alertBox")
        self.label_6 = QtWidgets.QLabel(self.alertBox)
        self.label_6.setGeometry(QtCore.QRect(0, 10, self.width, self.height-(constants.FONT_SIZE+50)))
        self.label_6.setWordWrap(True)
        self.label_6.setAlignment(Qt.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(constants.FONT_SIZE-30)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_alert = QtWidgets.QLabel(self.alertBox)
        self.label_alert.setGeometry(QtCore.QRect(0, self.height-(constants.FONT_SIZE+50), self.width, constants.FONT_SIZE+50))
        self.label_alert.setAlignment(Qt.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(constants.FONT_SIZE)
        self.label_alert.setFont(font)
        self.label_alert.setObjectName("label_alert")
        
        self.warningBox = QtWidgets.QGroupBox(self.centralwidget)
        self.warningBox.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.warningBox.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.warningBox.setTitle("")
        self.warningBox.setObjectName("warningBox")
        self.label_warning = QtWidgets.QLabel(self.warningBox)
        self.label_warning.setGeometry(QtCore.QRect(
            0,
            self.height // 2 - 160,
            self.width,
            100
        ))
        self.label_warning.setAlignment(Qt.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(constants.FONT_SIZE)
        self.label_warning.setFont(font)
        self.label_warning.setObjectName("label_warning")
        self.label_5 = QtWidgets.QLabel(self.warningBox)
        self.label_5.setGeometry(QtCore.QRect(
            0,
            self.height // 2 - 50,
            self.width,
            100
        ))
        self.label_5.setAlignment(Qt.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(constants.FONT_SIZE)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.showAlertScreen()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Проходите! Будьте здоровы!"))
        self.label_4.setText(_translate("MainWindow", "Поднесите руку к датчику"))
        self.label_6.setText(_translate("MainWindow", "Высокая температура! Обратитесь к врачу!"))
        self.label_5.setText(_translate("MainWindow", "Поднесите другую руку"))
        self.label_success.setText(_translate("MainWindow", ""))
        self.label_alert.setText(_translate("MainWindow", ""))
        self.label_warning.setText(_translate("MainWindow", ""))

    def showMainScreen(self):
        self.hideAll()
        self.mainBox.show()

    def showWarningScreen(self):
        self.hideAll()
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    sys.exit(app.exec_())
