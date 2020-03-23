import pygame
from pygame.locals import *
from constants import *
from block import Block
from os import system

class Snake:
	#Model...
	def __init__(self):
		self.leader_block	= Block()
		self.snake_blocks	= [self.leader_block]
	#Controller...
	def _update_links_between_blocks(self):
		for i	in range(len(self.snake_blocks)-1):
			self.snake_blocks[i].next_block_pos = list(self.snake_blocks[i+1].pos)
	def _move_snake_head(self,vector_direction):
		self.snake_blocks[-1].move_block(vector_direction)
	def _move_snake_body(self):
		for i	in range(len(self.snake_blocks)-1):
			self.snake_blocks[i].pos	= list(self.snake_blocks[i].next_block_pos)
	def add_new_block(self,new_block):
		self.snake_blocks.insert(0,new_block)
		self.snake_blocks[0].next_block_pos =	list(self.snake_blocks[1].pos)
	#View...
	def _draw_snake(self,screen):

		for block	in self.snake_blocks:
			block.draw_block(screen)
			
		pygame.display.update()
		
	def snake_loop(self,screen,vector_direction):
		#atualizo	ligacoes de	todos os blocos	da snake...
		self._update_links_between_blocks()
	   
		#movo	a cabeca da	snake...
		self._move_snake_head(vector_direction)
		
		#movo	o corpo	da snake...
		if 1 in vector_direction or -1 in	vector_direction:
			self._move_snake_body()
	
	
		#desenho cada	bloco da snake...
		self._draw_snake(screen)
	def __str__(self):
		string = ""
		for block	in self.snake_blocks:
			string += 30	* "-*-"
			string += '\n'
			string += block.__str__()
		return string
