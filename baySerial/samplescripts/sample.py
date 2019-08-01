#!/usr/bin/python
# -*- coding: utf-8 -*-

import baySerial
from bayeosgatewayclient import BayEOSFrame

ser = baySerial.BaySerial()

ser.begin('/dev/ttyUSB0',9600)

while(True):
    frame=ser.getFrame()
    if(not frame==False):
        # print(frame)
        print(BayEOSFrame.parse_frame(frame['frame']))



