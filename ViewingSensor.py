# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 18:04:53 2018

@author: Cobi
"""
#from WorldlineClass import Worldline

class Sensor:
    """An eye floating at a location in space-time in a given Universe.  It
    watches all worldlines not corresponding to its exception-key (representing
    the Physical object the sensor is attached to), and keeps track of the
    latest event in each worldline visible from its location.
    """
    
    def __init__(self, loc, univ, ownkey=None):
        self.univ = univ
        self.watchedlines = [] #pairs: 1st is Worldline id, 2nd is latest Event or None
        self.loc = loc
        for wline in self.univ.History:
            if wline.key != ownkey:
                ev = wline.find_latest_visible(self.loc,None)
                self.watchedlines.append((wline.key,ev))
                
    def observe(self):
        """Update-er to find latest visible event in all lines being watched"""
        j = 0
        while j < len(self.watchedlines):
            linekey,prev = self.watchedlines[j]
            ev = self.univ.get_worldline(linekey).find_latest_visible(self.loc,prev)
            if prev is not None and ev is None: #Worldline ended
                del self.watchedlines[j]
            else:
                self.watchedlines[j] = (linekey,ev)
                j += 1
        
    def watch_new_line(self,linekey):
        ev = self.univ.get_worldline(linekey).find_latest_visible(self.loc,None)
        self.watchedlines.append((linekey,ev))
        
    def get_visible(self):
        """returns a list of the latest visible events in all watched worldlines"""
        return [v[1] for v in self.watchedlines if v[1] is not None]