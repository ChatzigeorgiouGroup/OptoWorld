#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 09:46:21 2020

@author: daniel
"""

from mainwindow_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import paho.mqtt.client as client
import sys
import time


class Signals(QtCore.QObject):
    new_light_value = QtCore.pyqtSignal(int)
    new_temperature_value = QtCore.pyqtSignal(float)
    new_light_level_value = QtCore.pyqtSignal(float)

class MQTT_Listener(QtCore.QRunnable):
    def __init__(self, broker_address, client_name, port = 1883):
        QtCore.QRunnable.__init__(self)
        self.signals = Signals()
        self.client_name = client_name
        self.client = client.Client(client_name)
        self.client.connect(broker_address, port)
        self.client.subscribe("optoworld/blue_val")
        self.client.subscribe("optoworld/temperature")
        self.client.subscribe("optoworld/light_level")
        self.client.on_message = self.on_mqtt_message

    def on_mqtt_message(self, client, userdata, message):
        m = message.payload.decode()
        # sys.stdout.write(f"Message on topic {message.topic}: {m} \n")
        if "temperature" in message.topic:
            self.signals.new_temperature_value.emit(float(m))
        elif "blue" in message.topic:
            self.signals.new_light_value.emit(int(m))
        elif "level" in message.topic:
            self.signals.new_light_level_value.emit(float(m))
    
    @QtCore.pyqtSlot()
    def run(self):
        self.alive = True
        while self.alive:
            self.client.loop()

        self.client.disconnect()
            
         