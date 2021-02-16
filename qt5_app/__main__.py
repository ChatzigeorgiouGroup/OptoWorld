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
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from Tools.Stim_tools.Stim_tools import Timer
from Tools.Stim_tools.Stim_tools import Stim_widget
from Tools.MQTT_tools import MQTT_Listener
from Tools.PlotWidget import PlotWidget
from threading import Thread

BROKER_IP = "192.168.1.4"

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("OptoWorld")
        self.start_mqtt()

        self.ui.button_lightswitch.clicked.connect(self.button_clicked)
        self.ui.actionedit_light_profile.triggered.connect(self.edit_light_profile)
        self.ui.actionshow_live_graphs.triggered.connect(self.toggle_live_graphs)
        self.make_graphs()


    def start_mqtt(self):
        start_thread = Thread(target=self.start_mqtt_thread, )
        start_thread.start()

    def start_mqtt_thread(self):
        self.connected = False
        start_time = time.time()
        while not self.connected:
            try:
                self.mqtt_listener = MQTT_Listener(BROKER_IP, "listener")
                self.ui.label_mqtt_status.setText("Connected to Broker")
                self.ui.label_mqtt_status.setStyleSheet("color: green")
                self.mqtt_listener.signals.new_status.connect(self.update_status_labels)
                self.mqtt_listener.signals.disconnected.connect(self.start_mqtt)
                self.threadpool = QtCore.QThreadPool()
                self.threadpool.start(self.mqtt_listener)
                self.connected = True
            except Exception as e:
                self.ui.label_mqtt_status.setText(f"Broker not found. ({int(time.time()-start_time)}s)")
                self.ui.label_mqtt_status.setStyleSheet("color: red")
                self.connected = False
                sys.stdout.write(str(e))
                time.sleep(1)
        self.plotting = False
        self.ui.framePlotWidget.setVisible(False)




    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            self.close()
        elif event.key() == QtCore.Qt.Key_Plus:
            self.send_light_value(255)
        elif event.key() == QtCore.Qt.Key_Minus:
            self.send_light_value(0)

    def edit_light_profile(self):
        if not hasattr(self, "stim_widget"):        
            self.stim_widget = Stim_widget(parent = self)
        self.dock = self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.stim_widget)
        # self.dock.setWidget(self.stim_widget)
        self.stim_widget.show()

    def button_clicked(self):
        self.send_light_value(self.ui.slider_light.value())
        
    def send_light_value(self, val):
        switch = client.Client("Yay")
        switch.connect(BROKER_IP, port = 1883)
        switch.publish("optoworld/switch", val)
        switch.disconnect()

    def update_status_labels(self, m):
        temperature, light_value, light_intensity = str(m).split("_")
        self.ui.label_status_temperature.setText(f"Temperature: {temperature} C")
        self.ui.label_status_light.setText(f"Light Value: {light_value}")
        self.ui.label_status_light_intensity.setText(f"Light Level: {light_intensity} lux")

        df = pd.DataFrame()
        df["date"] = [datetime.datetime.now().strftime("%Y%m%d")]
        df["time"] = [time.strftime("%H:%M:%S")]
        # df["time"] = time.time()?
        df["temperature"] = [float(temperature)]
        df["value"] = [int(light_value)]
        df["intensity"] = [float(light_intensity)]

        try:
            self.df = pd.concat([self.df, df], ignore_index=True)
        except Exception as e:
            self.df = df

        if self.plotting == True:
            self.update_plots(self.df[-100:])

    def toggle_live_graphs(self):
        if self.plotting == False:
            self.plotting = True
            self.ui.framePlotWidget.setVisible(True)
        else:
            self.plotting = False
            self.ui.framePlotWidget.setVisible(False)
    def update_plots(self, df):


        try:
            frame_height = self.ui.framePlotWidget.size().height()
            if frame_height < 700:
                fs = 6
            elif frame_height > 700 and frame_height < 800:
                fs = 8
            else:
                fs = 10
            self.axes_temperature.clear()
            self.axes_temperature.plot(df["time"], df["temperature"])
            self.axes_temperature.set_ylabel('Temperature (C)', fontsize= fs)

            self.axes_intensity.clear()
            self.axes_intensity.set_ylim(0,1050)
            self.axes_intensity.plot(df["time"], df["intensity"])
            self.axes_intensity.set_ylabel('Intensity (lux)', fontsize= fs)

            self.axes_light_value.clear()
            self.axes_light_value.set_ylim(0,300)
            self.axes_light_value.plot(df["time"], df["value"])
            self.axes_light_value.set_ylabel('Value (0-255)', fontsize= fs)


            for ax in [self.axes_temperature, self.axes_intensity, self.axes_light_value]:
                ax.set_xlabel("Time")
                ax.xaxis.set_major_locator(plt.MaxNLocator(15))

            self.plot.canvas.figure.autofmt_xdate()
            self.plot.draw()
            self.plot.canvas.figure.tight_layout()
        except Exception as e:
            print(str(e))


    def make_graphs(self):
        # self.plot_temperature = PlotWidget()
        # self.plot_light_intensity = PlotWidget()
        # self.plot_light_value = PlotWidget()
        self.plot = PlotWidget()

        self.ui.framePlotWidget.setLayout(QtWidgets.QVBoxLayout())

        self.ui.framePlotWidget.layout().addWidget(self.plot)
        self.axes_temperature = self.plot.canvas.figure.add_subplot(311)
        self.axes_intensity = self.plot.canvas.figure.add_subplot(312)
        self.axes_light_value = self.plot.canvas.figure.add_subplot(313)

        # for widget in [self.plot_light_intensity, self.plot_light_value, self.plot_temperature]:
        #     self.ui.framePlotWidget.layout().addWidget(widget)
        # self.axes_temperature = self.plot_temperature.canvas.figure.gca()
        # self.axes_intensity = self.plot_light_intensity.canvas.figure.gca()
        # self.axes_light_value = self.plot_light_value.canvas.figure.gca()

    def closeEvent(self, event):
        switch_off = QtWidgets.QMessageBox.question(self, "Switch Off?","Do you want to switch off the light on closing?", 
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if switch_off==QtWidgets.QMessageBox.Yes:
            self.send_light_value(0)
        else:
            pass
        
        sys.stdout.write("\n\n Closing... \n\n Killing mqtt-monitor thread.... \n")
        self.mqtt_listener.alive = False
        self.mqtt_listener.client.disconnect()
        try:
            self.stim_widget.timer.alive = False
            self.stim_widget.timer.client.disconnect()
            sys.stdout.write("\nCleaning up remaining timer-threads...")
        except:
            sys.stdout.write("\nNo remaining timer-threads found")
        
        self.df.to_csv("dataframe_test_long_profile.csv", sep = "\t")
        sys.stdout.write("\n\nGood Bye")
        event.accept()



        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtWidgets.QApplication.instance().exec_()
