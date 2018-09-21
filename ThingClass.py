# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 16:56:19 2018

@author: Cobi
"""
import numpy as np
from ViewingSensor import Sensor
from WorldlineClass import Worldline, Location, Event

class Thingy:
    """Physical objects that live in the Universe.  Each have a distinct id, a
    current Worldline, and some physical image.  They keep track of all
    Worldlines that they might one day see, using the Worldine id "key"s, and
    when they will first see that worldline if no maneuvers occur
    Fields:   x   v   t   id   image   events   visible   linekey """
        
    Universe = {}
    keycounter = 0
      
    def increment(dt=1):
        for thing in Thingy.Universe.values():
            thing.Drift(dt)
            
    
    def __init__(self,x,v,t):
        self.loc = Location(t,x)
        if self.loc.dim()==1:
            v = [v]
        self.v = np.array(v)
        assert(len(self.v) == self.loc.dim())
        self.theta = 0
        self.omega = 0
        worldline = Worldline() #build new Worldline (it adds itself to to History)
        worldline.AddEvent(self.loc,self.Compress())
        self.worldkey = worldline.key
        self.sensor = Sensor(self.loc, self.worldkey)
        #inform rest of Universe about the new Worldline
        for tkey, thing in Thingy.Universe.items():
            thing.sensor.AddLine(self.worldkey)
        #add self to universe
        self.key = Thingy.keycounter
        Thingy.keycounter = (Thingy.keycounter+1)%10000 #limit of 10,000 distinct Thingys
        Thingy.Universe[self.key] = self
        
    def Maneuver(self,dv):
        if self.loc.dim() ==1:
            dv = [dv]
        dv = np.array(dv)
        self.v = self.v + dv
    
    def Drift(self, dt=1):
        #update location
        self.loc.t += dt
        d = len(self.v)
        self.loc.x += self.v[0]*dt
        if d>=2: self.loc.y = self.v[1]*dt
        if d>=3: self.loc.z = self.v[2]*dt
        self.theta += self.omega*dt #update angle
        Worldline.History[self.worldkey].AddEvent(self.loc,self.Compress())
        self.sensor.loc = self.loc #update the sensor so it knows where Thingy is
    
    def Compress(self):
        return "placeholderstring"
    
    
#    ####----OLD STUFF THAT NEEDS RETHINKING MAYBE----####
#    def schedule_event(self,time,eventkey):
#        self.events.put_nowait((time,eventkey))
#    def current_line(self):
#        return Worldline.History[self.linekey]
#    def all_visible(self):
#        while not self.events.empty():
#            t,k = self.events.queue[0] #peek at first, doesn't dequeue
#            if t<=self.t: #worldline has started being visible. Dequeue.
#                self.visible += [k]
#                self.events.get_nowait()
#            else:
#                break #queue is sorted
#        j = 0
#        while j < len(self.visible):
#            #remove any worldines where you are past their end
#            if self.t > Worldline.History[self.visible[j]].t_end(self):
#                del self.visible[j]
#            else:
#                j += 1
#        return self.visible
#    """change velocity, start new Worldline, recalculate time-till-see-events"""
#    def maneuver(self,dv):
#        assert(type(dv) == np.ndarray)
#        self.v = self.v + dv
#        self.current_line().terminate() #cap previous worldline
#        self.linekey = Worldline(self,Thingy.Universe.values()).key #new line
#        #visible things remain visible, but time-till-visible changes for queue
#        newqueue = PriorityQueue()
#        while not self.events.empty(): #empty out the old events queue
#            key = self.events.get_nowait()[1] #want only event key, not time
#            line = Worldline.History[key]
#            newqueue.put_nowait((line.t_start(self),key))
#        self.events = newqueue
#    """change position, start new Worldline, recalculate time-till-see-events"""     
#    def hyperjump(self,newpos):
#        assert(type(newpos) == np.ndarray)
#        self.current_line().terminate() #cap previous worldline
#        self.x = newpos #jump
#        self.linekey = Worldline(self,Thingy.Universe.values()).key #new line
#        #need to recheck queue AND visible
#        newqueue = PriorityQueue()
#        while not self.events.empty(): #empty out the old events queue
#            key = self.events.get_nowait()[1] #want only event key, not time
#            line = Worldline.History[key]
#            newqueue.put_nowait((line.t_start(self),key))
#        for key in self.visible:
#            line = Worldline.History[key]
#            newqueue.put_nowait((line.t_start(self),key))
#        self.events = newqueue
#        self.visible = []
#        self.all_visible() #go through queue, see what we can see