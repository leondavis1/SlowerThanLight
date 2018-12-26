# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 16:56:19 2018

@author: Cobi
"""
import numpy as np
from ViewingSensor import Sensor
from WorldlineClass import Worldline, Location, Event


class Thingy:
    """Physical objects that live in a Universe.  Each have a distinct id, a
    current Worldline, and some physical image.
    Fields:   univ  loc  v  theta  omega  worldkey  sensor  key
    """
        
#    Universe = {}
#    keycounter = 0 
    
    def __init__(self,x,v,t,univ):
        self.univ = univ
        self.loc = Location(t,x)
        if self.loc.dim()==1:
            v = [v]
        self.v = np.array(v)
        assert(len(self.v) == self.loc.dim())
        self.theta = 0 #orientation.  -----------------------------------------IMPLEMENT FURTHER LATER
        self.omega = 0 #orientation.  -----------------------------------------IMPLEMENT FURTHER LATER
        
        worldline = Worldline(univ) #build new Worldline (it adds itself to to History)
        worldline.add_event(self.loc,self.compress())
        self.worldkey = worldline.key
        self.sensor = Sensor(self.loc, self.worldkey,univ)
        
        #inform rest of Universe about the new Worldline
        for tkey, thing in univ.Physicals.items():
            thing.sensor.add_line(self.worldkey)
        self.key = univ.add_thingy(self)

    def maneuver(self,dv):
        if self.loc.dim() ==1:
            dv = [dv]
        dv = np.array(dv)
        self.v = self.v + dv
        if np.sum(self.v**2) > self.univ.lightspeed**2:  #can't exceed lightspeed
            self.v = (self.v / np.sqrt(np.sum(self.v**2)))*(self.univ.lightspeed*0.999)
    
    def drift(self, dt=1):
        #update location
        assert(self.loc.dim() == len(self.v))
        self.loc.t += dt
        self.loc.x += self.v[0]*dt
        if self.loc.dim()>=2: self.loc.y += self.v[1]*dt
        if self.loc.dim()>=3: self.loc.z += self.v[2]*dt
        self.theta += self.omega*dt #update angle
        self.univ.History[self.worldkey].add_event(self.loc,self.compress())
        self.sensor.loc = self.loc #update the sensor so it knows where Thingy is

    def destroy(self):
        self.univ.History[self.worldkey].add_event(self.loc,"explode")  #------PUT "DESTROYED" COMPRESSION HERE
        del self.univ.Physicals[self.key]
    
    def compress(self):
        """give enough info to reconstruct what the Thingy was doing at this
        current point in spacetime, in as short a string as possible"""
        return "placeholderstring"
  