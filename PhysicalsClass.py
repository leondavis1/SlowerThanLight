# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 16:56:19 2018

@author: Cobi
"""
import numpy as np
from ViewingSensor import Sensor
from WorldlineClass import Worldline
from LocationClass import Location


class Physical:
    """Physical objects that live in a Universe. They exist at a spacetime
    location with an orientation in space and velocity through space. Each
    Physical leaves behind a Worldline of events. Finally, each Physical has
    a Sensor which is the way it perceives other Physicals.
    
    Note: this class is meant to be extended to specific physical objects (for
    example, Ships or Asteroids). BE SURE TO OVERWRITE THE compress() AND
    decompress() METHODS!
    """
    
    def __init__(self,x,v,t,univ,isghost=False):
        """If isghost, the Physical is built as normal but without informing
        the Universe or building a Worldline for it."""
        self.univ = univ
        self.loc = Location(t,x)
        if self.loc.dim()==1:
            v = [v]
        self.v = np.array(v)
        assert(len(self.v) == self.loc.dim())
        #Finished with descriptive fields. Now add to Universe
        self.linekey = None
        self.key = None
        if not isghost:
            worldline = Worldline(univ) #build new Worldline (it adds itself to to univ.History)
            worldline.add_event(self.loc,type(self),self.compress())
            self.linekey = worldline.key
            self.sensor = Sensor(self.loc,univ,ownkey=self.linekey)
            #inform rest of Universe about the new Worldline
            for physkey, phys in univ.Physicals.items():
                phys.sensor.watch_new_line(self.linekey)
            self.key = univ.add_physical(self)

    def boost(self,dv):
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
        self.univ.get_worldline(self.linekey).add_event(self.loc,type(self),self.compress())
        self.sensor.loc = self.loc #update sensor so it knows where its Physical is

    def destroy(self):
        self.univ.del_physical(self.key)
    
    def get_worldline(self):
        return self.univ.get_worldline(self.linekey)
    
    def find_collided(self,impactradius):
        """return a list of all Events that this Physical can see which are
        within impactradius of itself"""
        impactlist = []
        for ev in self.sensor.get_visible():
            if ev.length_to(self.loc) <= impactradius:
                impactlist.append(ev)
                
    def see_visible(self):
        """return a list of all Events that this Physical can see"""
        return self.sensor.get_visible()
        
###-------------------------------------------------------------------------### BELOW THIS LINE IS STILL TO DO
    def compress(self):
        """give enough info to reconstruct the Physical as it was at this
        current point in spacetime, in as short a string as possible"""
        descrip = "L%0.2f" %self.loc.t
        for coord in self.loc.space():
            descrip += ",%0.2f" %coord
        descrip += "V%0.2f" % self.v[0]
        for vel in self.v[1:]:
            descrip += ",%0.2f" %vel
        descrip += "END"
        return descrip
    
    def decompress(cipherstring):
        """take in a compressed string following the compress method convention
        and returns a ghost Physical that matches the description.
        Note that this is a class method, NOT a instance method."""
        indxL = cipherstring.index("L")
        indxV = cipherstring.index("V")
        endex = cipherstring.index("END")
        tx = [float(x) for x in cipherstring[indxL+1:indxV].split(",")]
        v  = [float(x) for x in cipherstring[indxV+1:endex].split(",")]
        return Physical(tx[1:],v,tx[0],None,isghost=True)
    
