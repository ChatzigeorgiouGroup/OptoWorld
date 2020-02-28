#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:19:16 2020

@author: daniel
"""


import paho.mqtt.client as client
import threading
import queue
import os
import datetime, time
import sys




class MQTT_connection(threading.Thread):
    def __init__(self, broker_address, client_name, port = 1883):
        threading.Thread.__init__(self)
        self.client_name = client_name
        self.client = client.Client(client_name)
        self.client.connect(broker_address, port)
        self.client.on_message = self.on_mqtt_message
        
        
    def subscribe(self, topics):
        for topic in topics:
            self.client.subscribe(topic)
            
    def on_mqtt_message(self, client, userdata, message):
        m = message.payload.decode()
        sys.stdout.write(f"Message on topic {message.topic}: {m} \n")
        
    def run(self):
        self.alive = True
        sys.stdout.write(f"\n Starting mqtt object {self.client_name} \n")
        while self.alive:
            self.client.loop()
    def stop(self):
        self.alive = False
        

class Light_monitor(MQTT_connection):
    def __init__(self, *args, **kwargs):
        MQTT_connection.__init__(self, *args, **kwargs)
        self.subscribe(["optoworld/lightstatus"])
        self.light_state = 0
        self.start()
        
    def on_mqtt_message(self, client, userdata, message):
        self.light_state = int(message.payload.decode())
        sys.stdout.write(self.light_state)
        
class Listener(MQTT_connection):
    def __init__(self, broker_address, client_name, path = "./", *args, **kwargs):
        MQTT_connection.__init__(self, broker_address, client_name, *args, **kwargs)
        self.path = path
        self.create_logfile()
        self.subscribe(["optoworld/temperature"])
        self.light_monitor = Light_monitor(broker_address, client_name+"_lightmonitor", *args, **kwargs)
        self.start()
    
    def create_logfile(self):
        name = datetime.datetime.now().strftime("%Y%m%d_optoworld_temps.txt")
        self.filename = os.path.join(self.path, name)
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                f.write("date\ttime\ttemperature\tlightstate\n")
        
    def on_mqtt_message(self, client, userdata, message):
        self.create_logfile()
        t = message.payload.decode()
        with open(self.filename, "a") as f:
            f.write(datetime.datetime.now().strftime("%Y%m%d\t%H:%M:%S\t")+ t +"\t"+ str(self.light_monitor.light_state) + "\n")
       
class Light_Switch(MQTT_connection):
    def __init__(self, *args, **kwargs):
        MQTT_connection.__init__(self, *args, **kwargs)
        self.light_state = 0
        
    def switch(self):
        if self.light_state == 1:
            self.light_state = 0
        else:
            self.light_state = 1
            
        self.client.publish("optoworld/switch", self.light_state)
        
    def sync_with_world(self):
        self.switch()
        time.sleep(0.1)
        self.switch()
        
        
        
        
        
if __name__ == "__main__":
    pass
#    listener = Listener(broker_address = "192.168.1.3", client_name = "listener", path = "/mnt/NAS/optoworld_logs")
#    s = Light_Switch(broker_address = "192.168.1.3", client_name = "switch")
        
        
        
        
        
        
        
        
        
        
        
        
        

#class MQTT_connection_2(threading.Thread):
#    def __init__(self, broker_address, port = 1883, path = "./"):
#        threading.Thread.__init__(self)
#        self.client = client.Client("read_temperatures")
#        self.client.connect(broker_address, port)
#        self.path = path
#        self.client.on_message = self.on_mqtt_message
#        self.light_state = 0
#        self.alive = False
#        self.client.subscribe("optoworld/temperature")
#        self.client.subscribe("optoworld/lightstatus")
#        self.q = queue.Queue(maxsize = 10)
#        self.start()
#        self.create_logfile()
#
#    def create_logfile(self):
#        name = datetime.datetime.now().strftime("%Y%m%d_optoworld_temps.txt")
#        self.filename = os.path.join(self.path, name)
#        if not os.path.exists(self.filename):
#            with open(self.filename, "w") as f:
#                f.write("date\ttime\ttemperature\tlightstate\n")
#                
#    def on_mqtt_message(self, client, userdata, message):
#        if message.topic == "optoworld/temperature":
#            t = message.payload.decode()
#            self.q.put(float(t))
#            self.create_logfile()
#            with open(self.filename, "a") as f:
#                f.write(datetime.datetime.now().strftime("%Y%m%d\t%H:%M:%S\t")+ t +"\t"+ str(self.light_state) + "\n")
#        if message.topic == "optoworld/lightstatus":
#            self.light_state = int(message.payload.decode())
#          
#        
#    def switch_lights(self):
#        if self.light_state == 0:
#            self.light_state = 1
#        else:
#            self.light_state = 0
#        self.client.publish("optoworld/switch", int(self.light_state))
#    
#    def run(self):
#        self.alive = True
#        while self.alive:
#            self.client.loop()
#    def stop(self):
#        self.alive = False
#            

