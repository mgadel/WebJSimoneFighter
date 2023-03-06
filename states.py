# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 10:37:48 2023

@author: Matth
"""

import pygame
from fighter import Fighter
from button import Button
#from config import *
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE,RED,YELLOW, ROUND_OVER_COOLDOWN
from game import Game
from pygame import mixer
import sys
import os


def load_img(img):
    img = pygame.image.load(f"data/image/{img}.png").convert_alpha()
    return img

def get_font(size):
    return pygame.font.Font("assets/fonts/font.ttf",size)
 

class BaseState():
    
    music_on = None
    game_mode = None

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.persist={}

        # l'ensemble des variables à faire remonter
        
             
    def startup(self):
        #self.persist = persistent
        pass
        
    def get_event(self,event):
        pass
    
    def update(self,dt,window):
        pass
    
    def draw (self,window):
        pass

    @staticmethod
    def draw_bkg(image,window):
        #resize the image to fit the window
        scaled_bkg = pygame.transform.scale(image,(SCREEN_WIDTH,SCREEN_HEIGHT))
        window.blit(scaled_bkg,(0,0))        
        


class Intro(BaseState):
    def __init__(self):
        super().__init__()
        self.intro_image= pygame.image.load("assets/images/background/background.jpg").convert_alpha()
        self.next_state = "MENU"
        self.time_active = 0
        self.load_images()
        self.bkg_animation_step = 0
        self.logo_animation_step= 0
        self.update_time_bkg = pygame.time.get_ticks()
        self.update_time_logo = pygame.time.get_ticks()


    def load_images(self):
            self.list_bkg = []
            for i, file in enumerate(os.listdir('assets/images/background/intro')):
                self.list_bkg.append(pygame.image.load('assets/images/background/intro/' + file).convert_alpha())

            LOGO_SIZE = 470
            LOGO_SCALE = 1.3
            self.list_logo = []
            logo_sprite = pygame.image.load('assets/images/icons/jsimonefighter.png').convert_alpha()
            for i in range(0,7):
                tmp_img = logo_sprite.subsurface(i*LOGO_SIZE, 0 , LOGO_SIZE,LOGO_SIZE)
                tmp_scaled_img = pygame.transform.scale(tmp_img,(LOGO_SIZE*LOGO_SCALE,LOGO_SIZE*LOGO_SCALE))
                self.list_logo.append(tmp_scaled_img)


    def get_event(self,event): 
        if event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()
            sys.exit()

    def update(self,dt,window):
        #print the screen for some time     
        self.time_active +=dt     
        if self.time_active >=5000:
            self.done = True

    def animate_background(self):
        if (pygame.time.get_ticks() - self.update_time_bkg ) > 150:
            self.update_time_bkg = pygame.time.get_ticks()
            if self.bkg_animation_step <  len (self.list_bkg)-1:
                self.bkg_animation_step += 1
            else:
                self.bkg_animation_step = 0

        if (pygame.time.get_ticks() - self.update_time_logo ) > 500:
            self.update_time_logo = pygame.time.get_ticks()
            if self.logo_animation_step <  len (self.list_logo)-1:
                self.logo_animation_step += 1
            else:
                self.logo_animation_step = len (self.list_logo)-1

            
    def draw (self, window):

        self.animate_background()
        self.draw_bkg(self.list_bkg[self.bkg_animation_step],window)
        window.blit(self.list_logo[self.logo_animation_step],(180,0)) 
        #scaled_bkg = pygame.transform.scale(self.intro_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
        #window.blit(scaled_bkg,(0,0)) 
        '''
        intro_text = get_font(100).render(str("JSIMONE"),True,"#b68f40")
        intro_text2 = get_font(100).render(str("FIGHTER"),True,"#b68f40")
        intro_rect = intro_text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/3))
        intro_rect2 = intro_text2.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT*2/3))
        window.blit(intro_text,intro_rect)
        window.blit(intro_text2,intro_rect2)
        '''




class Menu(BaseState):
    def __init__(self):
        super().__init__()
        #self.active_index=0
        #self.menu_image= pygame.image.load("assets/images/background/Background.png").convert_alpha()
        self.menu_image= pygame.image.load("assets/images/background/fondchooseyourfighter.png").convert_alpha()
        self.next_state = "MENU"
        #self.state_image=
        play_solo_button = Button(image=None,pos = (SCREEN_WIDTH/2,SCREEN_HEIGHT/6*2+10),text_input="PLAY SOLO",font=get_font(60),base_color="#ff3c00",hovering_color="White")
        play_multi_button = Button(image=None,pos = (SCREEN_WIDTH/2,SCREEN_HEIGHT/6*3),text_input="PLAY MULTIJOUEUR",font=get_font(60),base_color="#ff3c00",hovering_color="White")
        option_button = Button(image=None,pos = (SCREEN_WIDTH/2,SCREEN_HEIGHT*4/6),text_input="CONTROLS",font=get_font(60),base_color="#ff3c00",hovering_color="White")
        quit_button = Button(image=None,pos = (SCREEN_WIDTH/2,SCREEN_HEIGHT*5/6),text_input="QUIT",font=get_font(60),base_color="#ff3c00",hovering_color="White")
        self.buttons = [play_solo_button,play_multi_button,option_button,quit_button]

    def draw(self,window):
        self.draw_bkg(self.menu_image,window)
        menu_text = get_font(100).render("MAIN MENU",True,"#060ab2")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/6))
        window.blit(menu_text,menu_rect)

        for button_i in self.buttons:
            button_i.update(window)

    def get_event(self, event):      
        
        game_mode = None
        menu_mouse_pos = pygame.mouse.get_pos()
        
        for button_i in self.buttons:
            button_i.changeColor(menu_mouse_pos)
        
        if event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons[0].checkForInput(menu_mouse_pos):
                self.next_state = "SELECT CHARACTER 1"
                game_mode='solo'      
                self.done=True                 
            if self.buttons[1].checkForInput(menu_mouse_pos):
                self.next_state = "SELECT CHARACTER 1"
                game_mode='multi'        
                self.done=True              
            if self.buttons[2].checkForInput(menu_mouse_pos):
                self.next_state = "OPTIONS"
                self.done=True 
            if self.buttons[3].checkForInput(menu_mouse_pos):
                self.quit = True
                pygame.quit()
                sys.exit()

        return game_mode

    
class Select_character_1(BaseState):

    game_mode = 'solo'

    def __init__(self,game_default):
        super().__init__()
        self.player_character_dict=game_default['player_character_dict']
        self.select_bkg= pygame.image.load("assets/images/background/fondchooseyourfighter.png").convert_alpha()
        self.select_image= pygame.image.load("assets/images/icons/chooseyourfighter.png").convert_alpha()
        #self.state_image
        character_1 = Button(image=None,pos = (SCREEN_WIDTH/7,SCREEN_HEIGHT/9*7+20+10),text_input="FELINE FURY",font=get_font(15),base_color="#ff3c00",hovering_color="White")
        character_2 = Button(image=None,pos = (SCREEN_WIDTH*2/7-10,SCREEN_HEIGHT/9*7.5+20+10),text_input="GO-GO GADABOUT",font=get_font(15),base_color="#ff5f19",hovering_color="White")
        character_3 = Button(image=None,pos = (SCREEN_WIDTH*3/7+10,SCREEN_HEIGHT/9*8+20+10),text_input="MUSCLE QUEEN",font=get_font(15),base_color="#f8923F",hovering_color="White")
        character_4 = Button(image=None,pos = (SCREEN_WIDTH*4/7+40,SCREEN_HEIGHT/9*8+10),text_input="FROSTY",font=get_font(15),base_color="#f8923F",hovering_color="White")
        character_5 = Button(image=None,pos = (SCREEN_WIDTH*5/7+20,SCREEN_HEIGHT/9*7.5+20),text_input="PHANTOM",font=get_font(15),base_color="#ff5f19",hovering_color="White")
        character_6 = Button(image=None,pos = (SCREEN_WIDTH*6/7-10,SCREEN_HEIGHT/9*7+20),text_input="MIDNIHT STORM",font=get_font(15),base_color="#ff3c00",hovering_color="White")
        
        quit_button = Button(image=None,pos = (SCREEN_WIDTH/10*9+30,SCREEN_HEIGHT*9/10+40),text_input="BACK",font=get_font(15),base_color="#f8923F",hovering_color="White")
              
        self.buttons = [character_1,character_2,character_3,character_4,character_5,character_6,quit_button]

    def draw(self,window):    
        select_text = get_font(50).render("SELECT",True,"#060ab2")        
        select_text2 = get_font(50).render("PLAYER ONE",True,"#060ab2") 
        select_rect = select_text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/5-80+30))
        select_rect2 = select_text2.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/5+30))
        
        self.draw_bkg(self.select_bkg,window)
        self.draw_bkg(self.select_image,window)
        window.blit(select_text,select_rect)
        window.blit(select_text2,select_rect2)
        
        for button_i in self.buttons:
            button_i.update(window)
        
    
    def get_event(self,event):
   
        menu_mouse_pos = pygame.mouse.get_pos()
        
        for button_i in self.buttons:
            button_i.changeColor(menu_mouse_pos)     
        
        if event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_mode=='multi':
                if self.buttons[0].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 1      
                    self.next_state = "SELECT CHARACTER 2"
                    self.done=True 
                if self.buttons[1].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 2
                    self.next_state = "SELECT CHARACTER 2"
                    self.done=True 
                if self.buttons[2].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 3      
                    self.next_state = "SELECT CHARACTER 2"
                    self.done=True                  
                if self.buttons[3].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 4     
                    self.next_state = "SELECT CHARACTER 2"   
                    self.done=True                     
                if self.buttons[4].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 5      
                    self.next_state = "SELECT CHARACTER 2"
                    self.done=True                  
                if self.buttons[5].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 6     
                    self.next_state = "SELECT CHARACTER 2"   
                    self.done=True  

            elif self.game_mode=='solo':
                if self.buttons[0].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 1   
                    self.player_character_dict[2] = 3  
                    self.next_state = "PLAY"
                    self.done=True 
                if self.buttons[1].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 2
                    self.player_character_dict[2] = 5
                    self.next_state = "PLAY"
                    self.done=True 
                if self.buttons[2].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 3 
                    self.player_character_dict[2] = 4   
                    self.next_state = "PLAY"
                    self.done=True                  
                if self.buttons[3].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 4  
                    self.player_character_dict[2] = 1   
                    self.next_state = "PLAY"   
                    self.done=True                     
                if self.buttons[4].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 5 
                    self.player_character_dict[2] = 6    
                    self.next_state = "PLAY"
                    self.done=True                  
                if self.buttons[5].checkForInput(menu_mouse_pos):
                    self.player_character_dict[1] = 6  
                    self.player_character_dict[2] = 2  
                    self.next_state = "PLAY"   
                    self.done=True  

            if self.buttons[6].checkForInput(menu_mouse_pos):
                self.next_state = "MENU"
                self.done=True       
                       
                                               
                
class Select_character_2(BaseState):

    def __init__(self,game_default):
        super().__init__()
        self.select_bkg= pygame.image.load("assets/images/background/fondchooseyourfighter.png").convert_alpha()
        self.select_image= pygame.image.load("assets/images/icons/chooseyourfighter.png").convert_alpha()
        self.player_character_dict=game_default['player_character_dict']
        character_1 = Button(image=None,pos = (SCREEN_WIDTH/7,SCREEN_HEIGHT/9*7+20+10),text_input="FELINE FURY",font=get_font(15),base_color="#ff3c00",hovering_color="White")
        character_2 = Button(image=None,pos = (SCREEN_WIDTH*2/7-10,SCREEN_HEIGHT/9*7.5+20+10),text_input="GO-GO GADABOUT",font=get_font(15),base_color="#ff5f19",hovering_color="White")
        character_3 = Button(image=None,pos = (SCREEN_WIDTH*3/7+10,SCREEN_HEIGHT/9*8+20+10),text_input="MUSCLE QUEEN",font=get_font(15),base_color="#f8923F",hovering_color="White")
        character_4 = Button(image=None,pos = (SCREEN_WIDTH*4/7+40,SCREEN_HEIGHT/9*8+10),text_input="FROSTY",font=get_font(15),base_color="#f8923F",hovering_color="White")
        character_5 = Button(image=None,pos = (SCREEN_WIDTH*5/7+20,SCREEN_HEIGHT/9*7.5+20),text_input="PHANTOM",font=get_font(15),base_color="#ff5f19",hovering_color="White")
        character_6 = Button(image=None,pos = (SCREEN_WIDTH*6/7-10,SCREEN_HEIGHT/9*7+20),text_input="MIDNIHT STORM",font=get_font(15),base_color="#ff3c00",hovering_color="White")
        
        quit_button = Button(image=None,pos = (SCREEN_WIDTH/10*9+30,SCREEN_HEIGHT*9/10+40),text_input="BACK",font=get_font(15),base_color="#f8923F",hovering_color="White")
              
        self.buttons = [character_1,character_2,character_3,character_4,character_5,character_6,quit_button]

 
    def draw(self, window):  
        select_text = get_font(50).render("SELECT",True,"#060ab2")        
        select_text2 = get_font(50).render("PLAYER TWO",True,"#060ab2") 
        select_rect = select_text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/5-80+30))
        select_rect2 = select_text2.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/5+30))
        
        self.draw_bkg(self.select_bkg,window)
        self.draw_bkg(self.select_image,window)
        window.blit(select_text,select_rect)
        window.blit(select_text2,select_rect2)
 
        for button_i in self.buttons:
                button_i.update(window)

    def get_event(self,event):
        
        menu_mouse_pos = pygame.mouse.get_pos()

        for button_i in self.buttons:
            button_i.changeColor(menu_mouse_pos)
            
        if event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons[0].checkForInput(menu_mouse_pos):
                self.player_character_dict[2] = 1      
                self.next_state = "PLAY"  
                self.done=True
            if self.buttons[1].checkForInput(menu_mouse_pos):
                self.player_character_dict[2] = 2
                self.next_state = "PLAY"  
                self.done=True
            if self.buttons[2].checkForInput(menu_mouse_pos):
                self.player_character_dict[2] = 3      
                self.next_state = "PLAY"  
                self.done=True
            if self.buttons[3].checkForInput(menu_mouse_pos):
                self.player_character_dict[2] = 4     
                self.next_state = "PLAY"   
                self.done=True
            if self.buttons[4].checkForInput(menu_mouse_pos):
                self.player_character_dict[2] = 5      
                self.next_state = "PLAY"  
                self.done=True
            if self.buttons[5].checkForInput(menu_mouse_pos):
                self.player_character_dict[2] = 6     
                self.next_state = "PLAY"   
                self.done=True

            if self.buttons[6].checkForInput(menu_mouse_pos):
                self.next_state = "MENU"
                self.done=True   
  



class Options(BaseState):
    
    # on definit ici les variables de classe
    music_on = True

    def __init__(self,game_default):
        super().__init__()
        #self.state_image
        #self.menu_image = pygame.image.load("assets/images/background/Background.png").convert_alpha()
        self.menu_image= pygame.image.load("assets/images/background/fondchooseyourfighter.png").convert_alpha()
        
        self.back_button = Button(image=None,pos = (SCREEN_WIDTH/2,SCREEN_HEIGHT*9/10+40),text_input="BACK",font=get_font(15),base_color="#060ab2",hovering_color="White")
        
       
    def draw(self,window):         
        self.draw_bkg(self.menu_image,window)
        option_text = get_font(100).render("CONTROLS",True,"#060ab2")
        option_rect = option_text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/6)) 
        window.blit(option_text,option_rect)   
        #on verifie la valeur de la variable de classe
        font_size=20
        texte1 = get_font(font_size).render("JUMP -   P1: Z   /   P2 - UP (keypad)",True,"#ff3c00")
        texte2 = get_font(font_size).render("CROUCH -   P1: S   /   P2 - DOWN (keypad)",True,"#ff3c00")
        texte3 = get_font(font_size).render("LEFT -   P1: Q   /   P2 - LEFT (keypad)",True,"#ff3c00")
        texte4 = get_font(font_size).render("RIGHT -   P1: D   /   P2 - RIGHT (keypad)",True,"#ff3c00")
        texte5 = get_font(font_size).render("PUNCH -   P1: E   /   P2 - K        ",True,"#ff3c00")
        texte6 = get_font(font_size).render("KICK -   P1: R   /   P2 - L        ",True,"#ff3c00")
        texte7 = get_font(font_size).render("FIREBALL -   P1: T   /   P2 - M        ",True,"#ff3c00")
        
        divide = 11
        offset=40
        rect1 = texte1.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/divide*3+offset)) 
        rect2 = texte2.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/divide*4+offset)) 
        rect3 = texte3.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/divide*5+offset)) 
        rect4 = texte4.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/divide*6+offset)) 
        rect5 = texte5.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/divide*7+offset)) 
        rect6 = texte6.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/divide*8+offset)) 
        rect7 = texte7.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/divide*9+offset)) 

        for pair in [(texte1,rect1),(texte1,rect2),(texte3,rect3),(texte4,rect4),(texte5,rect5),(texte6,rect6),(texte7,rect7)]:
            window.blit(pair[0],pair[1])

        option_mouse_pos = pygame.mouse.get_pos()   
        self.back_button.changeColor(option_mouse_pos)
        self.back_button.update(window)
        

    def get_event(self, event):
       
        option_mouse_pos = pygame.mouse.get_pos()   
        # Definir les boutons de options
        if event.type == pygame.QUIT:
            self.done = True
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  
            if self.back_button.checkForInput(option_mouse_pos):
                self.next_state="MENU"
                self.done=True
 


"""
class Options(BaseState):
    
    # on definit ici les variables de classe
    music_on = True

    def __init__(self,game_default):
        super().__init__()
        #self.state_image
        #self.menu_image = pygame.image.load("assets/images/background/Background.png").convert_alpha()
        self.menu_image= pygame.image.load("assets/images/background/fondchooseyourfighter.png").convert_alpha()
        self.character_fx_dict = game_default['character_fx_dict']
        self.player_character_dict = game_default['player_character_dict']
        
        self.buttons=[]
        
        '''
        if self.music_on == True:
            option_button =Button(image=None,pos = (SCREEN_WIDTH/2,SCREEN_HEIGHT/5*3),text_input="SOUND ON",font=get_font(75),base_color="#ff3c00",hovering_color="White")
            print('a')
        elif self.music_on==False:
            option_button =Button(image=None,pos = (SCREEN_WIDTH/2,SCREEN_HEIGHT/5*3),text_input="SOUND OFF",font=get_font(75),base_color="Black",hovering_color="White")
            print('b')
        '''
        back_button = Button(image=None,pos = (SCREEN_WIDTH/2,SCREEN_HEIGHT/5*4),text_input="BACK",font=get_font(75),base_color="#ff3c00",hovering_color="White")
        option_button =Button(image=None,pos = (SCREEN_WIDTH/2,SCREEN_HEIGHT/5*3),text_input="SOUND ON",font=get_font(75),base_color="#ff3c00",hovering_color="White")

        self.buttons = [option_button,back_button]
        
       

    def draw(self,window):         
        
        option_text = get_font(100).render("OPTIONS",True,"#060ab2")
        option_rect = option_text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/5))    
        #on verifie la valeur de la variable de classe
        if self.music_on == True:
            self.buttons[0].base_color= "#ff3c00"
            self.buttons[0].changeText("SOU&    ND ON")
            #self.buttons[0].update(window)
        elif self.music_on==False:
            self.buttons[0].base_color= "Black"
            self.buttons[0].changeText("SOUND OFF")
            #self.buttons[0].update(window)
        
        option_mouse_pos = pygame.mouse.get_pos()   
        
        for button_i in self.buttons:
            button_i.changeColor(option_mouse_pos)

        self.draw_bkg(self.menu_image,window)
        window.blit(option_text,option_rect)

        self.buttons[0].update(window)
        self.buttons[1].update(window)
    
        print(self.music_on)
        # Definir les boutons de options      
      
        
    #on a besoin de mettre à jour la variable music_on lors de l'initialisation de la classe !     
        

    def get_event(self, event):
       
        option_mouse_pos = pygame.mouse.get_pos()   
        # Definir les boutons de options
        if event.type == pygame.QUIT:
            self.done = True
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  
            if self.buttons[0].checkForInput(option_mouse_pos):
                if self.music_on == True:
                    self.music_on=False
                    self.game_sound()
                    return False
                else :
                    self.music_on=True
                    self.game_sound()
                    return True
            if self.buttons[1].checkForInput(option_mouse_pos):
                self.next_state="MENU"
                self.done=True


    def game_sound(self):
        if self.music_on==True: #0 : sound on
            # load music and sounds        
            #mixer.music.set_volume(0.35)
            #mixer.music.play(-1,0.0,5000)
            #self.character_fx_dict[self.player_character_dict[1]].set_volume(0.5)
            #self.character_fx_dict[self.player_character_dict[2]].set_volume(0.5)    
            mixer.music.unpause() 
        elif self.music_on==False:
            mixer.music.pause()
            #self.character_fx_dict[self.player_character_dict[1]].set_volume(0)
            #self.character_fx_dict[self.player_character_dict[2]].set_volume(0)
