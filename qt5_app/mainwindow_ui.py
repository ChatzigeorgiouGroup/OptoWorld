# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(627, 497)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_mqtt_status = QtWidgets.QLabel(self.groupBox)
        self.label_mqtt_status.setObjectName("label_mqtt_status")
        self.verticalLayout.addWidget(self.label_mqtt_status)
        self.label_status_light_intensity = QtWidgets.QLabel(self.groupBox)
        self.label_status_light_intensity.setObjectName("label_status_light_intensity")
        self.verticalLayout.addWidget(self.label_status_light_intensity)
        self.label_status_light = QtWidgets.QLabel(self.groupBox)
        self.label_status_light.setObjectName("label_status_light")
        self.verticalLayout.addWidget(self.label_status_light)
        self.label_status_temperature = QtWidgets.QLabel(self.groupBox)
        self.label_status_temperature.setObjectName("label_status_temperature")
        self.verticalLayout.addWidget(self.label_status_temperature)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_light = QtWidgets.QLabel(self.groupBox)
        self.label_light.setAlignment(QtCore.Qt.AlignCenter)
        self.label_light.setObjectName("label_light")
        self.verticalLayout_2.addWidget(self.label_light)
        self.slider_light = QtWidgets.QSlider(self.groupBox)
        self.slider_light.setMaximum(255)
        self.slider_light.setOrientation(QtCore.Qt.Vertical)
        self.slider_light.setInvertedAppearance(False)
        self.slider_light.setInvertedControls(False)
        self.slider_light.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.slider_light.setTickInterval(10)
        self.slider_light.setObjectName("slider_light")
        self.verticalLayout_2.addWidget(self.slider_light)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 2, 1, 1)
        self.button_lightswitch = QtWidgets.QPushButton(self.groupBox)
        self.button_lightswitch.setCheckable(False)
        self.button_lightswitch.setObjectName("button_lightswitch")
        self.gridLayout.addWidget(self.button_lightswitch, 1, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.framePlotWidget = QtWidgets.QFrame(self.centralwidget)
        self.framePlotWidget.setMinimumSize(QtCore.QSize(600, 400))
        self.framePlotWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePlotWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framePlotWidget.setObjectName("framePlotWidget")
        self.gridLayout_2.addWidget(self.framePlotWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 627, 30))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionedit_light_profile = QtWidgets.QAction(MainWindow)
        self.actionedit_light_profile.setObjectName("actionedit_light_profile")
        self.actionshow_live_graphs = QtWidgets.QAction(MainWindow)
        self.actionshow_live_graphs.setObjectName("actionshow_live_graphs")
        self.menuOptions.addAction(self.actionedit_light_profile)
        self.menuOptions.addAction(self.actionshow_live_graphs)
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        self.slider_light.sliderMoved['int'].connect(self.label_light.setNum)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Controls"))
        self.label_mqtt_status.setText(_translate("MainWindow", "TextLabel"))
        self.label_status_light_intensity.setText(_translate("MainWindow", "light_level"))
        self.label_status_light.setText(_translate("MainWindow", "Light"))
        self.label_status_temperature.setText(_translate("MainWindow", "Temperature"))
        self.label_light.setText(_translate("MainWindow", "0"))
        self.button_lightswitch.setText(_translate("MainWindow", "Set Value"))
        self.menuOptions.setTitle(_translate("MainWindow", "Optio&ns"))
        self.actionedit_light_profile.setText(_translate("MainWindow", "&edit light profile"))
        self.actionshow_live_graphs.setText(_translate("MainWindow", "show live graphs"))


