# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 21:14:11 2016

@author: Mikes
"""

#//TODO: Figure out more sophisticated way of passing buffer.
# Create getters and setters
import threading    


class pilotControl(object):
    """Module provides user input object
    """
    
    def __init__(self):
        self.lock = threading.Lock()
        self._Header1 =  0xFF
        self._Header2 =  0xFF
        self._Buttons1 = 0x00
        self._Buttons2 = 0x00       
        self._joystick = [511, 511, 511, 511]      
        

    def setButtons1(self,val):
        self.lock.acquire()
        self._Buttons1 = val
        self.lock.release()
        
    def setButtons2(self,val):
        self.lock.acquire()
        self._Buttons2 = val
        self.lock.release()
        
    def setJoysticks(self, val1, val2, val3, val4):
        self.lock.acquire()
        self._joystick = [self._clamp(val1,0,1023), self._clamp(val2,0,1023), self._clamp(val3,0,1023), self._clamp(val4,0,1023)]
        self.lock.release()
        
    def _clamp(self, n, smallest, largest): 
        return max(smallest, min(n, largest))
    
    def _swap16(self, x):
        return bytes([(x & 0xFF)]) + bytes([(x >> 8) & 0xFF])
        
    def _hiByteVal(self, x):
        return ((x >> 8) & 0xFF)
        
    def _loByteVal(self, x):
        return (x & 0xFF)
        
    def _byteSum(self,x):
        return(self._hiByteVal(x) + self._loByteVal(x))
        
    def _checkSum(self):
        iChcksum = self._Buttons1 + self._Buttons2 + \
        self._byteSum(self._joystick[0]) + self._byteSum(self._joystick[1]) + \
        self._byteSum(self._joystick[2]) + self._byteSum(self._joystick[3])
        return(bytes([255-(iChcksum & 0xFF)]))
        
    def getBuffor(self):
        self.lock.acquire()

        """Return a byte array for TX"""
        
        Buff = bytes([self._Header1]) + bytes([self._Header2]) + bytes([self._Buttons1]) \
        + bytes([self._Buttons2]) + self._swap16(self._joystick[3]) + self._swap16(self._joystick[2]) + self._swap16(self._joystick[1]) \
        + self._swap16(self._joystick[0]) + self._checkSum()
        
        self.lock.release()
        
        return Buff
        
pltInput = pilotControl()

        
if __name__ == "__main__":    
    print(pltInput.getBuffor())
