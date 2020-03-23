from body_abstract import BodyAbstract
import pygame
from random import seed,randrange
from pygame.locals import *
from variables import *

class Obstacle(BodyAbstract):
    def __init__(self,dir_sprites,type_item,position):
        super().__init__(type_item,position)
        self.obstacles = {'cactus_tall':pygame.image.load(dir_sprites['cactus_tall']).convert_alpha(),'cactus_large':pygame.image.load(dir_sprites['cactus_large']).convert_alpha(),'cactus_small':pygame.image.load(dir_sprites['cactus_small']).convert_alpha(),'skeleton':pygame.image.load(dir_sprites['skeleton']).convert_alpha()}
        self._generate_random_obstacle()
    def _generate_random_obstacle(self):
        seed()
        list_keys = list(self.obstacles.keys())
        random_index = randrange(len(list_keys))
        random_key = list_keys[random_index]
        self.sprite = self.obstacles[random_key]
        
        #handler in position of obstacles with less height... 
        #30px less...
        if self.sprite == self.obstacles['skeleton'] or self.sprite == self.obstacles['cactus_small']:
            self.attributes['position'][1] += 30