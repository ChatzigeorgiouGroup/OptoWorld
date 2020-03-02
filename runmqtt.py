#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 08:54:53 2020

@author: daniel
"""

from mqtt import Listener

l = Listener(broker_address="192.168.1.3", client_name="Listener")
