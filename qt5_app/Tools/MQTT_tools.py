#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 09:46:21 2020

@author: daniel
"""

from mainwindow_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import paho.mqtt.client as client
import pandas as pd
import sys
import time


class Signals(QtCore.QObject):
    new_status = QtCore.pyqtSignal(str)
    disconnected = QtCore.pyqtSignal()

class MQTT_Listener(QtCore.QRunnable):
    def __init__(self, broker_address, client_name, port = 1883):
        QtCore.QRunnable.__init__(self)
        self.signals = Signals()
        self.client_name = client_name
        self.client = client.Client(client_name)
        self.client.on_message = self.on_mqtt_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_connect = self.on_connect
        self.client.connect(broker_address, port)
        # self.client.loop_start()
        self.connected=False
        time_spent = 0
        sys.stdout.write(f"\r Connecting to MQTT Broker... ")
        while not self.connected:
            self.client.loop()
            time.sleep(0.1)

        self.time_since_last_message = time.time()

    def on_mqtt_message(self, client, userdata, message):
        m = message.payload.decode()
        if "status" in message.topic.lower():
            self.signals.new_status.emit(str(m))

    def on_connect(self, client, userdata,flags, rc):
        self.connected = True
        self.client.subscribe("optoworld/status")
        sys.stdout.write("\n\rSuccesfully connected to MQTT Broker\n")

    def on_disconnect(self, client, userdata,flags, rc):
        self.signals.disconnected.emit()
        self.alive = False
        sys.stdout.write("DISCONNECTED!")

    @QtCore.pyqtSlot()
    def run(self):

        self.alive = True
        while self.alive:
            self.client.loop(.2)


        # self.signals.disconnected.emit()
        self.client.disconnect()
        sys.stdout.write("\n MQTT Listener Disconnected \n")
         