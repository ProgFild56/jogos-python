import pygame
from pygame.locals import *
from random import randrange
from constants import *
from block import Block
from snake import Snake


class Board:
	#Model...
	def __init__(self,title=TITLE_SCREEN,dimensions=list(DIMENSIONS_SCREEN),color_fill=list(BACKGROUND_COLOR)):
		pygame.init()
		#tem que ser antes da	criacao	da snake para permitir usar	o metodo convert dentro	dela em	sua	criacao...
		self.create_window(title,dimensions,color_fill)
		self.create_clock()
		self.snake = Snake()
		self.feeds = []
	#View...
	def create_window(self,title,dimensions,color_fill):
		self.title = title
		self.dimensions =	dimensions
		self.color_fill =	color_fill
		pygame.display.set_caption(title)
		self.screen =	pygame.display.set_mode(self.dimensions,pygame.SWSURFACE,32)
		self.screen.fill(self.color_fill)
	def create_clock(self):
		self.clock = pygame.time.Clock()
	def feeds_loop(self,screen):
		for feed in self.feeds:
			feed.draw_block(screen)
		pygame.display.update()
	#Controller...
	def _generate_random_feeds(self):
		#randomize the new block...
		for i in range(5):
			pos =	[randrange(self.dimensions[0] - DIMENSIONS_BLOCKS[0]),randrange(self.dimensions[1] - DIMENSIONS_BLOCKS[1])]
			type = randrange(BLOCK_FEED_APPLE,BLOCK_FEED_MOUSE)
			new_block	= Block(list(pos),type)
			self.feeds.append(new_block)		
	def play_bg_music(self):
		pygame.mixer.music.load(PATH_BACKGROUND_MUSIC)
		pygame.mixer.music.set_volume(0.3)
		pygame.mixer.music.play(-1)
	def collect_feed(self):
		snake_head = pygame.Rect(list(self.snake.leader_block.pos),list(self.snake.leader_block.dimensions))
		for feed in self.feeds:
			if pygame.Rect(list(feed.pos),list(feed.dimensions)).colliderect(snake_head):
				nf = feed.change_block(feed.pos,BLOCK_SNAKE)
				self.snake.add_new_block(nf)
				self.feeds.remove(feed)		
	def is_collided(self):
		board_collided = self.snake.leader_block.pos[0] < 0 or self.snake.leader_block.pos[0] > self.dimensions[0]	or 	self.snake.leader_block.pos[1] < 0 or self.snake.leader_block.pos[1] > self.dimensions[1]
		

		body_collided = False
		if len(self.snake.snake_blocks) > 1:
			rect_second_block = pygame.Rect(list(self.snake.snake_blocks[1].pos),list(self.snake.snake_blocks[1].dimensions)) 
			for block in self.snake.snake_blocks[2:]:
				rb = pygame.Rect(list(block.pos),list(block.dimensions))
				if rb.colliderect(rect_second_block) and block not in self.feeds:
					body_collided = True
					break

		return board_collided or body_collided	
	def board_loop(self):
		self.play_bg_music()
		direction = [0,0]
		while True:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if event.type == KEYDOWN:
					if event.key == K_UP:
						direction[1] = -1
					elif event.key == K_DOWN:
						direction[1] = 1
					elif event.key == K_RIGHT:
						direction[0] = 1
					elif event.key == K_LEFT:
						direction[0] = -1

				if event.type == KEYUP:
					if event.key == K_UP:
						direction[1] = 0
					elif event.key == K_DOWN:
						direction[1] = 0
					elif event.key == K_RIGHT:
						direction[0] = 0
					elif event.key == K_LEFT:
						direction[0] = 0
			
			if len(self.feeds) == 0:
				self._generate_random_feeds()

			self.feeds_loop(self.screen)
			self.snake.snake_loop(self.screen,direction)
			self.collect_feed()
			if self.is_collided():
				pygame.quit()
				exit()
			self.screen.fill(self.color_fill)
