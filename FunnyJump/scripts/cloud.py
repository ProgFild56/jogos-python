from body_abstract import BodyAbstract
import pygame
from pygame.locals import *
from variables import *

class Cloud(BodyAbstract):    
    def __init__(self,dir_sprites,type_item,position):
        super().__init__(type_item,position)
        self.sprite = pygame.image.load(dir_sprites['cloud']) 
        