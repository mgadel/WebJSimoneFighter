# -*- codi ng: utf-8 -*-:
"""
Created on Thu Dec 29 17:03:32 2022

@author: Matth
"""

import pygame
import random


class Fireball():
    def __init__(self,player,sprite,center_x,center_y,flip):
        self.player = player
        self.rect = pygame.Rect((center_x+40,center_y,20,20))
        self.fireball_speed = 10
        self.fireball_strength = 5
        self.flip=flip
        self.sprite = sprite
        self.image= self.load_image()


    def load_image(self):
        SIZE=470
        SCALE=1
        tmp_img = self.sprite.subsurface(0, 0 , SIZE, SIZE)
        scaled_fire_img = pygame.transform.scale(tmp_img,(SIZE*SCALE,SIZE*SCALE))
        return scaled_fire_img

    def move(self):
        if self.flip == False:
            dx = self.fireball_speed
        elif self.flip == True:
            dx = -self.fireball_speed   
        self.rect.x = self.rect.x + dx  


    def wound(self,target):
        if self.rect.colliderect(target.rect):
            target.health -= self.fireball_strength
            target.hit =True
            return True 
        return False    
        
        
    def update(self):
        # étant donné l'état dans lequel on se trouve, on déoule la liste des animation d'u nmeme état
        animation_cooldown = 50
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            #et on reset le timer 
            self.update_time= pygame.time.get_ticks()

        # check if the animation has finished reset to first frame
        if self.frame_index >= len(self.animation_list[self.action]):
            #check if the player is dead, then end animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #♣ check if an attack was executed 
                if self.action == 4 or self.action ==3:
                    self.attacking = False
                    # set a cooldown for the attack
                    self.attack_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    # if the player was in the middle of an attack, then it cancel the ongoing attack
                    self.attacking = False
                    self.attack_cooldown = 20
        
        
    def draw(self,surface):
        OFFSET =[180,250]
        #pygame.draw.rect(surface,(255,0,0),self.rect)
        #change de coté l'image de la boule de feu
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img,(self.rect.x - OFFSET[0] ,self.rect.y - OFFSET[1]))
        

