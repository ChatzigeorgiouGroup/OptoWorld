# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dockwidget.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(758, 643)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.spinBox_intensity = QtWidgets.QSpinBox(self.dockWidgetContents)
        self.spinBox_intensity.setMaximum(255)
        self.spinBox_intensity.setObjectName("spinBox_intensity")
        self.horizontalLayout_3.addWidget(self.spinBox_intensity)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.frame = QtWidgets.QFrame(self.dockWidgetContents)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinBox_on_hour = QtWidgets.QSpinBox(self.frame)
        self.spinBox_on_hour.setObjectName("spinBox_on_hour")
        self.horizontalLayout.addWidget(self.spinBox_on_hour)
        self.spinBox_on_minute = QtWidgets.QSpinBox(self.frame)
        self.spinBox_on_minute.setObjectName("spinBox_on_minute")
        self.horizontalLayout.addWidget(self.spinBox_on_minute)
        self.spinBox_on_second = QtWidgets.QSpinBox(self.frame)
        self.spinBox_on_second.setObjectName("spinBox_on_second")
        self.horizontalLayout.addWidget(self.spinBox_on_second)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.dockWidgetContents)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.spinBox_off_hour = QtWidgets.QSpinBox(self.frame_2)
        self.spinBox_off_hour.setObjectName("spinBox_off_hour")
        self.horizontalLayout_2.addWidget(self.spinBox_off_hour)
        self.spinBox_off_minute = QtWidgets.QSpinBox(self.frame_2)
        self.spinBox_off_minute.setObjectName("spinBox_off_minute")
        self.horizontalLayout_2.addWidget(self.spinBox_off_minute)
        self.spinBox_off_second = QtWidgets.QSpinBox(self.frame_2)
        self.spinBox_off_second.setObjectName("spinBox_off_second")
        self.horizontalLayout_2.addWidget(self.spinBox_off_second)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.spinBox_repeats = QtWidgets.QSpinBox(self.dockWidgetContents)
        self.spinBox_repeats.setObjectName("spinBox_repeats")
        self.horizontalLayout_4.addWidget(self.spinBox_repeats)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.button_add_stim = QtWidgets.QPushButton(self.dockWidgetContents)
        self.button_add_stim.setObjectName("button_add_stim")
        self.verticalLayout.addWidget(self.button_add_stim)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView = QtWidgets.QTableView(self.groupBox)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.button_save_profile = QtWidgets.QPushButton(self.groupBox)
        self.button_save_profile.setObjectName("button_save_profile")
        self.horizontalLayout_5.addWidget(self.button_save_profile)
        self.button_load_profile = QtWidgets.QPushButton(self.groupBox)
        self.button_load_profile.setObjectName("button_load_profile")
        self.horizontalLayout_5.addWidget(self.button_load_profile)
        self.button_run = QtWidgets.QPushButton(self.groupBox)
        self.button_run.setObjectName("button_run")
        self.horizontalLayout_5.addWidget(self.button_run)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.gridLayout_3.addWidget(self.groupBox, 0, 1, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "Doc&kWidget"))
        self.label_3.setText(_translate("DockWidget", "Intensity (0-255)"))
        self.label.setText(_translate("DockWidget", "On Duration (H:M:s)"))
        self.label_2.setText(_translate("DockWidget", "Off Duration (H:M:s)"))
        self.label_4.setText(_translate("DockWidget", "Repeats"))
        self.button_add_stim.setText(_translate("DockWidget", "Add stim to profile"))
        self.groupBox.setTitle(_translate("DockWidget", "Profile"))
        self.button_save_profile.setText(_translate("DockWidget", "Save Profile"))
        self.button_load_profile.setText(_translate("DockWidget", "Load Profile"))
        self.button_run.setText(_translate("DockWidget", "Run Profile"))
