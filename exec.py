# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 00:05:28 2016

@author: Mikes
"""

import threading
import xBeeSerial
import HotKeyGui
from pilotControl import pltInput
import sys

xBee = xBeeSerial.xBeeComm()
GUI = HotKeyGui.Control()


def xBeeThread():
    xBee.main()
    
if __name__=='__main__':
                
    t = threading.Thread(name='xBee_Service', target=xBeeThread)
    
    try:
        t.start()
    except (KeyboardInterrupt, SystemExit):
        t._stop.
        sys.exit()

    
    GUI.main()
   
    
  

#for x in range(0,50):
    #test = xBee.pltControl.setButtons1(1)
    #print(x)

    #time.sleep(1)