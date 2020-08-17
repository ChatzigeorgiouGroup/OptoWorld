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
        DockWidget.resize(400, 300)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox_on_duration = QtWidgets.QSpinBox(self.dockWidgetContents)
        self.spinBox_on_duration.setMaximum(999999999)
        self.spinBox_on_duration.setObjectName("spinBox_on_duration")
        self.horizontalLayout.addWidget(self.spinBox_on_duration)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBox_off_duration = QtWidgets.QSpinBox(self.dockWidgetContents)
        self.spinBox_off_duration.setMaximum(999999999)
        self.spinBox_off_duration.setObjectName("spinBox_off_duration")
        self.horizontalLayout_2.addWidget(self.spinBox_off_duration)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
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
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(self.dockWidgetContents)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 1, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "Doc&kWidget"))
        self.label_3.setText(_translate("DockWidget", "Intensity (0-255)"))
        self.label.setText(_translate("DockWidget", "On_duration (s)"))
        self.label_2.setText(_translate("DockWidget", "Off_duration (s)"))
        self.label_4.setText(_translate("DockWidget", "Repeats"))
        self.button_add_stim.setText(_translate("DockWidget", "Add stim to profile"))
