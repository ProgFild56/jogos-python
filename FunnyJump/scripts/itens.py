from body_abstract import BodyAbstract
import pygame
from pygame.locals import *
from variables import *

class Item(BodyAbstract):
    #type_item => 'life', 'bronze-coin', 'silver-coin' or 'gold-coin'...
    def __init__(self,dir_sprites,type_item,position):
     
        super().__init__(type_item,position)
     
        if type_item == 'life':
            self.sprite = pygame.image.load(dir_sprites['life']).convert_alpha()
            self.attributes.update({'score_increase':0,'life_increase':1})
        elif type_item == 'bronze-coin':
            self.sprite = pygame.image.load(dir_sprites['bronze_coin']).convert_alpha()
            self.attributes.update({'score_increase':50,'life_increase':0})
        elif type_item == 'silver-coin':
            self.sprite = pygame.image.load(dir_sprites['silver_coin']).convert_alpha()
            self.attributes.update({'score_increase':100,'life_increase':1})
        elif type_item == 'gold-coin':
            self.sprite = pygame.image.load(dir_sprites['gold_coin']).convert_alpha()
            self.attributes.update({'score_increase':500,'life_increase':1})
        else:
            print("error: type of Item not defined!")
            exit()