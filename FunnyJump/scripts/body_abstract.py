from random	import seed,randrange
import pygame
from pygame.locals import *
from variables import *

#BodyAbstract has few attributes also presents in Item and Obstacle...
class BodyAbstract:
	def __init__(self,type_item,position):
		self.attributes =	{'position':list(position),'type':type_item}
		self.sprite =	None
	def move(self,initial_player_position,screen_width,screen_height,speed_obstacles):
		#if the object is	a cloud, she will move with	less speed...
		if self.attributes['type'] ==	'cloud':
			speed_obstacles *= 0.1
			
		self.attributes['position'][0] -=	speed_obstacles
		
		#if the object exists	from screen...
		if self.attributes['position'][0]	<= (0 -	self.sprite.get_width()):
			seed()
			self.attributes['position'][0] =	randrange(screen_width,screen_width	* 5)
			#if the object is an	collected item...
			if self.attributes['type'] != 'obstacle'	and	self.attributes['type']	!= 'cloud':
				#I also	change the position	in y...	
				self.attributes['position'][1] = randrange(screen_height //	3,screen_height	// 2)
			#if the object is an	obstacle...
			elif	self.attributes['type']	== 'obstacle':
				#I reset the position.y...
				self.attributes['position'][1] = initial_player_position[1]
				#I change for randomic sprite...
				self._generate_random_obstacle()
				
		if (0 -	self.sprite.get_width()) < self.attributes['position'][0] < initial_player_position[0]:
			#Player jump the obstacle without to collide...
			#so I return qtd obstacles passed as 1...
			return 1
		else:
			return 0		
	def graphical_loop(self,screen,initial_player_position,speed_obstacles):
		qtd_obstacles_passed = self.move(initial_player_position,screen.get_width(),screen.get_height(),speed_obstacles)
		screen.blit(self.sprite,self.attributes['position'])
		return qtd_obstacles_passed
