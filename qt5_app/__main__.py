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
    new_value = QtCore.pyqtSignal(int)

class MQTT_pyqt(QtCore.QRunnable):
    def __init__(self, broker_address, client_name, port = 1883):
        QtCore.QRunnable.__init__(self)
        self.client_name = client_name
        self.client = client.Client(client_name)
        self.client.connect(broker_address, port)
        self.client.subscribe("optoworld/blue_val")
        self.client.on_message = self.on_mqtt_message
        
        self.signals = Signals()
        
    def on_mqtt_message(self, client, userdata, message):
        m = message.payload.decode()
        sys.stdout.write(f"Message on topic {message.topic}: {m} \n")
        self.signals.new_value.emit(int(m))
    
    @QtCore.pyqtSlot()
    def run(self):
        self.alive = True
        while self.alive:
            self.client.loop()
             
        
        
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
        self.mqtt_listener.signals.new_value.connect(self.update_value_label)

    
    def button_clicked(self):
        self.send_light_value(self.ui.slider_light.value())
        
    def send_light_value(self, val):
        switch = client.Client("Yay")
        switch.connect("192.168.1.9", port = 1883)
        switch.publish("optoworld/switch", val)
        switch.disconnect()

    def update_value_label(self, new_val):
        self.ui.label_status_light.setText(str(new_val))
        
    def closeEvent(self, event):
        self.mqtt_listener.alive = False
        
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