# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import constants
from switch import Switch


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(constants.SCREEN_HIGH, constants.SCREEN_WIDTH)
        # Main window
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.coolerSlider = QtWidgets.QSlider(self.centralwidget)
        self.coolerSlider.setGeometry(QtCore.QRect(20, 70, 411, 22))
        self.coolerSlider.setOrientation(QtCore.Qt.Horizontal)
        self.coolerSlider.setObjectName("coolerSlider")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 411, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(410, 100, 47, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 150, 411, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 210, 411, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(720, 20, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 390, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 85, 0);")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(20, 280, 421, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(20, 330, 421, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(111, 111, 111);")
        self.label_9.setObjectName("label_9")
        self.switchReagent = Switch(MainWindow)
        self.switchTemperature = Switch(MainWindow)
        self.switchReagent.setGeometry(QtCore.QRect(360, 150, 75, 31))
        self.switchTemperature.setGeometry(QtCore.QRect(360, 210, 75, 31))
        self.label_7.hide()

        # Password window
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(
            (constants.SCREEN_WIDTH // 2) - 85,
            (constants.SCREEN_HIGH // 2) - 300,
            600,
            170
        ))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label")
        self.verticalLayout.addWidget(self.label_10)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Скорость вращения вентилятора"))
        self.label_2.setText(_translate("MainWindow", "min"))
        self.label_3.setText(_translate("MainWindow", "max"))
        self.label_4.setText(_translate("MainWindow", "Распылитель"))
        self.label_5.setText(_translate("MainWindow", "Измерение температуры"))
        self.label_6.setText(_translate("MainWindow", "--°C"))
        self.label_7.setText(_translate("MainWindow", "Низкий уровень жидкости"))
        self.label_8.setText(_translate("MainWindow", "Уровень жидкости"))
        self.label_9.setText(_translate("MainWindow", "23 мм"))
        self.label_10.setText(_translate("MainWindow", "Введите пароль"))
        self.pushButton.setText(_translate("MainWindow", "OK"))
    
    def showPassword(self):
        self.label.hide()
        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.coolerSlider.hide()
        self.switchTemperature.hide()
        self.switchReagent.hide()
        
        self.label_10.show()
        self.pushButton.show()
        self.lineEdit.show()

    def showMainWindow(self):
        self.label_10.hide()
        self.pushButton.hide()
        self.lineEdit.hide()

        self.label.show()
        self.label_2.show()
        self.label_3.show()
        self.label_4.show()
        self.label_5.show()
        self.label_6.show()
        self.label_7.hide()
        self.label_8.show()
        self.label_9.show()
        self.coolerSlider.show()
        self.switchTemperature.show()
        self.switchReagent.show()
