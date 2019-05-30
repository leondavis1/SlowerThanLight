# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 22:52:40 2017

@author: Cobi
"""
#import matplotlib.pyplot as plt
from universe import Universe
from graphics import ViewScreen
from physical import Physical
import argparse
import pygame.time
import numpy as np
import cProfile, pstats
from contextlib import contextmanager


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-profile',)
    return parser


@contextmanager
def profile(formatted_output=None):
    pf = cProfile.Profile()
    pf.enable()
    try:
        yield pf
    finally:
        pf.disable()
        with open(formatted_output, 'w') as out:
            ps = pstats.Stats(pf, stream=out)
            ps.sort_stats('tottime')
            ps.print_stats()

def ship_controls(myship,keyspressed):
    if 'a' in keyspressed:
        myship.boost((-.01,0))
    if 'd' in keyspressed:
        myship.boost((0.01,0))
    if 'w' in keyspressed:
        myship.boost((0,-.01))
    if 's' in keyspressed:
        myship.boost((0,0.01))
    if "c" in keyspressed:
        myship.boost((-1*myship.v[0],-1*myship.v[1]))


def main():
    try:
        #####----TWO DIMENTIONAL OPERATION----####
        viewscreen = ViewScreen(True)
        keeplooping = True
        univ = Universe(lightspeed=1)
        myship = Physical((0, 0), (0, 0), 0, univ)
        othership = Physical((100, 100), (0, 0), 0, univ, watches=False)
        scattered = []

        for i in range(10):
            p = Physical((i * 3, i * 3), (0, 0), 0, univ, watches=False)
            scattered.append(p)

        while keeplooping:
            n=0
            avg_time = 0
            t0 = pygame.time.get_ticks()
            univ.increment(dt=1)
            viewscreen.draw_visible(univ, myship.sensor)
            letters = viewscreen.get_keys()
            ship_controls(myship, letters)
            if "Q" in letters:
                keeplooping = False

            # make the other ship dance around a bit
            shipclock = othership.loc.t % 1000
            if 0 < shipclock < 30:
                othership.boost((.01, 0))
            if 600 < shipclock < 630:
                othership.boost((-.01, 0))
            if 500 < shipclock < 530:
                othership.boost((-.02, 0))
            if 800 < shipclock < 830:
                othership.boost((.02, 0))
            if 50 < shipclock < 60:
                othership.boost((0, .1))
            if 150 < shipclock < 160:
                othership.boost((0, -.1))
            if 300 < shipclock < 350:
                othership.boost((0, -.01))
            if 500 < shipclock < 550:
                othership.boost((0, .01))

            for s in scattered:
                dv = np.random.rand(2) - 0.5
                s.boost(0.1 * dv)
            t1 = pygame.time.get_ticks()
            avg_time = avg_time*n/(n+1) + (t1 - t0)/(n+1)

            if shipclock % 100 == 0:
                print("Average loop time: %f ms" % avg_time)
                print(len(othership.get_worldline().eventlist))
            if myship.loc.t // 1000 > 3:
                keeplooping = False
            pygame.time.wait(10-(t1-t0))


        viewscreen.close()

    except Exception as e:
        viewscreen.close()
        raise e


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()
    pf = cProfile.Profile()
    if args.profile:
        with profile(args.profile):
            main()

    else:
        main()


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
    #myship.boost((-1*myship.v[0],0))
    #showtimesteps(10,1)
    #othership.boost((-1*othership.v[0],0))
    #showtimesteps(30,1)
    #othership.boost((-4,0))
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
    #myship.boost(-1*myship.v[0])
    #plottimesteps(10,1)
    #othership.boost(-1*othership.v[0])
    #plottimesteps(30,1)
    #othership.boost(-4)
    #plottimesteps(60,1)
    #othership.destroy()
    #plottimesteps(20,1)