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
import sys


class Timer(QtCore.QRunnable):
    def __init__(self, timing_df, broker_address = "192.168.1.9", port = 1883, client_name = "timer"):
        self.timing_df = timing_df
        QtCore.QRunnable.__init__(self)
        self.client_name = client_name
        self.broker_address = broker_address
        self.port = port
        
    @QtCore.pyqtSlot()
    def run(self):
        self.client = client.Client(self.client_name)
        self.client.connect(self.broker_address, self.port)
        self.alive = True
        total_time = self.timing_df.on_duration.sum() + self.timing_df.off_duration.sum()
        sys.stdout.write(f"About to execute {len(self.timing_df)} stimuli. Total run time: {total_time} seconds.")
        for index, row in self.timing_df.iterrows():
            sys.stdout.write(f"\n Currently executing {index}")
            self.client.publish("optoworld/switch", row["intensity"])
            time.sleep(row["on_duration"])
            self.client.publish("optoworld/switch", 0)
            time.sleep(row["off_duration"])
            
class Stim_widget(QtWidgets.QDockWidget, Ui_DockWidget):
    def __init__(self, stim_df = False):
        QtWidgets.QDockWidget.__init__(self)
        Ui_DockWidget.__init__(self)
        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Stimulus Profile")
        self.connect_ui()
        
        
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
        
    def display_stim_df(self):
        model = pandasModel(self.stim_df)
        self.ui.tableView.setModel(model)
        
    def add_stim_to_profile(self):
        on_duration = self.ui.spinBox_on_duration.value()
        off_duration = self.ui.spinBox_off_duration.value()
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
    
        
        
        
        
        