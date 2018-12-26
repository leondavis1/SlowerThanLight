# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 16:57:26 2018

@author: Cobi
"""
import numpy as np
from UniverseClass import Event,Location,Universe



        
class Worldline:
    """A list of Events in a single Universe describing a line through
    4-dimentional space-time"""
            
    def __init__(self,univ):
        self.eventlist = []  #ordered list of Events
        self.timestamps = {} #dictionary of timestamp, index_of_event pairs
        self.key = univ.add_worldline(self)
        self.univ = univ   ###-------------------------------------------------might just want lightspeed?
        
    def add_event(self,loc,descrip):
        if len(self.eventlist)>0:
            if loc.t > self.eventlist[-1].loc.t:  #adding in chronological order
                self.timestamps[loc.t] = len(self.eventlist)  #index of the new Event being added
                self.eventlist.append(Event(loc.duplicopy(),descrip))
            elif loc.t == self.eventlist[-1].loc.t:  #same time, so replace
                self.eventlist[-1] = Event(loc.duplicopy(),descrip)
            else:
                raise AssertionError #trying to add backwards in time!
        else:
            self.timestamps[loc.t] = len(self.eventlist)  #index of the new Event being added
            self.eventlist.append(Event(loc.duplicopy(),descrip))
    
#    def prune(self,shiptime):
#        """get rid of all events in this Worldline that are too far in the past
#        to be visible to a ship at time <shiptime>, even if that ship were
#        across the universe.  Do this only if eventlist and timestamps are
#        sufficiently large, so that we can remove a bunch at once"""
#        if len(self.eventlist) > 2000 or len(self.timestamps) > 2000:
#            cuttime = shiptime - (2 * self.univ.size / self.univ.lightspeed)
#            k = 0; 
#            while self.eventlist[k].loc.t < cuttime:
#                k+=1
#            self.eventlist = self.eventlist[k-1:]
#            for t in self.timestamps.keys():
#                if t < cuttime:
#                    del self.timestamps[t]
#                else:
#                    self.timestamps[t] -= (k-1) #compensate for eventlist index shift
            

    """Return the latest Event that a viewer at loc would see of the Events on
    the Worldline. If the viewer could not see any Event, return None. prev is
    the last Event that the viewer remembers seeing, of events on this
    Worldline (not necessarily the immediate previous Event on the line), or
    None if none is remembered.
    THIS FUNCTION IS AT THE HEART OF THE WHOLE PROGRAM WORKING PROPERLY!!!
    """
    def find_latest_visible(self,loc,prev=None):
        if prev is None: #we need to iterate through eventlist
            prev = self.eventlist[0] #oldest Event in Worldline
        if not prev.is_visible(loc, self.univ.lightspeed):
            return None #if can't see oldest, can't see any
        
        index = self.timestamps[prev.loc.t] #index to start searching Worldline
        
        while index+1 < len(self.eventlist):
            if not self.eventlist[index+1].is_visible(loc,self.univ.lightspeed):
                break #can see Event at index but not event at index+1
            index += 1
        else: #can see even latest in Worldline:
            return None #entire Worldline is now in the past
        return self.interpolate(index,loc)        
    
    def interpolate(self, index, viewloc):
        """Find where the lightcone of viewloc intersects the worldline joining
        the events prev and post.  Return an interpolated event at that
        intersection point, which is what viewloc would see as it watches the
        worldline.
        Using convention prev=1, post=2, veiwloc=v:
            parametrized worldline is x=(t-t1)*v_i+x1 for v_i=(x2-x1)/(t2-t1)
            find t where distance b/w x, viewloc is delta-t*c
        """
        prev = self.eventlist[index]
        post = self.eventlist[index+1]
        v_i = (post.loc.space() - prev.loc.space())/(post.loc.t - prev.loc.t)
        #quadratic formula components
        a = np.sum(v_i**2)-self.univ.lightspeed**2
        b = (2 * np.sum(v_i*(prev.loc.space() - prev.loc.t*v_i - viewloc.space())) +
                2 * viewloc.t * self.univ.lightspeed**2)
        c = (np.sum((prev.loc.space() - prev.loc.t*v_i - viewloc.space())**2) -
                 (viewloc.t * self.univ.lightspeed)**2)
        pos = (-1*b + np.sqrt(b**2 - 4*a*c))/(2*a)
        neg = (-1*b - np.sqrt(b**2 - 4*a*c))/(2*a)
        #use correct component for time, then use time to find spatial location        
        inter_t = (pos if prev.loc.t<=pos<=post.loc.t else neg)
        inter_x = list((inter_t-prev.loc.t)*v_i+prev.loc.space())
        while len(inter_x) < 3:
            inter_x.append(None) #fixing dimentionality        
        self.timestamps[inter_t] = index  #viewer might dictionary-lookup inter_t later
        
        return Event(Location(inter_t,inter_x[0],inter_x[1],inter_x[2]),prev.descrip)  #should really interpolate description too....
        
        
