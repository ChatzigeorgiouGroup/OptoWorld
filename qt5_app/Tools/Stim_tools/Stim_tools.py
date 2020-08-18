#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 09:37:46 2020

@author: daniel
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import time
import paho.mqtt.client as client
from collections import OrderedDict
import pandas as pd
from Tools.General.PandasModel import pandasModel
from Tools.Stim_tools.stim_widget_ui import Ui_DockWidget
import sys, os

BROKER_IP = "192.168.1.9"

class Signals(QtCore.QObject):
    starting = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

class Timer(QtCore.QRunnable):
    def __init__(self, timing_df, broker_address = BROKER_IP, port = 1883, client_name = "timer"):
        self.timing_df = timing_df
        QtCore.QRunnable.__init__(self)
        self.signals = Signals()
        self.client_name = client_name
        self.broker_address = broker_address
        self.port = port
        
    @QtCore.pyqtSlot()
    def run(self):
        self.signals.starting.emit()
        self.client = client.Client(self.client_name)
        self.client.connect(self.broker_address, self.port)
        self.alive = True
        total_time = self.timing_df.on_duration.sum() + self.timing_df.off_duration.sum()
        sys.stdout.write(f"About to execute {len(self.timing_df)} stimuli. Total run time: {total_time} seconds.")
        for index, row in self.timing_df.iterrows():
            if self.alive:
                sys.stdout.write(f"\n Currently executing {index}")
                self.client.publish("optoworld/switch", row["intensity"])
                time.sleep(row["on_duration"])
            else:
                break
            if self.alive:
                self.client.publish("optoworld/switch", 0)
                time.sleep(row["off_duration"])
            else:
                break
        self.client.disconnect()
        self.signals.finished.emit()
            
class Stim_widget(QtWidgets.QDockWidget, Ui_DockWidget):
    def __init__(self, stim_df = False, parent = None):
        QtWidgets.QDockWidget.__init__(self)
        Ui_DockWidget.__init__(self)
        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Stimulus Profile")
        self.connect_ui()
        self.parent = parent
            
        self.remove_stim_action = QtWidgets.QAction("&Remove Highlighted Stimuli", self, triggered = self.remove_stimuli)
        self.ui.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tableView.customContextMenuRequested.connect(self.contextMenuEvent_tableView)
        
        
        if not stim_df:
            self.stim_df = pd.DataFrame(columns = ["id","on_duration", "off_duration", "intensity"])
        else:
            self.stim_df = stim_df
        self.display_stim_df()
        
    
    def contextMenuEvent_tableView(self, event):
        menu = QtWidgets.QMenu(self)
        menu.addAction(self.remove_stim_action)
        menu.popup(self.ui.tableView.mapToGlobal(event))
    
    def remove_stimuli(self):
        to_remove = [x.data() for x in self.ui.tableView.selectedIndexes()]
        self.stim_df = self.stim_df[~self.stim_df["id"].isin(to_remove)]
        self.display_stim_df()
        
    def connect_ui(self):
        self.ui.button_add_stim.clicked.connect(self.add_stim_to_profile)
        self.ui.button_run.clicked.connect(self.run_profile)
        self.ui.button_save_profile.clicked.connect(self.save_profile)
        self.ui.button_load_profile.clicked.connect(self.load_profile)
        
    def display_stim_df(self):
        model = pandasModel(self.stim_df)
        self.ui.tableView.setModel(model)

    def hms_to_s(self, H, M, s):
        duration = (H*3600) + (M*60) + s
        return duration

    def add_stim_to_profile(self):
        on_duration_hour = self.ui.spinBox_on_hour.value()
        on_duration_minute = self.ui.spinBox_on_minute.value()
        on_duration_second = self.ui.spinBox_on_second.value()
        on_duration = self.hms_to_s(on_duration_hour, on_duration_minute, on_duration_second)

        off_duration_hour = self.ui.spinBox_off_hour.value()
        off_duration_minute = self.ui.spinBox_off_minute.value()
        off_duration_second = self.ui.spinBox_off_second.value()
        off_duration = self.hms_to_s(off_duration_hour,off_duration_minute, off_duration_second)

        intensity = self.ui.spinBox_intensity.value()
        repeats = self.ui.spinBox_repeats.value()
        
        stims = OrderedDict()
        for i in range(repeats):
            n = i + len(self.stim_df)
            stims[f"stim_{str(n).zfill(3)}"] = {"id": f"stim_{str(n).zfill(3)}",
                                                "on_duration": on_duration, 
                                                "off_duration": off_duration, 
                                                "intensity": intensity}
        
        stim_df = pd.DataFrame.from_dict(stims)
        self.stim_df = pd.concat([self.stim_df, stim_df.T])
        self.stim_df['id'] = [f"stim_{str(x).zfill(3)}" for x in range(len(self.stim_df))]
        self.display_stim_df()
    
    def run_profile(self):
        self.timer = Timer(self.stim_df)
        self.timer.signals.starting.connect(self.timer_started)
        self.timer.signals.finished.connect(self.timer_stopped)
        self.parent.threadpool.start(self.timer)

    def timer_started(self):
        self.parent.ui.button_lightswitch.setEnabled(False)

    def timer_stopped(self):
        self.parent.ui.button_lightswitch.setEnabled(True)

    def save_profile(self):
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(parent = self, directory = os.curdir, filter = ".txt",
                                                          options=QtWidgets.QFileDialog.DontUseNativeDialog)
        try:
            print(save_path)
            if not save_path.endswith(".txt"):
                save_path += ".txt"
            self.stim_df.to_csv(save_path, sep = "\t")
        except:
            print("Could not save this this file.")

    def load_profile(self):
        load_path, ok = QtWidgets.QFileDialog.getOpenFileName(parent = self, directory = os.curdir,
                                                              options=QtWidgets.QFileDialog.DontUseNativeDialog)
        try:
            self.stim_df = pd.read_csv(load_path, sep = "\t")
            for c in self.stim_df.columns:
                if "unnamed" in c.lower() and "0" in c.lower():
                    self.stim_df = self.stim_df.set_index(c)
            self.display_stim_df()
        except:
            sys.stdout.write("Not a valid profile file")
        
        