#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:19:16 2020

@author: daniel
"""


import paho.mqtt.client as client
import pyqtgraph
import threading
import queue
from PyQt5 import QtWidgets, QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
import datetime



class MQTT_connection(threading.Thread):
    def __init__(self, broker_address, port = 1883):
        threading.Thread.__init__(self)
        self.client = client.Client("read_temperatures")
        self.client.connect(broker_address, port)
        self.client.on_message = self.on_mqtt_message
        self.light_state = 0
        self.alive = False
        self.client.subscribe("optoworld/temperature")
        self.client.subscribe("optoworld/lightstatus")
        self.q = queue.Queue(maxsize = 10)
        self.start()
        self.create_logfile()

    def create_logfile(self):
        if not os.path.exists("testfile.txt"):
            with open("testfile.txt", "w") as f:
                f.write("date\ttime\ttemperature\tlightstate\n")
    def on_mqtt_message(self, client, userdata, message):
        if message.topic == "optoworld/temperature":
            t = message.payload.decode()
            self.q.put(float(t))
            self.create_logfile()
            with open("testfile.txt", "a") as f:
                f.write(datetime.datetime.now().strftime("%Y%m%d\t%H:%M:%S\t")+ t +"\t"+ str(self.light_state) + "\n")
        if message.topic == "optoworld/lightstatus":
            self.light_state = int(message.payload.decode())
          
        
    def switch_lights(self):
        if self.light_state == 0:
            self.light_state = 1
        else:
            self.light_state = 0
        self.client.publish("optoworld/switch", int(self.light_state))
    
    def run(self):
        self.alive = True
        while self.alive:
            self.client.loop()
    def stop(self):
        self.alive = False
            

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.mqtt = MQTT_connection()
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.button = QtWidgets.QPushButton("switch", self) 
        self.button.clicked.connect(self.on_click)
        
        
  

        self.x = [] # 100 time points
        self.y = []  # 100 data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
         # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.y.append(self.mqtt.q.get())
        self.mqtt.q.task_done()
        self.x = range(len(self.y))

        self.data_line.setData(self.x, self.y)  # Update the data.
        
    @QtCore.pyqtSlot()
    def on_click(self):
        print("click!")
        self.mqtt.switch_lights()

#if __name__ == "__main__":
#    app = QtWidgets.QApplication(sys.argv)
#    w = MainWindow()
#    w.show()
#    sys.exit(app.exec_())
#    w.mqtt.alive = False
