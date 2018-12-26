# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 22:52:40 2017

@author: Cobi
"""
import matplotlib.pyplot as plt
from ThingClass import Thingy
from ViewingSensor import Sensor
from UniverseClass import Universe        
from Graphics import ViewScreen

import time


def ship_controls(myship,keyspressed):
    if 'a' in keyspressed:
        myship.maneuver((-.01,0))
    if 'd' in keyspressed:
        myship.maneuver((0.01,0))
    if 'w' in keyspressed:
        myship.maneuver((0,-.01))
    if 's' in keyspressed:
        myship.maneuver((0,0.01))
    if "c" in keyspressed:
        myship.maneuver((-1*myship.v[0],-1*myship.v[1]))

#####----TWO DIMENTIONAL OPERATION----####
viewscreen = ViewScreen()
keeplooping = True
univ = Universe(lightspeed=1)
myship = Thingy((0,0),(0,0),0,univ)
othership = Thingy((100,100),(0,0),0,univ)

while keeplooping:
    startclock = time.perf_counter()
    univ.increment(dt=1)
    viewscreen.draw_viewer(univ,myship.sensor)
    letters = viewscreen.get_keys()
    ship_controls(myship,letters)
    if "Q" in letters:
        keeplooping = False
    while time.perf_counter() - startclock < 0.005: #5 ms, or 200FPS
        time.sleep(0.0005) #wait 1/2 ms
        
    #make the other ship dance around a bit
    shipclock = othership.loc.t%1000
    if 0<shipclock<30:
        othership.maneuver((.01,0))
    if 600<shipclock<630:
        othership.maneuver((-.01,0))
    if 500<shipclock<530:
        othership.maneuver((-.02,0))
    if 800<shipclock<830:
        othership.maneuver((.02,0))
    if 50<shipclock<60:
        othership.maneuver((0,.1))
    if 150<shipclock<160:
        othership.maneuver((0,-.1))
    if 300<shipclock<350:
        othership.maneuver((0,-.01))
    if 500<shipclock<550:
        othership.maneuver((0,.01))
    
viewscreen.close()



######----TWO DIMENTIONAL TEST----####
#viewscreen = ViewScreen()
#keeplooping = True
#univ = Universe(lightspeed=5)
#myship = Thingy((200,100),(-4,0),0,univ)
#othership = Thingy((200,100),(4,0),0,univ)
#
#def showtimesteps(steps,dt=1):
#    for j in range(steps):
#        startclock = time.perf_counter()
#        univ.increment(dt)
#        viewscreen.draw_viewer(univ,myship.sensor)
#        viewscreen.get_keys() #do nothing with the results
#        while time.perf_counter() - startclock < .005: #5 ms, or 200FPS
#            time.sleep(0.0005) #wait 1/2 ms
#
#showtimesteps(20,1)
#myship.maneuver((-1*myship.v[0],0))
#showtimesteps(10,1)
#othership.maneuver((-1*othership.v[0],0))
#showtimesteps(30,1)
#othership.maneuver((-4,0))
#showtimesteps(60,1)
#othership.destroy()
#showtimesteps(20,1)
#
#time.sleep(5)
#viewscreen.close()





#####----ONE DIMENTIONAL TEST----####
#univ = Universe(lightspeed=5)
#myship = Thingy((0),(-4),0,univ)
#othership = Thingy((2),(4),0,univ)
#plt.close('all')
#plt.figure(); plt.ion(); plt.show()
#plt.xlabel("space"); plt.ylabel("time")
#def plottimesteps(steps, dt=1):
#    for j in range(steps):
#        plt.plot(myship.loc.x,    myship.loc.t,    "go")
#        plt.plot(othership.loc.x, othership.loc.t, "r.")
#        for event in myship.sensor.get_visible():
#            plt.plot([event.loc.x],[myship.loc.t],"bo")
#        univ.increment(dt)
#        myship.sensor.observe()
#
#plottimesteps(20,1)
#myship.maneuver(-1*myship.v[0])
#plottimesteps(10,1)
#othership.maneuver(-1*othership.v[0])
#plottimesteps(30,1)
#othership.maneuver(-4)
#plottimesteps(60,1)
#othership.destroy()
#plottimesteps(20,1)