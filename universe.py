# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 11:26:41 2018
@author: Cobi

"""

class Universe:
    """All of the physical objects, and their history as Worldlines, in a
    single causally-connected universe.  Objects with different Universes
    have no way to interact"""

    MAX_PHYSICALS = 10000

    def __init__(self,lightspeed=5,radius=500, max_physicals=None):
        self.max_physicals = max_physicals if max_physicals is not None else self.MAX_PHYSICALS

        self._physicals = [None] * self.max_physicals #list of Physicals
        self.physicals_counter = 0
        self.History = [] #list of Worldlines, indexed so History[Worldline.key] gets corresponding Worldline
        self.worldline_counter = 0
        self.lightspeed = lightspeed
        self.radius = radius #radius of the universe

    @property
    def Physicals(self):
        return [p for p in self._physicals if p is not None]
    
    def increment(self,dt=1):
        """Perform a timestep of length dt of the universe. Move physical
            objects and delete Worldlines that have already been seen fully"""
        for line in self.History:
            line.timer += dt
            line.prune()
        for thing in self.Physicals:
            thing.drift(dt)

    def add_worldline(self,line):
        """Given a new Worldline, add it to the Universe's history"""
        key = self.worldline_counter
        self.worldline_counter = (self.worldline_counter+1)%10000  ###---------limit 10,000 distinct worldlines
        #add the line to History at the location dictated by key
        if key == len(self.History): #key is index of slot 1 space after list ends
            self.History.append(line)
        else:
            self.History[key] = line
        return key
    
    def get_worldline(self,linekey):
        return self.History[linekey]
    
    def del_worldline(self,linekey):
        self.History[linekey] = None
    
    def add_physical(self,physical):
        """Give a new Physical, add it to the Universe's list of objects"""
        key = self.physicals_counter
        self.physicals_counter = (self.physicals_counter+1)%10000  ###---------------limit 10,000 distinct thingies
        self._physicals[key] = physical
        return key

    def get_physical(self,physkey):
        return self._physicals[physkey]
    
    def del_physical(self,physkey):
        self._physicals[physkey] = None
