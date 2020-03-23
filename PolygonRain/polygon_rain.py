import pygame
from pygame.locals import *
from random import randrange
from math import ceil


fps = 60
width_player,height_player = 20,20
width_meteors,height_meteors = 20,20
width_screen,height_screen = 640,480
bg_color_screen = (160,160,160)
bg_color_player = (0,0,0)
bg_color_meteor = (123,45,153)

posy_start_player = height_screen - height_player
initial_gravity_force = 5
gravity_force = 5


background_music = "background-music.mp3"
image_icon = "icon.png"

pygame.init()

screen = pygame.display.set_mode((width_screen,height_screen))
pygame.display.set_caption("polygon rain")
icon = pygame.image.load(image_icon)
pygame.display.set_icon(icon)


clock = pygame.time.Clock()


pygame.mouse.set_visible(0)


player = pygame.Rect((0,posy_start_player,width_player,height_player))
meteor = pygame.Rect((0,0,width_meteors,height_meteors))


#play background music...
pygame.mixer.music.load(background_music)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

while True:
	clock.tick(fps)

	screen.fill(bg_color_screen)
	pygame.draw.rect(screen,bg_color_player,player)
	
	#player movement...
	for event in pygame.event.get():
		if event.type == pygame.MOUSEMOTION:
			player.x  = pygame.mouse.get_pos()[0]
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	#meteor movement...
	if meteor.y <= screen.get_height():
		meteor.y += gravity_force
		pygame.draw.rect(screen,bg_color_meteor,meteor)

	else:
		#randomize meteor...
		meteor.x = randrange(0,width_screen - width_meteors)
		meteor.y = 0
		
	
	#detections...
	collision = player.colliderect(meteor)
	
	if collision:
		player.w += ceil(player.w * 0.05) #+5%
		meteor.y = height_screen * 2
	
	elif meteor.y >= height_screen:
		if player.w - ceil(player.w * 0.5) > 1:
			player.w -= ceil(player.w * 0.7) #-70%
		else:
			player.w = 1

		meteor.y = -height_screen * 2

	if player.w >= width_screen:
		print("GANHOU!!!")
		break
	elif player.w <= 1:
		print("PERDEU!!!")
		break
		
	#level design...
	dificulty =  (player.w / width_screen) * 6
	gravity_force = initial_gravity_force + (initial_gravity_force * dificulty) 
	print("pw",player.w,"dif",dificulty,"gf",gravity_force)


	pygame.display.update()



pygame.quit()
