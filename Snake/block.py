import pygame
from pygame.locals import *
from constants import *

class Block:
	#Model...
	def __init__(self,pos = INITIAL_POS_SNAKE,type	= BLOCK_SNAKE,dimensions = DIMENSIONS_BLOCKS,next_block_pos	= INITIAL_POS_SNAKE):
		self.type	= type
		self.pos = list(pos)
		self.dimensions =	list(dimensions)

		if type == BLOCK_SNAKE:
			self.next_block_pos = list(next_block_pos)
			
		self._load_itens_block(type)
	def _load_itens_block(self,type):
		if type == BLOCK_SNAKE:
			self.color =	(255,255,255)
			
		elif type	== BLOCK_FEED_APPLE:
			self.color =	(255,0,0)
			
		elif type	== BLOCK_FEED_GRAPE:
			self.color =	(100,0,102)
			
		elif type	== BLOCK_FEED_LEMON:
			self.color =	(0,255,0)
			
		elif type	== BLOCK_FEED_BIRD:
			self.color =	(252,242,99)
			
		elif type	== BLOCK_FEED_TURTLE:
			self.color =	(102,178,255)
			
		elif type	== BLOCK_FEED_MOUSE:
			self.color =	(255,204,204)
			
 
		self.sprite =	pygame.Surface(self.dimensions).convert()
		self.sprite.fill(self.color)
		pygame.draw.rect(self.sprite,(0,0,0),(0,0,DIMENSIONS_BLOCKS[0],DIMENSIONS_BLOCKS[1]),2)
	#Controller...
	def change_block(self,pos,type):
		return Block(list(pos),type)
	def move_block(self,vector_direction):
		self.pos[0] += vector_direction[0] * self.dimensions[0]
		self.pos[1] += vector_direction[1] * self.dimensions[1] 
	#View...
	def draw_block(self,screen):
		screen.blit(self.sprite,self.pos)

	def __str__(self):
	  return "Type:{}\nPosition:{}\nDimensions:{}".format(self.type, self.pos,	self.dimensions)	
