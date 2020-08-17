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


             
        
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.button_lightswitch.clicked.connect(self.button_clicked)
        
        self.mqtt_listener = MQTT_Listener("192.168.1.9", "listener")
        self.threadpool = QtCore.QThreadPool()
        self.threadpool.start(self.mqtt_listener)
        self.mqtt_listener.signals.new_light_value.connect(self.update_value_label)
        self.mqtt_listener.signals.new_temperature_value.connect(self.update_temperature_label)
        self.mqtt_listener.signals.new_light_level_value.connect(self.update_light_level_label)
        
        self.ui.action_edit_light_profile.triggered.connect(self.edit_light_profile)
        
    def edit_light_profile(self):
        if not hasattr(self, "stim_widget"):        
            self.stim_widget = Stim_widget(parent = self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.stim_widget)
        self.stim_widget.show()
        
    def button_clicked(self):
        self.send_light_value(self.ui.slider_light.value())
        
    def send_light_value(self, val):
        switch = client.Client("Yay")
        switch.connect("192.168.1.9", port = 1883)
        switch.publish("optoworld/switch", val)
        switch.disconnect()

    def update_value_label(self, new_val):
        self.ui.label_status_light.setText(f"Light Value: {new_val}")
        
    def update_temperature_label(self, new_val):
        self.ui.label_status_temperature.setText(f"Temperature: {new_val} C")
        
    def update_light_level_label(self, new_val):
        self.ui.label_status_light_level.setText(f"Light Level: {new_val} lux")
        
    def closeEvent(self, event):
        switch_off = QtWidgets.QMessageBox.question(self, "Switch Off?","Do you want to switch off the light on closing?", 
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if switch_off==QtWidgets.QMessageBox.Yes:
            self.send_light_value(0)
        else:
            pass
        
        sys.stdout.write("\n\n Closing... \n\n Killing mqtt-monitor thread.... \n")
        self.mqtt_listener.alive = False
        try:
            self.stim_widget.timer.alive = False
            sys.stdout.write("\nCleaning up remaining timer-threads...")
        except:
            sys.stdout.write("\nNo remaining timer-threads found")
        

        sys.stdout.write("\n\nGood Bye")
        event.accept()
    def test_parent(self):
        print("whhoooooo buddy")
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtWidgets.QApplication.instance().exec_()