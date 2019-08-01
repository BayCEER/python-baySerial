#!/usr/bin/python
# -*- coding: utf-8 -*-

import baySerial
from bayeosgatewayclient import BayEOSWriter, BayEOSSender
import tempfile
from os import path
from threading import Thread, Lock
from time import sleep

PATH = path.join(tempfile.gettempdir(),'bayeos-device') 
writer = BayEOSWriter(PATH)

NAME = 'BayEOSSerial-Thread-Example'
URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'

writer = BayEOSWriter(PATH)
writer.save_msg('Writer was started.')

sender = BayEOSSender(PATH, NAME, URL)
sender.start()

ser = baySerial.BaySerial()
ser.begin('/dev/ttyUSB0',9600)

lock=Lock();

def handleSerial():
    while True:
        frame=ser.getFrame()
        if not frame==False:
            # get lock for writer
            lock.acquire()
            writer.save_frame(frame['frame'], frame['ts'], "Serial1",True)
            lock.release()


t = Thread(target=handleSerial, args=())
t.start()


while(True):
    print "Main loop"
    sleep(10) 



