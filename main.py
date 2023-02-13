# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 16:13:21 2022

@author: Matth
"""

import pygame
from pygame import mixer
from config import SCREEN_WIDTH,SCREEN_HEIGHT
from game import Game
import asyncio
from states import Intro,Menu,Options,Select_character_1,Select_character_2,Play
from config import *

pygame.init()
mixer.init()
        
pygame.mixer.music.load('assets/audio/music.ogg')
pygame.mixer.music.set_volume(0.35)
pygame.mixer.music.play(-1,0.0,5000)
window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("JSimone Fighter")


game_default ={
    "character_fx_dict": {
            1:mixer.Sound("assets/audio/sword.ogg"),
            2:mixer.Sound("assets/audio/magic.ogg"),
            3:mixer.Sound("assets/audio/magic.ogg"),
            4:mixer.Sound("assets/audio/magic.ogg"),
            5:mixer.Sound("assets/audio/sword.ogg"),
            6:mixer.Sound("assets/audio/sword.ogg"),
            7:mixer.Sound("assets/audio/sword.ogg"),
            8:mixer.Sound("assets/audio/sword.ogg"),
            },
    "character_spritesheet_dict" : {
            6:(pygame.image.load("assets/images/js1/sprites/js1.png").convert_alpha(),JS1_ANIMATION_STEPS,pygame.image.load("assets/images/js1/boule.png").convert_alpha()),
            5:(pygame.image.load("assets/images/js2/sprites/js2.png").convert_alpha(),JS2_ANIMATION_STEPS,pygame.image.load("assets/images/js2/boule.png").convert_alpha()),
            4:(pygame.image.load("assets/images/js3/sprites/js3.png").convert_alpha(),JS3_ANIMATION_STEPS,pygame.image.load("assets/images/js3/boule.png").convert_alpha()),
            2:(pygame.image.load("assets/images/js4/sprites/js4.png").convert_alpha(),JS4_ANIMATION_STEPS,pygame.image.load("assets/images/js4/boule.png").convert_alpha()),
            1:(pygame.image.load("assets/images/js5/sprites/js5.png").convert_alpha(),JS5_ANIMATION_STEPS,pygame.image.load("assets/images/js5/boule.png").convert_alpha()),
            3:(pygame.image.load("assets/images/js6/sprites/js6.png").convert_alpha(),JS6_ANIMATION_STEPS,pygame.image.load("assets/images/js6/boule.png").convert_alpha()),
            7:(pygame.image.load("assets/images/warrior/sprites/warrior.png").convert_alpha(),WARRIOR_ANIMATION_STEPS),
            8:(pygame.image.load("assets/images/wizard/sprites/wizard.png").convert_alpha(),WIZARD_ANIMATION_STEPS),
            },
    "character_data_dict": {
            1:JS_DATA,
            2:JS_DATA,
            3:JS_DATA,
            4:JS_DATA,
            5:JS_DATA,
            6:JS_DATA,
            7:WARRIOR_DATA,
            8:WIZARD_DATA,
            },
    "character_game_data_dict": {
            1:JS_GAME_DATA,
            2:JS_GAME_DATA,
            3:JS_GAME_DATA,
            4:JS_GAME_DATA,
            5:JS_GAME_DATA,
            6:JS_GAME_DATA,
            7:WARRIOR_GAME_DATA,
            8:WIZARD_GAME_DATA,
            },
        "music_on" : True,
        "game_mode" : "solo",
        "player_character_dict" : {1:1,2:2}
}


states = {
    "INTRO":Intro(),
    "MENU":Menu(),
    "OPTIONS":Options(game_default),
    "PLAY":Play(game_default),
    "SELECT CHARACTER 1":Select_character_1(game_default),
    "SELECT CHARACTER 2":Select_character_2(game_default)
    }


game = Game(window,states,"INTRO")
asyncio.run(game.run())
#game.main_menu()


'''
if __name__ =='__main__':
     game = Game(window,states,"INTRO")
     asyncio.run(game.run())
'''
     
