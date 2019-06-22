import pygame, random, os
from pygame.locals import *

WIDTH = 800
HEIGHT = 600
FPS = 30

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up assets folders
game_folder = os.path.dirname(__file__)		# get the directory where this (current) file is
img_folder = os.path.join(game_folder, "img")
sound_folder = os.path.join(game_folder, "sound")

# Player is derived class from base class pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
	# constructor
	def __init__(self):
		# call the base class constructor
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load(os.path.join(img_folder, "robot_pic.png")).convert()
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH / 2, HEIGHT / 2)

	# override update function
	def update(self):
		self.rect.x += 5
		if self.rect.left > WIDTH:
			self.rect.right = 0

# initialization
pygame.init()
pygame.mixer.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game title")
clock = pygame.time.Clock()

# sprites group
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# game loop
running = True
while running:
	# event handler
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

	# update sprite group
	all_sprites.update()

	# draw / render
	display.fill(BLACK)
	all_sprites.draw(display)

	# after drawing everything, flip (or update) display
	pygame.display.flip()

	# keep game loop at right speed
	clock.tick(FPS)

pygame.quit()
quit()