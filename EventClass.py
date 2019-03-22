# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 14:54:39 2019

@author: Cobi
"""
from LocationClass import Location

class Event(Location):
    """A location in space-time and the type and parameters of the Physical object
    which was there at that time.  The parameters are not themselves a Physical,
    just some sort of compressed description that can be later expanded and
    used to see what had happened at this Event.
    """
    
    def __init__(self,loc,phystype,descrip):
        super().__init__(loc.t,loc.x,y=loc.y,z=loc.z)
        self.descrip = descrip
        self.phystype = phystype
    
    def is_visible(self,loc2,c=10):
        """given a viewing space-time location, return the boolean 'light has had
            time to travel from the Event to the viewer'"""
        assert(self.dim()==loc2.dim())
        spatial = self.length_to(loc2)
        return ((loc2.t - self.t)*c >= spatial)
    
    def get_image(self):
        """Return an instance of the correct subtype of Physical which matches
        the description of this event. That Physical is a 'ghost': not
        registered with the Universe and has no Worldline"""
        return self.phystype.decompress(self.descrip)
    