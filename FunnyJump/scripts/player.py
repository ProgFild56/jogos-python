from hud import Hud
import pygame
from pygame.locals import *
from variables import *

#Player has Hud...
class Player:
    def __init__(self,dir_sprites,dir_sounds,dir_fonts,lifes=constants['MAX_PLAYER_LIFES'],hjump=constants['INITIAL_PLAYER_HJUMP'],gravity = constants['INITIAL_PLAYER_GRAVITY'], position = list(constants['START_POSITION_PLAYER'])):
        self.hud = Hud(dir_sprites,dir_fonts,lifes=lifes)
        self.sprites = {'wait':pygame.image.load(dir_sprites['player_wait']).convert_alpha(),'run':pygame.image.load(dir_sprites['player_run']).convert_alpha(),'hurt':pygame.image.load(dir_sprites['player_hurt']).convert_alpha()}
        #the following attribute will be modified in method _run...
        self.sprite_base = self.sprites['wait']
        self.sounds = {'score_plus':pygame.mixer.Sound(dir_sounds['sound_player_score_plus'])}
        self.attributes = {'hjump':hjump,'gravity':gravity,'position':position}
    def collision(self,body2):
        
        player_position = list(self.attributes['position'])
        player_dimensions = [self.sprite_base.get_width(), self.sprite_base.get_height()]
        body2_position = list(body2.attributes['position'])
        body2_dimensions = [body2.sprite.get_width(), body2.sprite.get_height()]
        
        player_rect = pygame.Rect(player_position,player_dimensions)
        body2_rect = pygame.Rect(body2_position,body2_dimensions)

        collided = player_rect.colliderect(body2_rect)
        
        if collided:
            if body2.attributes['type'] == 'obstacle':
                self.hud.decrease_lifes(1)
                #self.sounds['hurt'].play()
            #body2 is a coin or life item...
            elif body2.attributes['type'] == 'life':
                self.hud.increase_lifes(body2.attributes['life_increase'])
                #self.sounds['get_life'].play()
            elif body2.attributes['type'] == 'bronze-coin':
                self.hud.increase_score(body2.attributes['score_increase'])
                #self.sounds['get_coin'].play()
            elif body2.attributes['type'] == 'silver-coin':
                self.hud.increase_score(body2.attributes['score_increase'])
                #self.sounds['get_coin'].play()
            elif body2.attributes['type'] == 'gold-coin':
                self.hud.increase_score(body2.attributes['score_increase'])
                #self.sounds['get_coin'].play()
                                                  
            #body2 exit of screen (exit from the user view)...
            body2.attributes['position'][0] = -9000   
    def jump(self):
        #self.sounds['jump'].play(maxtime=100)
        self.attributes['position'][1] -= self.attributes['hjump']
        
    def run(self):
        st = ""
        
        if self.sprite_base == self.sprites['wait']:
            self.sprite_base = self.sprites['run']
            st = "run"
        elif self.sprite_base == self.sprites['run']:
            self.sprite_base = self.sprites['wait']
            st = "wait"
        
        if self.hud.get_lifes() <= 0:
            self.sprite_base = self.sprites['hurt']
            st = "hurt"
        elif self.sprite_base == self.sprites['hurt']:
            #default configs when lifes > 0 but sprite_base == 'hurt'...
            self.sprite_base = self.sprites['wait']
            st = "wait"
            
        return st
    def fall(self):
        if self.attributes['position'][1] < constants['START_POSITION_PLAYER'][1]:
            self.attributes['position'][1] += self.attributes['gravity']       
       
        touch_the_ground = self.attributes['position'][1] >= constants['START_POSITION_PLAYER'][1]
        return touch_the_ground
    def graphical_loop(self,constants,count_obstacles_passed,screen,bodys_in_the_screen):
        #run the graphical loop of the HUD...
        self.hud.graphical_loop(constants,count_obstacles_passed,screen)
        status_return = self.run()
        #print(status_return)
        for body in bodys_in_the_screen:
            self.collision(body)
            
        screen.blit(self.sprite_base,self.attributes['position'])