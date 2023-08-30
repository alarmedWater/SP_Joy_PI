from typing import Self
import pygame
from pygame.locals import *
import pickle 
from os import path 

pygame.init()


clock = pygame.time.Clock()
fps = 60

screen_width = 500
screen_higth = 500



#load images
background_1 = pygame.image.load('/Users/juli/Softwareporjekt/Code/Bilder/Hintergrund/Hintergrund_level1.jpg') #/Users/juli/Softwareporjekt

#load buttons
restart_img = pygame.image.load('/Users/juli/Softwareporjekt/Code/Bilder/Buttons/restart_button.png')
start_img =  pygame.image.load('/Users/juli/Softwareporjekt/Code/Bilder/Buttons/start.png')
exit_img  = pygame.image.load('/Users/juli/Softwareporjekt/Code/Bilder/Buttons/exit.png')



#restet level
def reset_level(level):
	player.reset(100, screen_higth - 130)
	blob_group.empty()
	lava_group.empty()
	protal_group.empty()

	#load in level data and create world
	if path.exists(f'level{level}_data'):
		pickle_in = open(f'level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)

	return world
#Screen setup

screen = pygame.display.set_mode((screen_width, screen_higth))

pygame.display.flip()


#gameVaibales
#scaling 
###player_higth = screen_higth //16.667
##player_witgh = screen_width // 11.76  

tile_size = screen_higth // 20 
game_over = 0 #  -1 = lost ; 1 = won
main_menu = True
level = 0
max_level = 3



class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False
	def draw(self):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] ==1 and self.clicked == False:
				action = True
				self.clicked = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		screen.blit(self.image, self.rect)
		return 	action

class Player():
	def __init__(self, x, y):
		self.reset(x,y)
	
	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 5

		if game_over == 0:
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				self.vel_y = -12
				self.jumped = True
			if key[pygame.K_SPACE] == False :
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 3
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 3
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]
					
		#handle animation
			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]
				
			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#check for collision
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False
			#enemy colliton check
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1
				#lava colliton check
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				#portal colliton check
			if pygame.sprite.spritecollide(self, protal_group, False):
				game_over = 1
				


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy
		elif game_over == -1:
			self.image = self.dead_image
			self.rect.y -= 5
			
		#draw player onto screen
		screen.blit(self.image, self.rect)
		pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
		return game_over
	
	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 5):
			img_right = pygame.image.load('/Users/juli/Softwareporjekt/Code/Bilder/Player/palyer1.png') #{num}
			img_right = pygame.transform.scale(img_right, (20, 50))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('/Users/juli/Softwareporjekt/Code/Bilder/Player/player_dead.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.y = y 
		self.rect.x = x
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True

		
class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('/Users/juli/Softwareporjekt/Code/Bilder/Enemy/enemy_1.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
				self.move_direction *= -1
				self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('/Users/juli/Softwareporjekt/Code/Bilder/Enemy/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 1.5))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('/Users/juli/Softwareporjekt/Code/Bilder/Rewards/coin.png')
		self.image = pygame.transform.scale(img, (tile_size//2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		

class Portal(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('Bilder/Walls/portal.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size//  0.75))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y




class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		brickblock_img = pygame.image.load('brick-wall.png')
		blocks_img = pygame.image.load('Bilder/Walls/blocks.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(brickblock_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(blocks_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size -20)
					blob_group.add(blob) 
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size+10)
					lava_group.add(lava)
				if tile == 7:
					coin = Coin(col_count * tile_size + (tile_size//2), row_count * tile_size + (tile_size//2))
					coin_group.add(coin)
				if tile == 8: 
					portal = Portal(col_count * tile_size, row_count * tile_size -10)
					protal_group.add(portal)					
					 


				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])



world_data_testlevel = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 3, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


run = True

player = Player(100, screen_higth - 130)

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
protal_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

#level laden und welt aufbauen
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data','rb')
	world_data = pickle.load(pickle_in)
world = World(world_data_testlevel)


#buttons
restart_button = Button(screen_width // 2 -100 , screen_higth//2, restart_img)
start_button = Button(screen_width // 2 -200 , screen_higth//2, start_img)
exit_button = Button(screen_width // 2 +50 , screen_higth//2, exit_img)


while run:
	clock.tick(fps)

	screen.blit(background_1,(0, 0))

	if main_menu == True:
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
	else:
		world.draw()


		if game_over == 0:
			blob_group.update()


		blob_group.draw(screen)
		lava_group.draw(screen)
		protal_group.draw(screen)

		game_over = player.update(game_over)

		#died
		if game_over == -1:
			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				game_over = 0


		#level finished
		if game_over == 1:
			level += 1
			#max level
			
			if level <= max_level:
				world_data = []
				world = reset_level(level)
				game_over = 0
			else: 
				if restart_button.draw():
					level = 1
					#reset level
					world_data = []
					world = reset_level(level)
					game_over = 0
	
	

    #eventhandler closing 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
        
	pygame.display.update()    
    
pygame.quit()       

