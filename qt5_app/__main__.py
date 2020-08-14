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

class Signals(QtCore.QObject):
    new_light_value = QtCore.pyqtSignal(int)
    new_temperature_value = QtCore.pyqtSignal(float)
    new_light_level_value = QtCore.pyqtSignal(float)

class MQTT_pyqt(QtCore.QRunnable):
    def __init__(self, broker_address, client_name, port = 1883):
        QtCore.QRunnable.__init__(self)
        self.client_name = client_name
        self.client = client.Client(client_name)
        self.client.connect(broker_address, port)
        self.client.subscribe("optoworld/blue_val")
        self.client.subscribe("optoworld/temperature")
        self.client.subscribe("optoworld/light_level")
        self.client.on_message = self.on_mqtt_message
        
        self.signals = Signals()
        
    def on_mqtt_message(self, client, userdata, message):
        m = message.payload.decode()
        sys.stdout.write(f"Message on topic {message.topic}: {m} \n")
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
            
class Timer(QtCore.QRunnable):
    def __init__(self, broker_address = "192.168.1.9", port = 1883, client_name = "timer"):
#        self.timing_df = timing_df
        QtCore.QRunnable.__init__(self)
        self.client_name = client_name
        self.broker_address = broker_address
        self.port = port
        
    @QtCore.pyqtSlot()
    def run(self):
        on_time = 5
        off_time = 3
        
        self.client = client.Client(self.client_name)
        self.client.connect(self.broker_address, self.port)
        self.alive = True
        while self.alive:
            self.client.publish("optoworld/switch", 255)
        
            time.sleep(on_time)
            self.client.publish("optoworld/switch", 0)
        
            time.sleep(off_time)
            
            
             
        
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.button_lightswitch.clicked.connect(self.button_clicked)
        
        self.mqtt_listener = MQTT_pyqt("192.168.1.9", "listener")
        self.threadpool = QtCore.QThreadPool()
        self.threadpool.start(self.mqtt_listener)
        self.mqtt_listener.signals.new_light_value.connect(self.update_value_label)
        self.mqtt_listener.signals.new_temperature_value.connect(self.update_temperature_label)
        self.mqtt_listener.signals.new_light_level_value.connect(self.update_light_level_label)
        
    def button_clicked(self):
#        self.send_light_value(self.ui.slider_light.value())
        self.timer = Timer()
        self.threadpool.start(self.timer)
        
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
        self.mqtt_listener.alive = False
        self.timer.alive = False
        
        switch_off = QtWidgets.QMessageBox.question(self, "Switch Off?","Do you want to switch off the light on closing?", 
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if switch_off==QtWidgets.QMessageBox.Yes:
            self.send_light_value(0)
        else:
            pass
        sys.stdout.write("Good Bye")
        event.accept()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtWidgets.QApplication.instance().exec_()