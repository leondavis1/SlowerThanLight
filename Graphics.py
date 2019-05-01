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
        """
        Takes in a universe and a physical and displays onscreen the view from
        that physical.

        :param univ: UniverseClass.Universe
        :param viewer: SensorClass.Sensor
        """
        assert(viewer.loc.dim()==2)
        viewer.observe()
        self.screen.fill((0,0,0))

        if self.view_real:
            for thing in univ.Physicals.values():
                thing.draw(self.screen,color=(255,0,0),radius=3) #red is real AND CHEATING

        if viewer.key is not None:
            viewer_phys = univ.get_physical(viewer.key)
            viewer_phys.draw(self.screen, color=(0,255,0), radius=5)  #green is you

        for event in viewer.get_visible():
            event.get_image().draw(self.screen, color= (0,0,255), radius=5)  #blue is you seeing them

        pygame.display.flip()
        
    def get_keys(self):
        happenings = pygame.event.get(pygame.KEYDOWN)
        letters = [ev.unicode for ev in happenings]
        pygame.event.clear()
        if 'Q' in letters:  #hardcoded quit
            self.close()
        return letters
    

