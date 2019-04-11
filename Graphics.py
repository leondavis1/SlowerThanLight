# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 21:21:32 2017

@author: Cobi
"""

import numpy as np
import pygame
#pygame.init()


class ViewScreen:
    def __init__(self, view_real=False):
        pygame.display.init()
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.key.set_repeat(5,5)  #5 ms delay, 5 ms interval b/w KEYDOWN events
        self.screen = pygame.display.set_mode((640, 400))  #type(screen) = pygame.Surface
        self.screen.fill((0,0,0))  #black
        self.view_real = view_real

    def close(self):
        self.screen = None
        pygame.display.quit()
        pygame.quit()

    def draw_visible(self,univ,viewer):
        """Takes in a universe and a sensor and displays onscreen the view from
        that sensor"""
        assert(viewer.loc.dim()==2)
        viewer.observe()
        self.screen.fill((0,0,0))

        if self.view_real:
            for thing in univ.Physicals.values():
                self.draw_circle((255,0,0),thing.loc,radius=3)  #red is real AND CHEATING

        self.draw_circle((0,255,0),viewer.loc,radius=5)  #green is you
        for event in viewer.get_visible():
            self.draw_circle((0,0,255),event.get_image().loc,radius=5)  #blue is you seeing them
        pygame.display.flip()
        
    def get_keys(self):
        happenings = pygame.event.get(pygame.KEYDOWN)
        letters = [ev.unicode for ev in happenings]
        pygame.event.clear()
        if 'Q' in letters:  #hardcoded quit
            self.close()
        return letters
    
    def draw_circle(self,color,loc,radius):
        x = int(np.round(loc.x))
        y = int(np.round(loc.y))
        pygame.draw.circle(self.screen,color,(x,y),radius,0)

