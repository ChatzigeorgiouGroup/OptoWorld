# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(540, 344)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_status_light = QtWidgets.QLabel(self.groupBox_2)
        self.label_status_light.setObjectName("label_status_light")
        self.horizontalLayout.addWidget(self.label_status_light)
        self.label_status_light_level = QtWidgets.QLabel(self.groupBox_2)
        self.label_status_light_level.setObjectName("label_status_light_level")
        self.horizontalLayout.addWidget(self.label_status_light_level)
        self.label_status_temperature = QtWidgets.QLabel(self.groupBox_2)
        self.label_status_temperature.setObjectName("label_status_temperature")
        self.horizontalLayout.addWidget(self.label_status_temperature)
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_lightswitch = QtWidgets.QPushButton(self.groupBox)
        self.button_lightswitch.setCheckable(False)
        self.button_lightswitch.setObjectName("button_lightswitch")
        self.horizontalLayout_2.addWidget(self.button_lightswitch)
        self.slider_light = QtWidgets.QSlider(self.groupBox)
        self.slider_light.setMaximum(100)
        self.slider_light.setOrientation(QtCore.Qt.Horizontal)
        self.slider_light.setObjectName("slider_light")
        self.horizontalLayout_2.addWidget(self.slider_light)
        self.label_light = QtWidgets.QLabel(self.groupBox)
        self.label_light.setObjectName("label_light")
        self.horizontalLayout_2.addWidget(self.label_light)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 540, 30))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_edit_light_profile = QtWidgets.QAction(MainWindow)
        self.action_edit_light_profile.setObjectName("action_edit_light_profile")
        self.menuOptions.addAction(self.action_edit_light_profile)
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        self.slider_light.valueChanged['int'].connect(self.label_light.setNum)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Status"))
        self.label_status_light.setText(_translate("MainWindow", "Light"))
        self.label_status_light_level.setText(_translate("MainWindow", "light_level"))
        self.label_status_temperature.setText(_translate("MainWindow", "Temperature"))
        self.groupBox.setTitle(_translate("MainWindow", "Controls"))
        self.button_lightswitch.setText(_translate("MainWindow", "Switch the Light"))
        self.label_light.setText(_translate("MainWindow", "0"))
        self.menuOptions.setTitle(_translate("MainWindow", "Optio&ns"))
        self.action_edit_light_profile.setText(_translate("MainWindow", "edit light profile"))
