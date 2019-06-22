import pygame, random
from pygame.locals import *

WIDTH = 800
HEIGHT = 600
FPS = 30

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# initialization
pygame.init()
pygame.mixer.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game title")
clock = pygame.time.Clock()

# sprites group
all_sprites = pygame.sprite.Group()

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