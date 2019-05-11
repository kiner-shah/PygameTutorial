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
YELLOW = (200, 200, 0)

display_width = 800
display_height = 600

# Get the surface object
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tanks')

# Load game icon
#icon = pygame.image.load('apple_trans.png')
#pygame.display.set_icon(icon)

# Load snake head image
#img = pygame.image.load('snake_head_trans.png')
# Load apple image
#apple_img = pygame.image.load('apple_trans.png')

# Frames per second
FPS = 15

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

def is_mouse_on_button(pos_tuple, tlx, tly, w, h):
    x, y = pos_tuple
    if x >= tlx and x <= tlx + w:
        if y >= tly and y <= tly + h:
            return True
    return False

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

        message_to_screen("Welcome to Tanks", GREEN, -100, "large")
        message_to_screen("The objective is to shoot and destroy", BLACK, -30)
        message_to_screen("the enemy tank before they destroy you.", BLACK, -10)
        message_to_screen("The more enemies you destroy, the harder they get", BLACK, 50)
        #message_to_screen("Press C to play, P to pause or Q to quit", BLACK, 180)
        cur = pygame.mouse.get_pos()
        if is_mouse_on_button(cur, 150, 400, 100, 50):
            pygame.draw.rect(gameDisplay, GREEN, (150, 400, 100, 50))
        else:
            pygame.draw.rect(gameDisplay, DARKGREEN, (150, 400, 100, 50))
        pygame.draw.rect(gameDisplay, YELLOW, (350, 400, 100, 50))
        pygame.draw.rect(gameDisplay, RED, (550, 400, 100, 50))
        
        text_to_button("PLAY", BLACK, 150, 400, 100, 50)
        text_to_button("CONTROLS", BLACK, 350, 400, 100, 50)
        text_to_button("EXIT", BLACK, 550, 400, 100, 50)

        pygame.display.update()
        clock.tick(15)

def text_objects(text, color, size):
    if size == "small":
        text_surface = smallfont.render(text, True, color)
    elif size == "medium":
        text_surface = mediumfont.render(text, True, color)
    elif size == "large":
        text_surface = largefont.render(text, True, color)

    return text_surface, text_surface.get_rect()

def text_to_button(message, color, buttonx, buttony, buttonw, buttonh, size = "small"):
    text_surface, text_rect = text_objects(message, color, size)
    text_rect.center = (buttonx + (buttonw / 2), buttony + (buttonh / 2))
    gameDisplay.blit(text_surface, text_rect)

def message_to_screen(msg, color, y_displace = 0, size = "small"):
    text_surface, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2, display_height / 2 + y_displace)
    gameDisplay.blit(text_surface, text_rect)

# Game loop
def game_loop():
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
                    pass
                elif event.key == K_RIGHT:
                    pass
                elif event.key == K_UP:
                    pass
                elif event.key == K_DOWN:
                    pass
                elif event.key == K_p:
                    pause()

        gameDisplay.fill(WHITE)
        pygame.display.update()
        # Make the clock tick as per FPS rate set
        clock.tick(FPS)

    pygame.quit()
    # Instead of sys.exit(), we can use quit()
    sys.exit()

game_intro()
game_loop()
