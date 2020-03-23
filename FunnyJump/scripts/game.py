import pygame
from pygame.locals import *
from math import sqrt

from variables import *
from player	import *
from cloud import *
from obstacle import *
from itens import *


class Game:
	def __init__(self):
		pygame.init()
		screen = pygame.display.set_mode((constants['SCREEN_W'],constants['SCREEN_H']))
		pygame.display.set_caption(window_title)
		icon = pygame.image.load(dir_icon)
		pygame.display.set_icon(icon)
		

		ms = MainScreen(level=1,speed_obstacles=constants['INITIAL_OBSTACLES_SPEED'])
		ms.graphical_loop(screen,list(constants['START_POSITION_PLAYER']),dir_sprites,dir_sounds,dir_fonts)


class MainScreen:
	def __init__(self,level,speed_obstacles):
		self.level = level
		self.speed_obstacles = speed_obstacles
		
		#clock system...
		self.clock = pygame.time.Clock()
		
		self.background_image	= pygame.image.load(dir_sprites['bg']).convert()
		
		#one player...
		self.player =	Player(dir_sprites,dir_sounds,dir_fonts)

		#four	itens...
		self.item_life = Item(dir_sprites,'life',(690,350))
		self.item_bronze_coin	= Item(dir_sprites,'bronze-coin',(1250,350))
		self.item_silver_coin	= Item(dir_sprites,'silver-coin',(1650,350))
		self.item_gold_coin =	Item(dir_sprites,'gold-coin',(2650,350))

		#three obstacles...
		self.obstacle1 = Obstacle(dir_sprites,'obstacle',(1000,350))
		self.obstacle2 = Obstacle(dir_sprites,'obstacle',(1400,350))
		self.obstacle3 = Obstacle(dir_sprites,'obstacle',(1300,350))

		#three clouds...
		self.cloud1 =	Cloud(dir_sprites,'cloud',(1100,30))
		self.cloud2 =	Cloud(dir_sprites,'cloud',(1150,30))
		self.cloud3 =	Cloud(dir_sprites,'cloud',(1300,30))		
	
	def _calculate_distance_between_obstacles(self,obstacle1,obstacle2):
		return sqrt((obstacle1.attributes['position'][0]-obstacle2.attributes['position'][0])	** 2 + (obstacle1.attributes['position'][1]-obstacle2.attributes['position'][1]) **	2)
	def _calculate_distance_required(self,player,level):
		num_frames_subida_pulo = 1
		num_frames_descida_pulo =	player.attributes['hjump'] / player.attributes['gravity']
		obstacles_speed =	constants['INITIAL_OBSTACLES_SPEED']
		
		min_distance = (num_frames_subida_pulo + num_frames_descida_pulo)	* obstacles_speed  
		gap_distance = (min_distance * (10 / level))
		
		distance_required	= min_distance + gap_distance
		return distance_required
	def _fix_distance_between_obstacles(self,player,list_obstacles,level):
		distance_required	= self._calculate_distance_required(player,level)
		for i	in range(len(list_obstacles)):
			for j in	range(len(list_obstacles)):
				if i !=	j:
					if	self._calculate_distance_between_obstacles(list_obstacles[i],list_obstacles[j])	< distance_required:
						list_obstacles[j].attributes['position'][0] =	list_obstacles[i].attributes['position'][0]	+ distance_required	
				else:
					continue
	def increase_level(self):
		self.level +=	1
		self.speed_obstacles += (self.level /	10)
		self.player.attributes['gravity']	+= (self.level / 100)
		print('level ->',self.level,'speed ->',self.speed_obstacles,'gravity ->',self.player.attributes['gravity'])
	def player_pass_to_next_level(self):
		if self.player.hud.attributes['score'] > (10000 *	self.level):
			return True
		return False
	def player_die(self):
		return self.player.hud.attributes['lifes'] <=	0
	def graphical_loop(self,screen,initial_player_position,dir_sprites,dir_sounds,dir_fonts):
	
		pygame.mixer.music.load(dir_sounds['music'])
		pygame.mixer.music.set_volume(0.3)
		pygame.mixer.music.play(-1)

		player_touch_the_ground =	True
		while	True:
			self.clock.tick(constants['FPS_MAX'])
			#print(self.clock.get_fps())
			count_obstacles_passed = 0
			screen.blit(self.background_image,(0,0))

			for event in	pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if event.type == KEYDOWN:
					if	event.key == pygame.K_q:
						pygame.quit()
						exit()
				if event.type == MOUSEBUTTONDOWN:
					if	event.button ==	1 and player_touch_the_ground:
						self.player.jump()


			player_touch_the_ground = self.player.fall()		  

			self.item_life.graphical_loop(screen,initial_player_position,self.speed_obstacles)
			self.item_bronze_coin.graphical_loop(screen,initial_player_position,self.speed_obstacles)
			self.item_silver_coin.graphical_loop(screen,initial_player_position,self.speed_obstacles)
			self.item_gold_coin.graphical_loop(screen,initial_player_position,self.speed_obstacles)
			
			count_obstacles_passed += self.obstacle1.graphical_loop(screen,initial_player_position,self.speed_obstacles)
			count_obstacles_passed += self.obstacle2.graphical_loop(screen,initial_player_position,self.speed_obstacles)
			count_obstacles_passed += self.obstacle3.graphical_loop(screen,initial_player_position,self.speed_obstacles)
			self._fix_distance_between_obstacles(self.player,[self.obstacle1,self.obstacle2,self.obstacle3],self.level)
			
			self.cloud1.graphical_loop(screen,initial_player_position,self.speed_obstacles)
			self.cloud2.graphical_loop(screen,initial_player_position,self.speed_obstacles)
			self.cloud3.graphical_loop(screen,initial_player_position,self.speed_obstacles)

			self.player.graphical_loop(constants,count_obstacles_passed,screen,[self.item_life,self.item_bronze_coin,self.item_silver_coin,self.item_gold_coin,self.obstacle1,self.obstacle2,self.obstacle3])

			
			if self.player_pass_to_next_level():
				self.increase_level()
				self.player.sounds['score_plus'].play()
				
			
			if self.player_die():
				pygame.quit()
				exit()	  
			
			pygame.display.update()

