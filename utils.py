# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 11:18:00 2022

@author: Matth
"""

import os
from PIL import Image

path_warrior = 'assets/images/warrior/sprites'
path_wizzard = 'assets/images/wizard/sprites'
path_js1 = 'assets/images/js1/sprites'
path_js2 = 'assets/images/js2/sprites'
path_js3 = 'assets/images/js3/sprites'
path_js4 = 'assets/images/js4/sprites'
path_js5 = 'assets/images/js5/sprites'
path_js6 = 'assets/images/js6/sprites'

##
# concatenate all images    
def concatenate(img1,img2):
    img_all = Image.new('RGBA',(max(img1.width,img2.width),(img1.height + img2.height)))
    img_all.paste(img1,(0,0))
    img_all.paste(img2,(0,img1.height))                  
    return img_all


# append all image on a same image
all_img_war = Image.new('RGBA',(0,0))
for i, file in enumerate(os.listdir(path_warrior)):
    all_img_war = concatenate(all_img_war, Image.open(path_warrior + '\\' + file))
# save the file
#all_img_war.save(path_warrior + r'\warrior.png')


all_img_wiz = Image.new('RGBA',(0,0))
for i, file in enumerate(os.listdir(path_wizzard)):
    all_img_wiz = concatenate(all_img_wiz, Image.open(path_wizzard + '\\' + file))
# save the file
#all_img_wiz.save(path_wizzard + r'\wizard.png')


all_img_js1 = Image.new('RGBA',(0,0))
for i, file in enumerate(os.listdir(path_js1)):
    all_img_js1 = concatenate(all_img_js1, Image.open(path_js1 + '/' + file))
# save the file
all_img_js1.save(path_js1 + '/js1.png')


all_img_js2 = Image.new('RGBA',(0,0))
for i, file in enumerate(os.listdir(path_js2)):
    all_img_js2 = concatenate(all_img_js2, Image.open(path_js2 + '/' + file))
# save the file
all_img_js2.save(path_js2 + '/js2.png')


all_img_js3 = Image.new('RGBA',(0,0))
for i, file in enumerate(os.listdir(path_js3)):
    all_img_js3 = concatenate(all_img_js3, Image.open(path_js3 + '/' + file))
# save the file
all_img_js3.save(path_js3 + '/js3.png')


all_img_js4 = Image.new('RGBA',(0,0))
for i, file in enumerate(os.listdir(path_js4)):
    all_img_js4 = concatenate(all_img_js4, Image.open(path_js4 + '/' + file))
# save the file
all_img_js4.save(path_js4 + '/js4.png')

all_img_js5 = Image.new('RGBA',(0,0))
for i, file in enumerate(os.listdir(path_js5)):
    all_img_js5 = concatenate(all_img_js5, Image.open(path_js5 + '/' + file))
# save the file
all_img_js5.save(path_js5 + '/js5.png')

all_img_js6= Image.new('RGBA',(0,0))
for i, file in enumerate(os.listdir(path_js6)):
    all_img_js6 = concatenate(all_img_js6, Image.open(path_js6 + '/' + file))
# save the file
all_img_js6.save(path_js6 + '/js6.png')