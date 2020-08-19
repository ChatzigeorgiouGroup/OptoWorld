#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 14:23:46 2020

@author: daniel
"""



from mainwindow_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import paho.mqtt.client as client
import sys
import time

from Tools.Stim_tools.Stim_tools import Timer
from Tools.Stim_tools.Stim_tools import Stim_widget
from Tools.MQTT_tools import MQTT_Listener
from Tools.PlotWidget import PlotWidget

BROKER_IP = "192.168.1.9"

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.button_lightswitch.clicked.connect(self.button_clicked)
        
        self.mqtt_listener = MQTT_Listener(BROKER_IP, "listener")
        # self.mqtt_listener.signals.new_light_value.connect(self.update_value_label)
        # self.mqtt_listener.signals.new_temperature_value.connect(self.update_temperature_label)
        # self.mqtt_listener.signals.new_light_level_value.connect(self.update_light_level_label)
        self.mqtt_listener.signals.new_status.connect(self.update_status_labels)

        self.threadpool = QtCore.QThreadPool()
        self.threadpool.start(self.mqtt_listener)

        self.ui.action_edit_light_profile.triggered.connect(self.edit_light_profile)
        self.make_graphs()
        
    def edit_light_profile(self):
        if not hasattr(self, "stim_widget"):        
            self.stim_widget = Stim_widget(parent = self)
        self.dock = self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.stim_widget)
        # self.dock.setWidget(self.stim_widget)
        self.stim_widget.show()

    def button_clicked(self):
        self.send_light_value(self.ui.slider_light.value())
        
    def send_light_value(self, val):
        switch = client.Client("Yay")
        switch.connect(BROKER_IP, port = 1883)
        switch.publish("optoworld/switch", val)
        switch.disconnect()

    def update_status_labels(self, df):
        # temperature, light_value, light_intensity = new_val.split("_")
        self.ui.label_status_temperature.setText(f"Temperature: {df['temperature'].values[-1]} C")
        self.ui.label_status_light.setText(f"Light Value: {df['light_value'].values[-1]}")
        self.ui.label_status_light_level.setText(f"Light Level: {df['light_intensity'].values[-1]} lux")
        # print(f"Recieved from signals.new_status:\n\n {df}")

    def closeEvent(self, event):
        switch_off = QtWidgets.QMessageBox.question(self, "Switch Off?","Do you want to switch off the light on closing?", 
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if switch_off==QtWidgets.QMessageBox.Yes:
            self.send_light_value(0)
        else:
            pass
        
        sys.stdout.write("\n\n Closing... \n\n Killing mqtt-monitor thread.... \n")
        self.mqtt_listener.alive = False
        self.mqtt_listener.client.disconnect()
        try:
            self.stim_widget.timer.alive = False
            self.stim_widget.timer.client.disconnect()
            sys.stdout.write("\nCleaning up remaining timer-threads...")
        except:
            sys.stdout.write("\nNo remaining timer-threads found")
        

        sys.stdout.write("\n\nGood Bye")
        event.accept()

    def make_graphs(self):
        self.plot_temperature = PlotWidget()
        self.plot_light_level = PlotWidget()
        self.plot_light_value = PlotWidget()

        self.ui.framePlotWidget.setLayout(QtWidgets.QVBoxLayout())

        for widget in [self.plot_light_level, self.plot_light_value, self.plot_temperature]:
            self.ui.framePlotWidget.layout().addWidget(widget)

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtWidgets.QApplication.instance().exec_()