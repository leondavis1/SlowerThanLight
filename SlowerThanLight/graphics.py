# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 21:21:32 2017

@author: Cobi
"""

import numpy as np
import pygame
#pygame.init()


class ViewScreen:
    """
    Handles interfacing with pygame's screen representation
    """
    def __init__(self, view_real=False,size=(640, 480)):
        """

        :param view_real: when True, displays 'real' locations of all objects
        :param size: Size of the window in pixels
        """
        pygame.display.init()
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.key.set_repeat(5,5)  #5 ms delay, 5 ms interval b/w KEYDOWN events
        self.screen = pygame.display.set_mode(size)  #type(screen) = pygame.Surface
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
            for thing in univ.Physicals:
                thing.draw(self.screen)  #red is real AND CHEATING

        if viewer.key is not None:
            viewer_phys = univ.get_physical(viewer.key)
            viewer_phys.draw(self.screen)  #green is you

        for event in viewer.get_visible():
            event.get_image().draw(self.screen)  #blue is you seeing them

        pygame.display.flip()
        
    def get_keys(self):
        happenings = pygame.event.get(pygame.KEYDOWN)
        letters = [ev.unicode for ev in happenings]
        pygame.event.clear()
        if 'Q' in letters:  #hardcoded quit
            self.close()
            return None
        return letters


