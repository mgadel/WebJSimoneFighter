# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 12:35:48 2023

@author: Matth
"""

import pygame
from pygame import mixer
import sys
import asyncio
from config import FPS


class Game():

    def __init__(self,window,states,start_state):
     
        self.done=False
        self.screen = window
        self.clock = pygame.time.Clock()   
        self.game_mode = 'multi'
        
        # le dictionnaire de toute les classes STATES
        self.states = states
        # le nom de l'état dans lequel on se trouve
        self.state_name = start_state
        # L'instance de classe de l'état dans lequel on se trouve
        self.state = self.states[self.state_name]
       

    def event_loop(self):
        # pour l état dans lequel on est, on prend en compte l'action de l'utilisateur
        for event in pygame.event.get():
            #print('a' + str(event))
            _ = self.state.get_event(event)

            if _ is not None and self.state_name == 'MENU':
                self.game_mode = self.state.get_event(event)
                setattr(self.states['PLAY'],'game_mode',self.game_mode)
                setattr(self.states['SELECT CHARACTER 1'],'game_mode',self.game_mode)
            
            if _ is not None and self.state_name == 'OPTION':
                self.music_on = self.state.get_event(event)
                setattr(self.state,'music_on',self.music_on)
                

    def flip_state(self):
        # tampon des cha
        # ngements d'états en attent la fin de la boucle
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup()
                   

    def update(self,dt):
        if self.state.quit:
            self.done = True      
        elif self.state.done:
            self.flip_state()

        self.state.update(dt,self.screen)

    def draw(self):
        self.state.draw(self.screen)

    #gestion asynchrone des evenements
    async def run(self):
        while not self.done:
            dt = self.clock.tick(FPS)
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()
            await asyncio.sleep(0)
        
        pygame.quit()
        sys.exit()


    @staticmethod
    def get_font(size):
        return pygame.font.Font("assets/fonts/font.ttf",size)
     
        
    
  