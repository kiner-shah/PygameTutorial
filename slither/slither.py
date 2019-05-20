import pygame, sys, time, random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Colors in RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
BLUE = (0, 0, 255)

display_width = 800
display_height = 600

# Get the surface object
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')

# Load game icon
icon = pygame.image.load('apple_trans.png')
pygame.display.set_icon(icon)

# Load snake head image
img = pygame.image.load('snake_head_trans.png')
# Load apple image
apple_img = pygame.image.load('apple_trans.png')

# Frames per second
FPS = 15

direction = "right"

# Clock object
clock = pygame.time.Clock()

block_size = 20
apple_thickness = 30

# Font objects
smallfont = pygame.font.Font("KOMIKAX_.ttf", 15)
mediumfont = pygame.font.Font("KOMIKAX_.ttf", 30)
largefont = pygame.font.Font("KOMIKAX_.ttf", 50)

def pause():
    paused = True
    #gameDisplay.fill(WHITE)
    message_to_screen("Paused", BLACK, -100, "large")
    message_to_screen("Press C to continue, Q to quit", BLACK, 25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_c:
                    paused = False
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(5)

def score(score):
    text = smallfont.render("Score: " + str(score), True, BLACK)
    gameDisplay.blit(text, (0, 0))

def rand_apple_gen():
    rand_apple_x = round(random.randrange(0, display_width - apple_thickness)) #/ 10.0) * 10.0
    rand_apple_y = round(random.randrange(0, display_height - apple_thickness)) #/ 10.0) * 10.0
    return rand_apple_x, rand_apple_y

def game_intro():
    intro = True
    while intro:
        gameDisplay.fill(WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_c:
                    intro = False
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()

        message_to_screen("Welcome to Slither", GREEN, -100, "large")
        message_to_screen("The objective of the game is to eat red apples", BLACK, -30)
        message_to_screen("The more apples you eat, the longer you get", BLACK, -10)
        message_to_screen("If you run into yourself or the edges, you die", BLACK, 50)
        message_to_screen("Press C to play, P to pause or Q to quit", BLACK, 180)
        pygame.display.update()
        clock.tick(5)

def snake(block_size, snake_list):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    elif direction == "left":
        head = pygame.transform.rotate(img, 90)
    elif direction == "up":
        head = img
    elif direction == "down":
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, snake_list[-1])
    for (x, y) in snake_list[:-1]:
        pygame.draw.rect(gameDisplay, DARKGREEN, (x, y, block_size, block_size))

def text_objects(text, color, size):
    if size == "small":
        text_surface = smallfont.render(text, True, color)
    elif size == "medium":
        text_surface = mediumfont.render(text, True, color)
    elif size == "large":
        text_surface = largefont.render(text, True, color)

    return text_surface, text_surface.get_rect()

def message_to_screen(msg, color, y_displace = 0, size = "small"):
    text_surface, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2, display_height / 2 + y_displace)
    gameDisplay.blit(text_surface, text_rect)

# Game loop
def game_loop():
    global direction
    direction = "right"
    # Head of snake
    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 10
    lead_y_change = 0

    snake_list = []
    snake_len = 1

    # Apple position
    rand_apple_x, rand_apple_y = rand_apple_gen()

    gameExit = False
    gameOver = False

    while not gameExit:
        if gameOver == True:
            #gameDisplay.fill(WHITE)
            message_to_screen("Game over",
                                RED,
                                -50,
                                "large")
            message_to_screen("Press C to play again or Q to quit",
                                BLACK,
                                50,
                                "medium")
            pygame.display.update()

        while gameOver == True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameExit = True
                    gameOver = False
                elif event.type == KEYDOWN:
                    if event.key == K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == QUIT:
                gameExit = True
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == K_p:
                    pause()

        # Out of window boundaries
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        # Set background as white
        gameDisplay.fill(WHITE)
        # Draw apple
#        pygame.draw.rect(gameDisplay, RED, (rand_apple_x, rand_apple_y, apple_thickness, apple_thickness))
        gameDisplay.blit(apple_img, (rand_apple_x, rand_apple_y))
        # Draw snake
        snake_head = (lead_x, lead_y)
        snake_list.append(snake_head)
        # Reduce the snake tail length by 1 if length of list exceeds the snake length
        # Note tail coordinates are actually at the beginning of the list
        if len(snake_list) > snake_len:
            del snake_list[0]
        # for any segment before last one
        for segment in snake_list[:-1]:
            if segment == snake_head:
                gameOver = True

        snake(block_size, snake_list)
        score(snake_len - 1)
        pygame.display.update()

        if (lead_x > rand_apple_x and lead_x < rand_apple_x + apple_thickness) or (lead_x + block_size > rand_apple_x and lead_x + block_size < rand_apple_x + apple_thickness):
            if (lead_y > rand_apple_y and lead_y < rand_apple_y + apple_thickness) or (lead_y + block_size > rand_apple_y and lead_y + block_size < rand_apple_y + apple_thickness):
                rand_apple_x, rand_apple_y = rand_apple_gen()
                snake_len += 1

        # Make the clock tick as per FPS rate set
        clock.tick(FPS)

    pygame.quit()
    # Instead of sys.exit(), we can use quit()
    sys.exit()

game_intro()
game_loop()
