# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 21:42:09 2016

@author: Mikes
"""
import serial 
import time
from pilotControl import pltInput


#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

class xBeeComm(object):

    def __init__(self):    
        
        self.ser = serial.Serial()
        #ser.port = "/dev/ttyUSB0"
        self.ser.port = "COM5"
        #ser.port = "/dev/ttyS2"
        self.ser.baudrate = 57600
        self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.ser.parity = serial.PARITY_NONE #set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        #ser.timeout = None          #block read
        self.ser.timeout = 1            #non-block read
        #ser.timeout = 2              #timeout block read
        self.ser.xonxoff = False     #disable software flow control
        self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 2     #timeout for write

    
    def __exit__(self):
        try:    
            self.ser.close()
        except Exception as ce:
            print("error closing/exiting serial port: " + str(ce))
            
    def main(self):
        
        try:             

            self.ser.open()
            self.ser.flushInput() #flush input buffer, discarding all its contents
            self.ser.flushOutput()#flush output buffer, aborting current output 
                         #and discard all that is in buffer
        except Exception as e:
            print("error open serial port: " + str(e))
            exit()
        
        while self.ser.isOpen():
        
            try:   
                #write data
                self.ser.write(pltInput.getBuffor())
                print(pltInput.getBuffor())
                time.sleep(.01)  #give the serial port sometime to receive the data 
                print("Bytes Sent")
            except Exception as e1:
                print("error communicating...: " + str(e1))
                self.ser.close()
                
        self.ser.close()  
        print("Serial Closed")
        
if __name__ == "__main__":
    text = xBeeComm()
    text.main()
