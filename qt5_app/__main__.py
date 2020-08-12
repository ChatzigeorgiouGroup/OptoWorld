#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 14:23:46 2020

@author: daniel
"""



from mainwindow_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import paho.mqtt.client as client
import sys
import time

class Light_Switch():
    def __init__(self, broker_address, client_name,light_state = 0, port = 1883):
        self.client_name = client_name
        self.client = client.Client(client_name)
        self.client.connect(broker_address, port)
        self.light_state = light_state
        
    def switch(self, val):
        
        self.client.publish("optoworld/switch", val)
        
    def sync_with_world(self):
        self.switch()
        time.sleep(0.1)
        self.switch()
        
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
#        self.switch = Light_Switch("192.168.1.9", "light_switch")
        
        self.ui.button_lightswitch.clicked.connect(self.button_clicked)
        
        self.ui.dial.setMinimum(0)
        self.ui.dial.setMaximum(255)
        self.ui.dial.setValue(0)
        
    
    def button_clicked(self):
        switch = client.Client("Yay")
        switch.connect("192.168.1.9", port = 1883)
        switch.publish("optoworld/switch", self.ui.dial.value())
        switch.disconnect()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    #sys.exit(app.exec_())
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()
    