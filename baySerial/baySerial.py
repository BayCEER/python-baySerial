# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Python port of BaySerial PHP library
# Author: Stefan Holzheu <stefan.holzheu@bayceer.uni-bayreuth.de>
#
# 
# 
from time import time, sleep
import serial
from struct import pack, unpack
from serial.serialutil import XON, XOFF, to_bytes

XBEE_ESCAPE  = to_bytes([0x7d])
XBEE_DELIM = to_bytes([0x7e])
API_DATA = to_bytes([0x1])
API_ACK = to_bytes([0x2])
TX_OK = to_bytes([0x1])
TX_CHECKSUM_FAILED = to_bytes([0x2])
TX_BREAK = to_bytes([0x3])

class BaySerial:
    def __init__(self):
        self.ser=None
        self.stack=[]
        self.count=0;
    
    def begin(self,dev,baud=38400):
        self.ser=serial.Serial(dev,baud,timeout=0)
        
    def close(self):
        self.ser.close()
        self.ser=None
    
    def send(self,frame,api=API_DATA,timeout=120):
        frame=XBEE_DELIM+self._escape(pack("<B",len(frame))+api+frame+self._calcChecksum(api+frame))
        self.ser.write(frame)
        if(api != API_DATA):
            return 0;
        res = self.getFrame(timeout)
        if(res == False):
            return 2
        if(res['api']!=API_ACK):
            self.sendTXBreak()
            self.ser.write(frame)
        res = self.getFrame(timeout)
        if(res == False):
            return 2  
        
        if(res['api']==API_ACK):
            if(res['frame']==TX_OK):
                return 0
            if(res['frame']==TX_CHECKSUM_FAILED):
                return 1
            if(res['frame']==TX_BREAK):
                return 3
        return 2
    
    def read(self,count=1):
        data = self.ser.read(count)
        if( not len(data)):
            return self.count
        if( not len(self.stack)):
            delim_pos=data.find(XBEE_DELIM)
            if(delim_pos==-1):
                return 0
            data=data[delim_pos+1:len(data)]
        
        chunks=data.split(XBEE_DELIM)
        offset=len(self.stack)-1
        if(offset==-1):
            offset=0
        i=0
        while(i<len(chunks)):
            index=i+offset
            if(len(self.stack)==index):
                self.stack.append({'ts':time(),'ok':False})
            if(not 'rawframe' in self.stack[index]):
                self.stack[index]['rawframe']=chunks[i]
            else:
                self.stack[index]['rawframe']+=chunks[i]
            self.stack[index]['frame']=self._unescape(self.stack[index]['rawframe'])
            res=self._parseFrame(self.stack[index]['frame'])
            if(res==0):
                self.stack[index]['ok']=True
                self.count+=1
            if(res==1):
                del self.stack[index]
                offset=offset-1
            if((i+1)<len(chunks) and 'ok' in self.stack[index] and not self.stack[index]['ok']):
                del self.stack[index]
                offset=offset-1
            i=i+1
        
        anz=len(self.stack)
        if(anz>0 and not self.stack[anz-1]['ok']):
            anz=anz-1
        return anz
                
        
    
    
    def getFrame(self,timeout=120):
        while(self.read()==0 and timeout>0):
            sleep(0.001)
            timeout=timeout-0.001
        if(timeout<0):
            return False
        if(self.count==0):
            return False
        
        frame=self.stack[0]
        del self.stack[0]
        self.count-=1
        frame['api']=frame['frame'][1:2]
        frame['length']=frame['frame'][0:1]
        frame['frame']=frame['frame'][2:len(frame['frame'])-1]
        return frame

    
    def _parseFrame(self,frame):
        if(len(frame)<3):
            return 2
        l=len(frame)
        length=frame[0:1]
        checksum=frame[l-1:l]
        data=frame[1:l-1]
        calculatedLength=pack('<B',len(data)-1)
        if(calculatedLength==length):
            calculatedChecksum=self._calcChecksum(data)
            if(checksum == calculatedChecksum):
                self._sendAck(TX_OK)
                return 0
            else:
                self._sendAck(TX_CHECKSUM_FAILED)
                return 1
        return 2
    
        
    
    def _calcChecksum(self,data):
        checksum=0
        i=1
        while i<=len(data):
            checksum+=unpack('<B',data[i-1:i])[0]
            i=i+1
        checksum=checksum & 0xFF
        checksum = 0xFF - checksum
        checksum=pack('<B',checksum)
        return checksum
    
    def _escape(self,data):
        res=b''
        i=1
        while i<=len(data):
            if(data[i-1:i] in [XBEE_ESCAPE,XBEE_DELIM,XOFF,XON]):
                res=res+XBEE_ESCAPE+pack("<B",0x20^unpack('<B',data[i-1:i])[0])
            else:
                res=res+data[i-1:i]
            i=i+1
        return res
    
    def _unescape(self,data):
        res=b''
        i=1
        while i<=len(data):
            if(data[i-1:i]==XBEE_ESCAPE):
                i=i+1
                if(i<=len(data)):
                    res=res+pack("<B",0x20^unpack('<B',data[i-1:i])[0])
            else:
                res=res+data[i-1:i]
            i=i+1
        return res  
    
    def _sendAck(self,data):
        self.send(data,API_ACK)
    
    def sendTXBreak(self):
        self._sendAck(TX_BREAK)
        
        
      
   
    
    
    
    
   