# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 18:04:53 2018

@author: Cobi
"""
from WorldlineClass import Worldline


class Sensor:
    """An eye floating at a location in space-time in a given Universe.  It
    watches all worldlines not corresponding to its exception-key (representing
    the Thingy the sensor is attached to), and keeps track of the latest
    event in each worldline visible from its location.
    """
    
    def __init__(self, loc, ownkey,univ):
        self.univ = univ
        self.watchedlines = [] #Worldline id, Event (or None) pairs
        self.loc = loc
        for wline in self.univ.History:
            if wline.key != ownkey:
                ev = wline.find_latest_visible(self.loc,None)
                self.watchedlines.append((wline.key,ev))
                
    """Update-er function to find latest visible event in all lines it is watching"""
    def observe(self):
        j = 0
        while j < len(self.watchedlines):
            wkey,prev = self.watchedlines[j]
            ev = self.univ.History[wkey].find_latest_visible(self.loc,prev)
            if prev is not None and ev is None: #Worldline ended
                del self.watchedlines[j]
            else:
                self.watchedlines[j] = (wkey,ev)
                j += 1
        
    def add_line(self,key):
        ev = self.univ.History[key].find_latest_visible(self.loc,None)
        self.watchedlines.append((key,ev))
        
    def get_visible(self):
        """returns a list of the latest visible events in all watched worldlines"""
        return [v[1] for v in self.watchedlines if v[1] is not None]