# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 11:26:41 2018
@author: Cobi

CONTAINS THE FOLLOWING CLASSES: Universe, Location, Event
"""

import numpy as np


class Universe:
    """All of the physical objects, and their history as Worldlines, in a
    single causally-connected universe.  Thingys with different Universes
    have no way to interact"""
    
    def __init__(self,lightspeed=5,radius=500):
        self.Physicals = {}
        self.thingy_counter = 0
        self.History = [] #indexed so History[Worldline.key] gets corresponding Worldline
        self.worldline_counter = 0
        self.lightspeed = lightspeed
        self.size = radius #radius of the universe
    def increment(self,dt=1):
#        shiptime = None
        for thing in self.Physicals.values():
#            if shiptime is None:
#                shiptime = thing.loc.t
            thing.drift(dt)        
#        if shiptime is not None:
#            for line in self.History:
#                line.prune(shiptime)
        
    def add_worldline(self,line):
        """give the new worldline a key and add it to self.History"""
        key = self.worldline_counter
        self.worldline_counter = (self.worldline_counter+1)%10000  ###---------limit 10,000 distinct worldlines
        #add the line to History at the location dictated by key
        if key == len(self.History): #key is index of slot 1 space after list ends
            self.History.append(line)
        else:
            self.History[key] = line
        return key
    def add_thingy(self,thingy):
        """give the new Thingy a key and add it to self.Physicals"""
        key = self.thingy_counter
        self.thingy_counter = (self.thingy_counter+1)%10000  ###---------------limit 10,000 distinct thingies
        self.Physicals[key] = thingy
        return key


class Location:
    """a location in spacetime.
        Either: x in an array of length between 1 and 3,
            or: x,y,z are spatial coords (for dim<3, leave z and/or y as Nones
        and t for time
        """
    def __init__(self,t,x,y=None,z=None):
        self.t=t; self.x=None; self.y=None; self.z=None
        try:
            d = len(x) #if x is a single real number this raises TypeError
            self.x = x[0]
            if d>=2: self.y = x[1]
            if d>=3: self.z = x[2]
        except TypeError:
            self.x=x; self.y=y; self.z=z
    def space(self):
        return np.array([v for v in [self.x,self.y,self.z] if v is not None])
    """number of spatial dimentions"""
    def dim(self):
        return len(self.space())
    """spatial separation between self and another Location"""
    def lengthto(self,loc2):
        assert(self.dim() == loc2.dim())
        return np.sqrt(np.sum((self.space() - loc2.space())**2))
    def duplicopy(self):
        return Location(self.t,self.x,self.y,self.z)
        

class Event:
    """A location in space-time and the parameters of the physical object
    which was there at that time.  The parameters are not themselves a Thingy,
    just some sort of compressed description that can be later expanded and
    used to see what had happened at this Event."""
    def __init__(self,loc,descrip):
        self.loc = loc
        self.descrip = descrip
    """given a viewing space-time location, return the boolean 'light has had
    time to travel from the Event to the viewer'"""
    def is_visible(self,loc2,c=10):
        assert(self.loc.dim()==loc2.dim())
        spatial = self.loc.lengthto(loc2)
        return ((loc2.t - self.loc.t)*c >= spatial)