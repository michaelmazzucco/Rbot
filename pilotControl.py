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

        self._Fire = 0
        self._Strafe = 0
        self._Rate1 = 0
        self._Rate2 = 0
        self._Rate3 = 0
        self._Rate4 = 0
        self._Safe = 0
        self._Arm = 0
        
    
    def MoveFwd(self,val):
        self.lock.acquire()
        self._unset_Strafe()
        self._joystick[2] = self._clamp(val,0,1023)  
        self.lock.release()
        
    def MoveBack(self,val):
        self.lock.acquire()
        self._unset_Strafe()
        self._joystick[2] = self._clamp(val,0,1023)  
        print(self._joystick[2])
        self.lock.release()
        
    def MoveTurnRight(self,val):
        self.lock.acquire()
        self._unset_Strafe()
        self._joystick[3] = self._clamp(val,0,1023)          
        self.lock.release()
        
    def MoveTurnLeft(self,val):
        self.lock.acquire()
        self._unset_Strafe()
        self._joystick[3] = self._clamp(val,0,1023)         
        self.lock.release()
        
        
# Button 1
    def set_Safe(self):
        self.lock.acquire()
        self._Buttons1 |= 0x04
        self.lock.release()
        
    def unset_Safe(self):
        self.lock.acquire()
        self._Buttons1 &= ~0x04
        self.lock.release()
        
        
    
    def set_Arm(self):
        self.lock.acquire()
        self._Buttons1 |= 0x08
        self.lock.release()
        
    def unset_Arm(self):
        self.lock.acquire()
        self._Buttons1 &= ~0x08
        self.lock.release()
        
    def setTurretUp(self):
        self.lock.acquire()
        self._Buttons1 |= 0x10
        self.lock.release()
        
    def unsetTurretUp(self):
        self.lock.acquire()
        self._Buttons1 &= ~0x10
        self.lock.release()
        
    def setTurretLeft(self):
        self.lock.acquire()
        self._Buttons1 |= 0x20
        self.lock.release()
        
    def unsetTurretLeft(self):
        self.lock.acquire()
        self._Buttons1 &= ~0x20
        self.lock.release()
                
    def setTurretDown(self):
        self.lock.acquire()
        self._Buttons1 |= 0x40
        self.lock.release()
        
    def unsetTurretDown(self):
        self.lock.acquire()
        self._Buttons1 &= ~0x40
        self.lock.release()
                
        
    def setTurretRight(self):
        self.lock.acquire()
        self._Buttons1 |= 0x80
        self.lock.release()
        
    def unsetTurretRight(self):
        self.lock.acquire()
        self._Buttons1 &= ~0x80
        self.lock.release()

# Button 2        
    def set_Rate1(self,val):
        self.lock.acquire()
        self._Buttons2 = self._Buttons2 ^ 0x01
        self.lock.release()
        
    def set_Rate2(self,val):
        self.lock.acquire()
        self._Buttons2 = self._Buttons2 ^ 0x02
        self.lock.release()
        
    def set_Rate3(self,val):
        self.lock.acquire()
        self._Buttons2 = self._Buttons2 ^ 0x04
        self.lock.release()
        
    def set_Rate4(self,val):
        self.lock.acquire()
        self._Buttons2 = self._Buttons2 ^ 0x08
        self.lock.release()        
        
    def set_Fire(self):
        self.lock.acquire()
        self._Buttons2 |= 0x20
        self.lock.release()
        
    def unset_Fire(self):
        self.lock.acquire()
        self._Buttons2 &= ~0x20
        self.lock.release()        
    
    def _set_Strafe(self):
        self._Buttons2 |=  0x10
        
    def _unset_Strafe(self):
        self._Buttons2 &= ~0x10
        
    def MoveStrafeLeft(self,val):
        self.lock.acquire()
        self._set_Strafe()
        self._joystick[3] = self._clamp(val,0,1023)    
        self.lock.release() 
    
    def MoveStrafeRight(self,val):
        self.lock.acquire()
        self._set_Strafe()
        self._joystick[3] = self._clamp(val,0,1023)    
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
