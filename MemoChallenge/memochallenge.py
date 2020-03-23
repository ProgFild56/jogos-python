import pygame
from random import randrange
from time import sleep

white = (255,255,255)

red = (50,0,0)
green = (0,50,0)
blue = (0,0,50)
yellow = (50,50,0)
magent = (50,0,50)
cian = (0,50,50)

normal_colors = [red,green,blue,yellow,magent,cian]


light_red = (255,0,0)
light_green = (0,255,0)
light_blue = (0,0,255)
light_yellow = (255,255,0)
light_magent = (255,0,255)
light_cian = (0,255,255)

light_colors = [light_red,light_green,light_blue,light_yellow,light_magent,light_cian]


screen_width , screen_height  = 900 , 600

width_buttons,height_button = screen_width // 3 , screen_height // 2

red_button = pygame.Rect((0,0,width_buttons,height_button)) 
green_button = pygame.Rect((width_buttons,0,width_buttons,height_button)) 
blue_button = pygame.Rect((width_buttons * 2,0,width_buttons,height_button)) 
yellow_button = pygame.Rect((0,height_button,width_buttons,height_button)) 
magent_button = pygame.Rect((width_buttons,height_button,width_buttons,height_button)) 
cian_button = pygame.Rect((width_buttons * 2,height_button,width_buttons,height_button)) 

buttons = [red_button,green_button,blue_button,yellow_button,magent_button,cian_button]






class MemoBall:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((screen_width , screen_height))
		pygame.display.set_caption("Memo Challenge (" + "Sequência de 3 botões)")
		pygame.display.set_icon(pygame.image.load("icon.png"))
		self.sound_lose = pygame.mixer.Sound("lose.ogg")
		self.sound_congratulations = pygame.mixer.Sound("congratulations.ogg")
		self.len_sequence = 3
		self.random_sequence = []
		self.player_sequence = []
		self.loop()
	
	def draw_button(self,color_button,button_rect):
		pygame.draw.rect(self.screen,color_button,button_rect)
	
	def generate_random_sequence(self):
		self.random_sequence = []
		for i in range(self.len_sequence):
			self.random_sequence.append(randrange(6))
		#print("computador sorteou >>",self.random_sequence)
	
	def select_effect(self,num_button):
		self.draw_button(normal_colors[num_button],buttons[num_button])
		pygame.display.update()
		sleep(0.6)
		self.draw_button(light_colors[num_button],buttons[num_button])
		pygame.display.update()
		sleep(0.2)
	
	def play_generated_sequence(self):
		for num_button in self.random_sequence:
			self.select_effect(num_button)

	def wait_player(self):
		clicks = 0
		self.player_sequence = []
		while clicks < self.len_sequence:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						cursor = pygame.Rect(event.pos,(5,5))
						for num_button in range(len(buttons)):
							if cursor.colliderect(buttons[num_button]):
								self.select_effect(num_button)
								
								self.player_sequence.append(num_button)
								clicks += 1
								
								break

	def increase_difficulty_or_exit(self):
		#player right the sequence...
		if self.player_sequence == self.random_sequence:
			self.len_sequence += 1
			#generate new sequence with one more random button...
			self.generate_random_sequence()
			#play congratulations sound...
			self.sound_congratulations.play()
			pygame.display.set_caption("Memo Challenge (" + "Sequência de " + str(self.len_sequence) + " botões)")
			sleep(3.5)
		else:
			#play lose sound...
			self.sound_lose.play()
			sleep(3.0)
			#exit the game...
			pygame.quit()
			exit()
		

	def loop(self):
		clock = pygame.time.Clock()

		self.generate_random_sequence()
		while True:
			clock.tick(60)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
			
			self.screen.fill(white)
			
			self.draw_button(light_red,red_button)
			self.draw_button(light_green,green_button)
			self.draw_button(light_blue,blue_button)
			self.draw_button(light_yellow,yellow_button)
			self.draw_button(light_magent,magent_button)
			self.draw_button(light_cian,cian_button)
		
			self.play_generated_sequence()
			
			self.wait_player()

			#print("jogador clicou >>",self.player_sequence)
			self.increase_difficulty_or_exit()

if __name__ == "__main__":
	MemoBall()