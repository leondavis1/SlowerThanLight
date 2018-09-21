# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 18:04:53 2018

@author: Cobi
"""
from WorldlineClass import Worldline


class Sensor:
    def __init__(self, loc, ownkey):
        self.watchedlines = [] #Worldline id, Event (or None) pairs
        self.loc = loc
        for wline in Worldline.History:
            if wline.key != ownkey:
                ev = wline.FindLatestVisible(self.loc,None)
                self.watchedlines.append((wline.key,ev))
                
    def Observe(self):
        j = 0
        while j < len(self.watchedlines):
            wkey,prev = self.watchedlines[j]
            ev = Worldline.History[wkey].FindLatestVisible(self.loc,prev)
            if prev is not None and ev is None: #Worldline ended
                del self.watchlines[j]
            else:
                self.watchedlines[j] = (wkey,ev)
                j += 1
        
    def AddLine(self,key):
        ev = Worldline.History[key].FindLatestVisible(self.loc,None)
        self.watchedlines.append((key,ev))
        
    def GetVisible(self):
        return [v[1] for v in self.watchedlines if v[1] is not None]