# Till tutorial 90
import pygame, sys, time, random, math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Colors in RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARKRED = (200, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
BLUE = (0, 0, 255)
DARKBLUE = (4, 4, 114)
YELLOW = (200, 200, 0)
LIGHTYELLOW = (255, 255, 12)

display_width = 800
display_height = 600

# Get the surface object
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Pseudo-3D')

# Frames per second
FPS = 15

# Clock object
clock = pygame.time.Clock()

# Font objects
smallfont = pygame.font.Font("KOMIKAX_.ttf", 15)
mediumfont = pygame.font.Font("KOMIKAX_.ttf", 30)
largefont = pygame.font.Font("KOMIKAX_.ttf", 50)

def cube(start, full_size):
    node1 = [start[0], start[1]]
    node2 = [start[0] + full_size, start[1]]
    node3 = [start[0], start[1] + full_size]
    node4 = [start[0] + full_size, start[1] + full_size]

    offset = int(full_size / 2)
    x_mid = int(display_width / 2)
    x_offset = -int(start[0] - x_mid)

    y_mid = int(display_height / 2)
    y_offset = int(start[1] - y_mid)
    if x_offset < -100:
        x_offset = -100
    elif x_offset > 100:
        x_offset = 100

    if y_offset < -100:
        y_offset = -100
    elif y_offset > 100:
        y_offset = 100

    node5 = [node1[0] + x_offset, node1[1] - y_offset]
    node6 = [node2[0] + x_offset, node2[1] - y_offset]
    node7 = [node3[0] + x_offset, node3[1] - y_offset]
    node8 = [node4[0] + x_offset, node4[1] - y_offset]

    # top line
    pygame.draw.line(gameDisplay, WHITE, node1, node2)
    # bottom line
    pygame.draw.line(gameDisplay, WHITE, node3, node4)
    # left line
    pygame.draw.line(gameDisplay, WHITE, node1, node3)
    # right line
    pygame.draw.line(gameDisplay, WHITE, node2, node4)

    # top line
    pygame.draw.line(gameDisplay, WHITE, node5, node6)
    # bottom line
    pygame.draw.line(gameDisplay, WHITE, node7, node8)
    # left line
    pygame.draw.line(gameDisplay, WHITE, node5, node7)
    # right line
    pygame.draw.line(gameDisplay, WHITE, node6, node8)

    pygame.draw.circle(gameDisplay, GREEN, node1, 5)
    pygame.draw.circle(gameDisplay, GREEN, node2, 5)
    pygame.draw.circle(gameDisplay, GREEN, node3, 5)
    pygame.draw.circle(gameDisplay, GREEN, node4, 5)

    pygame.draw.circle(gameDisplay, GREEN, node5, 5)
    pygame.draw.circle(gameDisplay, GREEN, node6, 5)
    pygame.draw.circle(gameDisplay, GREEN, node7, 5)
    pygame.draw.circle(gameDisplay, GREEN, node8, 5)

    pygame.draw.line(gameDisplay, WHITE, node1, node5)
    pygame.draw.line(gameDisplay, WHITE, node2, node6)
    pygame.draw.line(gameDisplay, WHITE, node3, node7)
    pygame.draw.line(gameDisplay, WHITE, node4, node8)

# Game loop
def game_loop():
    location = [300, 200]
    size = 100
    current_move = 0
    z_move = 0
    z_location = 50
    y_move = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    current_move = -5
                elif event.key == K_RIGHT:
                    current_move = 5
                elif event.key == K_UP:
                    y_move = -5
                elif event.key == K_DOWN:
                    y_move = 5

            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    current_move = 0
                elif event.key == K_UP or event.key == K_DOWN:
                    y_move = 0

        gameDisplay.fill(BLACK)
        location[0] += current_move
        location[1] += y_move
        if z_location + z_move > 200:
            z_move = 0
        elif z_location + z_move < 1:
            z_move = 0
        z_location += z_move
        current_size = size

        cube(location, current_size)
        pygame.display.update()
        # Make the clock tick as per FPS rate set
        clock.tick(FPS)

    pygame.quit()
    # Instead of sys.exit(), we can use quit()
    sys.exit()

game_loop()