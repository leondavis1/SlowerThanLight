# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 22:52:40 2017

@author: Cobi
"""
import matplotlib.pyplot as plt
from ThingClass import Thingy
from ViewingSensor import Sensor
from WorldlineClass import Worldline, Location, Event
        

            
        



myship = Thingy((0),(-4),0)
othership = Thingy((2),(4),0)





#####----ONE DIMENTIONAL TEST----####
#plt.close('all')
#plt.figure(); plt.ion(); plt.show()
#plt.xlabel("space"); plt.ylabel("time")
#for j in range(100):
#    plt.plot(myship.loc.x,myship.loc.t, "go")
#    
#    #draw some light-cones
#    x = othership.loc.x; t = othership.loc.t
#    if myship.loc.t%0.5 < 0.15:
##        x0 = 0; x2 = 2*x
##        y0 = t + (x-x0)/Worldline.Light; y2 = t + (x2-x)/Worldline.Light
##        plt.plot([x0,x,x2],[y0,t,y2],"-k")
#        
#        for event in myship.sensor.GetVisible():
#            plt.plot([event.loc.x],[myship.loc.t],"bo")
#    plt.plot(x,t, "ro")
#    
#    Thingy.increment(0.2)
#    myship.sensor.Observe()
#
##maneuver
#myship.Maneuver(-1*myship.v[0])
#
#for j in range(100):
#    plt.plot(myship.loc.x,myship.loc.t, "go")
#    
#    #draw some light-cones
#    x = othership.loc.x; t = othership.loc.t
#    if myship.loc.t%0.5 < 0.15:
##        x0 = 0; x2 = 2*x
##        y0 = t + (x-x0)/Worldline.Light; y2 = t + (x2-x)/Worldline.Light
##        plt.plot([x0,x,x2],[y0,t,y2],"-k")
#        
#        for event in myship.sensor.GetVisible():
#            plt.plot([event.loc.x],[myship.loc.t],"bo")
#    plt.plot(x,t, "ro")
#    
#    Thingy.increment(0.2)
#    myship.sensor.Observe()
#
##maneuver
#othership.Maneuver(-1*othership.v[0])
#
#for j in range(300):
#    plt.plot(myship.loc.x,myship.loc.t, "go")
#    
#    #draw some light-cones
#    x = othership.loc.x; t = othership.loc.t
#    if myship.loc.t%0.5 < 0.15:
##        x0 = 0; x2 = 2*x
##        y0 = t + (x-x0)/Worldline.Light; y2 = t + (x2-x)/Worldline.Light
##        plt.plot([x0,x,x2],[y0,t,y2],"-k")
#        
#        for event in myship.sensor.GetVisible():
#            plt.plot([event.loc.x],[myship.loc.t],"bo")
#    plt.plot(x,t, "ro")
#    
#    Thingy.increment(0.2)
#    myship.sensor.Observe()
