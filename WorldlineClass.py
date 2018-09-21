# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 16:57:26 2018

@author: Cobi
"""
import numpy as np


class Location:
    """a location in spacetime.
        Either: x in an array of length between 1 and 3,
            or: x,y,z are spatial coords (for dim<3, leave z and/or y as Nones"""
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
    def IsVisible(self,loc2,c=10):
        assert(self.loc.dim()==loc2.dim())
        spatial = self.loc.lengthto(loc2)
        return ((loc2.t - self.loc.t)*c >= spatial)

        
#    """The time when the light-cone of the Endpoint reaches the viewer"""
#    def t_seen(self,viewer,light):
#        #need separation AT MOMENT ENDPOINT WAS CREATED
#        x_o = viewer.x - (viewer.v * (viewer.t - self.t))
#        delta_x = x_o - self.x
#        a = np.sum(np.power(viewer.v,2)) - light**2
#        b = 2*np.sum(delta_x * viewer.v)
#        c = np.sum(np.power(delta_x,2))
#        #quadratic.  1 intersect is always back in time. Pick positive one.
#        #quadratic gives time AFTER endpoint was created when viewer sees. Want absolute
#        return self.t + (-1*b - np.sqrt(b**2 - 4*a*c))/(2*a)

        
class Worldline:
    
    Light = 5
    keycounter = 0
    History = [] #indexed so History[key] gets the corresponding Worldline
    
    def __init__(self):
        self.eventlist = []  #ordered list of Events
        self.timestamps = {} #dictionary of timestamp, Event-index pairs (easier than event, event-index)
        self.key = Worldline.keycounter
        Worldline.keycounter = (Worldline.keycounter+1)%10000 #limit of 10,000 distinct thingies
        #add self to History, at index self.key
        if Worldline.keycounter > len(Worldline.History):
            Worldline.History.append(self)
        else:
            Worldline.History[self.key] = self
        
    def AddEvent(self,loc,descrip):
        self.timestamps[loc.t] = len(self.eventlist)
        self.eventlist.append(Event(loc.duplicopy(),descrip))

    """Return the latest Event that a viewer at loc would see of the Events on
    the Worldline. If the viewer could not see any Event, return None. prev is
    the last Event that the viewer remembers seeing, of events on this
    Worldline (not necessarily the immediate previous Event on the line), or
    None if none is remembered."""
    def FindLatestVisible(self,loc,prev=None):
        if prev is None: #we need to iterate through eventlist
            prev = self.eventlist[0] #oldest Event in Worldline
        if not prev.IsVisible(loc, Worldline.Light):
            return None #if can't see oldest, can't see any
        index = self.timestamps[prev.loc.t] #index to start searching Worldline
        while index+1 < len(self.eventlist):
            if not self.eventlist[index+1].IsVisible(loc,Worldline.Light):
                break #can see Event at index but not event at index+1
            index += 1
        else: #can see even latest in Worldline:
            return None #entire Worldline is now in the past
        return self.Interpolate(self.eventlist[index], self.eventlist[index+1],loc)
    
    def Interpolate(self, prev, post, viewloc):
        return prev  ####----UNFINISHED, THIS SHOULD ALMOST CERTAINLY BE UPDATED----####
        
        
        
#        """<thing> should be at its start position and velocity"""
#        self.image = thing.image
#        self.start = Endpoint(thing.x,thing.t)
#        self.end = thing.id #end is either an Endpoint or a Thingy's id
#        self.key = Worldline.keycounter
#        Worldline.keycounter = (Worldline.keycounter+1)%10000 #limit of 10,000 worldlines
#        for v in viewerlist:
#            if thing != v:  #this check is needed for calls due to maneuvers
#                v.schedule_event(self.t_start(v),self.key)
#        Worldline.History[self.key] = self
#    def t_start(self,viewer):
#        return self.start.t_seen(viewer,Worldline.Light)
#    def t_end(self,viewer):
#        if type(self.end) is Endpoint:
#            return self.end.t_seen(viewer,Worldline.Light)
#        else: #it must be an id of a Thingy
#            thing = Thingy.Universe[self.end]
#            return Endpoint(thing.x,thing.t).t_seen(viewer,Worldline.Light)
#    def location_seen(self,viewer):
#        """Return the x-location pair where the viewer sees the image (or None
#        if the image is not visible to the viewer at the viewer's time)"""
#        x_s = self.start.x
#        x_e = (self.end.x if type(self.end) is Endpoint else Thingy.Universe[self.end].x)
#        t_s = self.t_start(viewer)
#        t_e = self.t_end(viewer)
#        t_v = viewer.t
#        if t_e == t_s: #edge case where worldline is just a single point
#            return x_s
#        return x_s + ((x_e-x_s)*(t_v-t_s)/(t_e-t_s))
#        #As an alternate method, could use v_seen = v_e*(c+v_v)/(c+v_e)
#        #v_e is emitter velocity, v_v is viewer velocity. 2D or 3D, though?
#    """If self.end is still a Thingy id, change it to an Endpoint at that place"""
#    def terminate(self):
#        if type(self.end) is not Endpoint: #then is still an id
#            thingy = Thingy.Universe[self.end]
#            self.end = Endpoint(thingy.x,thingy.t)