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
    new_status = QtCore.pyqtSignal(pd.core.frame.DataFrame)

class MQTT_Listener(QtCore.QRunnable):
    def __init__(self, broker_address, client_name, port = 1883):
        QtCore.QRunnable.__init__(self)
        self.signals = Signals()
        self.client_name = client_name
        self.client = client.Client(client_name)
        self.client.connect(broker_address, port)
        self.client.subscribe("optoworld/status")
        self.client.on_message = self.on_mqtt_message
        self.time_since_last_message = time.time()


    def on_mqtt_message(self, client, userdata, message):
        m = message.payload.decode()
        if "status" in message.topic.lower():
            # self.signals.new_status.emit(str(m))

            temperature, light_value, light_intensity = str(m).split("_")

            df = pd.DataFrame()
            df["time"] = [time.strftime("%H:%M:%S")]
            df["temperature"] = [float(temperature)]
            df["light_value"] = [int(light_value)]
            df["light_intensity"] = [float(light_intensity)]



            try:
                self.df = pd.concat([self.df, df])
            except Exception as e:
                self.df = df


            time_recieved = time.time()
            if time_recieved - self.time_since_last_message >= 5:
                self.signals.new_status.emit(self.df)
                self.time_since_last_message = time_recieved



    @QtCore.pyqtSlot()
    def run(self):
        self.alive = True
        while self.alive:
            self.client.loop()
        self.client.disconnect()
            
         