class Fighter():
    def __init__(self, player, x_y,display_data, sprite,game_data,sound,game_mode,flip = False):
        #create a rectangle object on the screen for the character
        # rect est un object pygame avec des proprietes
        self.player = player
        self.size = display_data[0]
        self.image_scale = display_data[1]
        self.offset = display_data[2]
        
        self.sprite_sheet= sprite[0]
        self.animation_steps=sprite[1] 
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps)
        self.fire_sprite=sprite[2]
        self.flip=flip
        self.rect = pygame.Rect((x_y[0],x_y[1],80,180))
        
        self.health = int(game_data[0])
        self.speed = int(game_data[1])
        self.strength =int(game_data[2])
        self.attack_sound=sound
        self.vel_y =0
        
        self.running = False
        self.hit = False
        self.hit_cooldown=0
        self.hit_recule = 10
        self.jump = False
        self.alive = True
        self.attack_type = 0
        self.attacking = False
        self.attack_cooldown=0
        self.crunch = False
        
        # freeze the player when hit or attacked
        self.freeze_hit = False
        #measure the running time of the game
        self.update_time = pygame.time.get_ticks()       
        # need to explain what the player is currently doing
        # 0: nth, 1: run, 2:jump, 3:poing, 4:pied, 5:hit, 6:death, 7:crunch, 8:fireball:
        self.action =0
        # the image currently displayed on the screen
        self.frame_index=0
        #selectionne l'image courrante dans la liste des animations
        self.image = self.animation_list[self.action][self.frame_index]
        self.game_mode = game_mode
        
        self.reflexion=50
        self.run_not_think=False
        
        self.fireball_cooldown=0
        self.fireballs_list=[]
        
        self.attack_button_pressed = False
      
    
    def update_action(self,new_action):
        # check if the new action is diffrent from the previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settint to handle different number of frame
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def load_images(self, sprite_sheet, animation_steps):
        # extract image 
        animation_list=[]
        
        for i, animation in enumerate(animation_steps):
            tmp_img_list=[]
            for a in range(animation):
                #print(sprite_sheet.get_width())
                #print(sprite_sheet.get_height())
                tmp_img = sprite_sheet.subsurface(a*self.size, i*self.size , self.size, self.size)
                tmp_scaled_img = pygame.transform.scale(tmp_img,(self.size*self.image_scale,self.size*self.image_scale))
                tmp_img_list.append(tmp_scaled_img)
            animation_list.append(tmp_img_list)
            
        return animation_list


        
    def attack_punch(self,target):
        # check if oponent are close enough to be hit
        # create an attack rectangle. If there is collision then HIT !
        #decide that we attach 2 tuimes the size of the personage
        
        # on s'assure que il y a un temps suffisant entre 2 attacks
        if self.attack_cooldown ==0: 
            self.attacking = True
            self.attack_sound.play()

            attacking_rect = pygame.Rect(self.rect.centerx - (2*self.rect.width)*self.flip , self.rect.y-self.rect.height*2/3, 2*self.rect.width, self.rect.height) 
            #si l'attaque touche l'ennemis
            if attacking_rect.colliderect(target.rect):
                target.health -= self.strength
                target.hit =True     
            #pygame.draw.rect(surface,(0,255,0),attacking_rect)
            
            
    def attack_kick(self,target):
        # check if oponent are close enough to be hit
        # create an attack rectangle. If there is collision then HIT !
        #decide that we attach 2 tuimes the size of the personage 
        # on s'assure que il y a un temps suffisant entre 2 attacks
        if self.attack_cooldown ==0: 
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2*self.rect.width)*self.flip , self.rect.y+self.rect.height*2/3, 2*self.rect.width, self.rect.height*1/3) 
            #si l'attaque touche l'ennemi
            if attacking_rect.colliderect(target.rect):
                target.health -= self.strength
                target.hit =True
            #pygame.draw.rect(surface,(0,255,0),attacking_rect)
            
            
    def attack_fireball(self,target):
        # check if oponent are close enough to be hit
        # create an attack rectangle. If there is collision then HIT !
        #decide that we attach 2 tuimes the size of the personage
        
        # on s'assure que il y a un temps suffisant entre 2 attacks
        if self.fireball_cooldown ==0: 
            self.attacking = True
            self.attack_sound.play()
            fireball=Fireball(self.player,self.fire_sprite,self.rect.centerx,self.rect.centery,self.flip)
            
            #si l'attaque ne touche pas l'ennemi on les garde en jeu
            if fireball.wound(target) == False:
                self.fireballs_list.append(fireball)
                
            #pygame.draw.rect(surface,(0,255,0),fireball.rect)



    def update (self):
        # check l'état du joueur
        if self.health <= 0:
            self.health =0
            self.alive=False
            self.update_action(6)
        elif self.hit == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type==1:
                self.update_action(3)
            elif self.attack_type==2:
                self.update_action(4)
            elif self.attack_type==3:
                # a mettre a jour on a pas de image
                self.update_action(8)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        elif self.crunch == True:
            # Pour l'instant on a pas l'image du CRUNCH mais on va le faire sur le rectangle vert
            self.update_action(7)
        else:
            self.update_action(0) 
        
        # étant donné l'état dans lequel on se trouve, on déoule la liste des animation d'u nmeme état
        animation_cooldown = 120
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check,if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            #et on reset le timer 
            self.update_time= pygame.time.get_ticks()
            
        # check if the animation has finished reset to first frame
        if self.frame_index >= len(self.animation_list[self.action]):
            #check if the player is dead, then end animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            
            else:
                self.frame_index = 0
                #♣ check if an attack was executed 
                if self.action == 4 or self.action ==3 or self.action ==8:
                    self.attacking = False
                    # set a cooldown for the attack
                    self.attack_cooldown = 20
                    self.fireball_cooldown =25
                
                if self.action == 5:
                    #player got hit
                    self.hit = False
                    self.hit_cooldown = 15
                    #self.freeze_hit=True
                    # if the player was in the middle of an attack, then it cancel the ongoing attack
                    self.attacking = False
                    # on rajoute un cooldown pour qu'il ne puisse pas attaquer
                    self.attack_cooldown = 20
                    self.fireball_cooldown = 25

        
    def decision(self,target):
        
        action_space = [0,1,2,3,4,5,6]
        
        decision_to_action = {
            0: "stand",
            1: "left",
            2: "right",
            3: "jump",
            4: "crouch",
            5: "punch",
            6: "kick",
            7: "fireball"
        }
        
        reach_pixel = 50
        if self.run_not_think == True :
            if (target.rect.centerx - self.rect.centerx ) < reach_pixel:
                policy=1
            elif (target.rect.centerx - self.rect.centerx ) > reach_pixel:
                policy=2
            elif abs(target.rect.centerx - self.rect.centerx ) <= reach_pixel:
                self.run_not_think= False
                policy=random.choice(action_space[3:])

        elif self.run_not_think== False :
            if self.reflexion > 0 :
                self.reflexion -= 10
                policy =0
                
            elif self.reflexion <= 0:
                self.reflexion = 300
                
                if (target.rect.centerx - self.rect.centerx ) < reach_pixel:
                    policy=1
                    self.run_not_think = True
                elif (target.rect.centerx - self.rect.centerx ) > reach_pixel:
                    policy=2
                    self.run_not_think = True
                # le rectangle fait 80x180
                elif target.jump==True:
                    policy=5
                elif target.crunch ==True:
                    policy=6
                else:
                    policy = random.choice(action_space[3:])
        
        return decision_to_action[policy]

        

    def move(self,screen_width,screen_height,target,round_over):
        #•size of the move
        speed = self.speed
        GRAVITY = 2
        dx=0
        dy=0
        self.running = False
        self.attack_type = 0
        self.crunch = False
        # taille définie pour le rectangle
        self.rect.height = 180
        key=pygame.key.get_pressed()
        events = pygame.event.get(pygame.KEYDOWN)

        # Can only perform other action when not currently attacking !
        if self.attacking == False and self.alive == True and round_over == False and self.freeze_hit==False:
            #check player 1
            if self.player == 1:
                # run movement
                if key[pygame.K_d]:
                    dx = speed
                    self.running = True
                if key[pygame.K_q]:
                    dx = -speed
                    self.running = True        
                # JUMP
                if key[pygame.K_z] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True                 
                # CRUNCH
                if key[pygame.K_s]:
                    self.rect.height = 180 / 2
                    self.crunch = True
                # ATTACK
                if key[pygame.K_e]:
                    self.attack_punch(target)
                    # determine which attack type was used
                    self.attack_type = 1
                if  key[pygame.K_r]:
                    self.attack_kick(target)
                    self.attack_type = 2                   
                if  key[pygame.K_t]:
                    self.attack_fireball(target)
                    self.attack_type = 3
            
                        # ATTACK
                """
                for event in events:
                    if event.key==pygame.K_r:
                        self.attack_punch(target)
                        # determine which attack type was used
                        self.attack_type = 1
                        print('hit') 
                    if  event.key==pygame.K_t:
                        self.attack_kick(target)
                        self.attack_type = 2                   
                    if  event.key==pygame.K_e:
                        self.attack_fireball(target)
                        self.attack_type = 3
                """
            
            #check player 2
            if self.player == 2:
                if self.game_mode == 'multi':
                    # run movement
                    if key[pygame.K_RIGHT]:
                        dx = speed
                        self.running = True
                    if key[pygame.K_LEFT]:
                        dx = -speed
                        self.running = True        
                    # JUMP
                    if key[pygame.K_UP] and self.jump == False:
                        self.vel_y = -30
                        self.jump = True
                    # CRUNCH
                    if key[pygame.K_DOWN]:
                        self.rect.height = 180 / 2
                        self.crunch = True
                    
                    if key[pygame.K_k]:
                        self.attack_punch(target)
                        # determine which attack type was used
                        self.attack_type = 1
                    if  key[pygame.K_l]:
                        self.attack_kick(target)
                        self.attack_type = 2                        
                    if  key[pygame.K_m]:
                        self.attack_fireball(target)
                        self.attack_type = 3
                
                    """;:
                    for event in pygame.event.get(pygame.KEYDOWN):
                        # ATTACK
                        if event.key==pygame.K_KP1:
                            self.attack_punch(target)
                            # determine which attack type was used
                            self.attack_type = 1
                        if  event.key==pygame.K_KP2:
                            self.attack_kick(target)
                            self.attack_type = 2                        
                        if  event.key==pygame.K_KP3:
                            self.attack_fireball(target)
                            self.attack_type = 3
                    """
                                
                if self.game_mode == 'solo':
                    
                    decision = self.decision(target)
                    # run movement
                    if decision=='right':
                        dx = speed
                        self.running = True
                    elif decision=='left':
                        dx = -speed
                        self.running = True        
                    # JUMP
                    elif decision=='jump' and self.jump == False:
                        self.vel_y = -30
                        self.jump = True
                    # CRUNCH
                    elif decision=='crouch':
                        self.rect.height = 180 / 2
                        self.crunch = True
                    # ATTACK
                    elif decision=='punch':     
                        self.attack_punch(target)
                        # determine which attack type was used
                        self.attack_type = 1
                    elif decision=='kick':  
                        self.attack_kick(target)
                        self.attack_type = 2
                    elif decision=='fireball':  
                        self.attack_fireball(target)
                        self.attack_type = 3            
                
        # apply GRAVITY 
        self.vel_y += GRAVITY
        dy += self.vel_y           
            
        # apply attack cooldown
        if self.attack_cooldown > 0 :
            self.attack_cooldown -= 1

        if self.fireball_cooldown > 0 :
            self.fireball_cooldown -= 1

        # recule si tu es HIT
        if self.hit_cooldown > 0 :
            self.freeze_hit= True
            self.hit_cooldown -= 1 
            if self.flip == False:
                dx -= 10
            elif self.flip == True:
                dx += 10
        else: 
            self.freeze_hit = False
            
        # keep the players on the screen
        if self.rect.left + dx < 0:
            dx = self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right 
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom
              
        # ensure players are facing
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # update plaver position
        self.rect.x = self.rect.x + dx
        self.rect.y += dy
        
        # Update fireball positions
        if len(self.fireballs_list) != 0:
            tmp = []
            for fireball in self.fireballs_list:
                fireball.move()
                if fireball.wound(target) == False:
                    tmp.append(fireball)
            self.fireballs_list = tmp
                    
        
    def draw(self,surface):
        #pygame.draw.rect(surface,(255,0,0),self.rect)
        img = pygame.transform.flip(self.image, self.flip, False)
        if self.crunch==True:
            surface.blit(img,(self.rect.x -(self.offset[0] * self.image_scale),self.rect.y- 90 - (self.offset[1] * self.image_scale)))
        else:
            surface.blit(img,(self.rect.x -(self.offset[0] * self.image_scale),self.rect.y - (self.offset[1] * self.image_scale)))
        
    
    