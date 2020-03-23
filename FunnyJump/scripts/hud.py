from math import floor,ceil
import pygame
from pygame.locals import *
from variables import *

class Hud:
    def __init__(self,dir_sprites,dir_fonts,score=0,lifes=constants['MAX_PLAYER_LIFES'],color_font = (0,0,0)):
        self.attributes = {'score':score,'lifes':lifes,'color_font':color_font}
        self.font_score = pygame.font.Font(dir_fonts['font_score'],30)
        self.item_life = pygame.image.load(dir_sprites['life']).convert_alpha()
    def set_score(self,new_score):
        self.attributes['score'] = new_score
    def get_score(self):
        return self.attributes['score']
    
    def set_lifes(self,num_lifes):
        self.attributes['lifes'] = num_lifes
    def get_lifes(self):
        return self.attributes['lifes']
    
    def set_color_font(self,new_color):
        self.attributes['color_font'] = new_color
    def get_color_font(self):
        return self.attributes['color_font']
    
    def increase_score(self,increase_score):
        self.attributes['score'] += increase_score
    def increase_lifes(self,increase_num_lifes):
        self.attributes['lifes'] += increase_num_lifes
        if self.attributes['lifes'] > constants['MAX_PLAYER_LIFES']:
            self.set_lifes(constants['MAX_PLAYER_LIFES'])
    
    def decrease_score(self,decrease_score):
        self.attributes['score'] -= decrease_score
        if self.attributes['score'] < 0:
            self.set_score(0)
    def decrease_lifes(self,decrease_num_lifes):
        self.attributes['lifes'] -= decrease_num_lifes
        if self.attributes['lifes'] < 0:
            self.set_lifes(0)

    def graphical_loop(self,constants,count_obstacles_passed,screen):
        #increase the score using count_obstacles_passed...
        self.increase_score(ceil(count_obstacles_passed * 0.5))
        #get data a object structure...
        score = self.get_score()
        lifes = self.get_lifes()
        color_font = self.get_color_font()
        
        #limit the number of caracters show on screen...
        #limits in >= 10000 and >= 1000000
        if score >= 10000 and score < 1000000:
            score = str(floor(score / 1000)) + "K"
        elif score >= 1000000:
            score = str(floor(score / 1000000)) + "M"
            
        font_surface = self.font_score.render(str(score),True,color_font)
        
        #draw objects at screen...
        width_item_life = self.item_life.get_width()
        x = constants['SCREEN_W'] - width_item_life
        for i in range(self.get_lifes()):
            screen.blit(self.item_life,(x,0))
            x -= width_item_life
            
        screen.blit(font_surface,((constants['SCREEN_W'] - font_surface.get_width() ) // 2,constants['SCREEN_H'] // 3))