"""
    
class Play(BaseState):

    game_mode = 'solo'

    def __init__(self,game_default):
        super().__init__()
    
        self.bkg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
        self.victory_image = pygame.image.load("assets/images/icons/winner.png").convert_alpha()    
        self.looser_image= pygame.image.load("assets/images/icons/looser.png").convert_alpha()    
        self.load_backgrounds()
        self.bkg_animation_step = 0
        self.counter_font = pygame.font.Font("assets/fonts/font.ttf",80)
        self.score_font= pygame.font.Font("assets/fonts/font.ttf",30)   
        self.update_time_bkg = pygame.time.get_ticks()

        self.counter_font = get_font(80)
        self.score_font=get_font(30)
        
        self.character_data_dict=game_default['character_data_dict']
        self.player_character_dict=game_default['player_character_dict']
        self.character_spritesheet_dict=game_default['character_spritesheet_dict']
        self.character_game_data_dict=game_default['character_game_data_dict']
        self.character_fx_dict=game_default['character_fx_dict']
        #self.game_mode=game_default['game_mode']
        self.round_over_time=0
        self.score = [0,0] #player scores [P1,P2]

        self.startup()
        
    def load_backgrounds(self):
        self.list_bkg = []
        for i, file in enumerate(os.listdir('assets/images/background/play2')):
            self.list_bkg.append(pygame.image.load('assets/images/background/play2/' + file).convert_alpha())

    def startup(self):    
        self.intro_count = 3
        self.round_over = False
        self.last_count_update = pygame.time.get_ticks()
        # reset everything
        self.fighter_1 = Fighter(1,(200,310),self.character_data_dict[self.player_character_dict[1]], self.character_spritesheet_dict[self.player_character_dict[1]],self.character_game_data_dict[self.player_character_dict[1]],self.character_fx_dict[self.player_character_dict[1]],self.game_mode)
        self.fighter_2 = Fighter(2,(700,310),self.character_data_dict[self.player_character_dict[2]], self.character_spritesheet_dict[self.player_character_dict[2]],self.character_game_data_dict[self.player_character_dict[2]],self.character_fx_dict[self.player_character_dict[2]],self.game_mode,True)

    
    def get_event(self,event):
        # event handler
        if event.type == pygame.KEYDOWN:
            exit_key=pygame.key.get_pressed()
            if exit_key[pygame.K_ESCAPE]:
                self.next_state = "MENU"
                self.score = [0,0]
                self.done=True             
        if event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()
            sys.exit()

    def animate_background(self):

        if (pygame.time.get_ticks() - self.update_time_bkg ) > 50:
            self.update_time_bkg = pygame.time.get_ticks()
            if self.bkg_animation_step <  len (self.list_bkg)-1:
                self.bkg_animation_step += 1
            else:
                self.bkg_animation_step = 0


    def draw(self,window):
    
        # draw  the gameplay
        self.animate_background()
        self.draw_bkg(self.list_bkg[self.bkg_animation_step],window)
        #self.draw_bkg(self.bkg_image,window)
        
        self.draw_text(window,"PUSH ESC TO GO BACK TO MENU", get_font(10),RED,20,SCREEN_HEIGHT-20)
        # show players stats
        self.draw_health_bar(window,self.fighter_1.health,20,20)
        self.draw_health_bar(window,self.fighter_2.health,580,20)
        self.draw_text(window,"P1: " +str(self.score[0]),self.score_font,RED,20,60)
        self.draw_text(window,"P2: " +str(self.score[1]),self.score_font,RED,580,60)
 
        # draw fighters
        self.fighter_1.draw(window)
        self.fighter_2.draw(window)
        
        # Draw fireballs
        for fighter in [self.fighter_1,self.fighter_2]:
            for fireball in fighter.fireballs_list:
                fireball.draw(window)
   
        if self.intro_count >0 :
        #display count timer
            self.draw_text(window,str(self.intro_count),self.counter_font,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/3)
       
        if self.round_over == True:
            #window.blit(self.victory_image,(360,150))
            if self.game_mode=='solo':
                if self.fighter_1.alive == True:
                    #self.draw_text(window,"YES QUUUEN !",self.counter_font,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                    self.draw_bkg(self.victory_image,window)
                elif self.fighter_2.alive == True:
                    #self.draw_text(window,"LOOOSER !",self.counter_font,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                    self.draw_bkg(self.looser_image,window)
            elif self.game_mode=='multi':
                if self.fighter_1.alive == False:
                    #self.draw_text(window,"P1 YOU'RE THE QUEEN",self.counter_font,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                    self.draw_bkg(self.victory_image,window)
                elif self.fighter_2.alive == False:
                    #self.draw_text(window,"P2, BEAUTIFUL HONEY !",self.counter_font,RED,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                    self.draw_bkg(self.victory_image,window)
           

    def update(self,dt,window):
           
        if self.intro_count <=0 : 
            self.fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT,self.fighter_2, self.round_over)
            self.fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT,self.fighter_1, self.round_over)
        else:        
            #update count timer
            if (pygame.time.get_ticks() - self.last_count_update) >=1000:
                self.intro_count -= 1
                self.last_count_update = pygame.time.get_ticks() 
            
        #update the image from animation list
        self.fighter_1.update()
        self.fighter_2.update()
         
        # check for player defeat
        if self.round_over == False:
            if self.fighter_1.alive == False:
                self.score[1] += 1
                self.round_over = True
                self.round_over_time = pygame.time.get_ticks()
            elif self.fighter_2.alive == False:
                self.score[0] += 1
                self.round_over = True
                self.round_over_time = pygame.time.get_ticks()
        else:
            # display victory image
            if (pygame.time.get_ticks() - self.round_over_time) > ROUND_OVER_COOLDOWN:
                self.startup()

        
    @staticmethod
    def draw_health_bar(window,health,x,y):
        #+draw yellow rectangle
        ratio = health / 100
        pygame.draw.rect(window,WHITE,(x-5,y-5,410,40))
        pygame.draw.rect(window,RED,(x,y,400,30))
        pygame.draw.rect(window,YELLOW,(x,y,400*ratio,30))


    @staticmethod
    def draw_text(window,text,font,text_col,x,y):
        #on affiche le font comme une image
        img = font.render(text,font,text_col)
        window.blit(img,(x,y))
        
        
        
 
        
        
        
        
        
        
        
        
        
        
        