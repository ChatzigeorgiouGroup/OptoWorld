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
import sys  # We need sys so that we can pass argv to QApplication
import os
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
            

