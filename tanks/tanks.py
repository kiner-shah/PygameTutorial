# Till tutorial 82
# https://bigsoundbank.com/detail-1137-firecracker-with-wick-1.html - fire sound
# https://bigsoundbank.com/detail-1023-explosion-far-away.html - explosion sound
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
pygame.display.set_caption('Tanks')

fire_sound = pygame.mixer.Sound("fire.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Frames per second
FPS = 15

# Clock object
clock = pygame.time.Clock()

tank_width = 40
tank_height = 20
turret_length = 27
turret_width = 5
wheel_width = 5

ground_height = 35

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
        click_pressed = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                click_pressed = True

        message_to_screen("Welcome to Tanks", DARKGREEN, -100, "large")
        message_to_screen("The objective is to shoot and destroy", BLACK, -30)
        message_to_screen("the enemy tank before they destroy you.", BLACK, -10)
        message_to_screen("The more enemies you destroy, the harder they get", BLACK, 50)

        button("PLAY", 150, 400, 100, 50, DARKGREEN, GREEN, action = "play", pressed = click_pressed)
        button("CONTROLS", 350, 400, 100, 50, YELLOW, LIGHTYELLOW, action = "controls", pressed = click_pressed)
        button("EXIT", 550, 400, 100, 50, DARKRED, RED, action = "quit", pressed = click_pressed)

        pygame.display.update()
        clock.tick(15)

def game_over():
    game_over = True
    while game_over:
        gameDisplay.fill(WHITE)
        click_pressed = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                click_pressed = True

        message_to_screen("Game over", DARKGREEN, -100, "large")
        message_to_screen("You died", BLACK, -30)

        button("PLAY AGAIN", 150, 400, 100, 50, DARKGREEN, GREEN, action = "play", pressed = click_pressed)
        button("CONTROLS", 350, 400, 100, 50, YELLOW, LIGHTYELLOW, action = "controls", pressed = click_pressed)
        button("EXIT", 550, 400, 100, 50, DARKRED, RED, action = "quit", pressed = click_pressed)

        pygame.display.update()
        clock.tick(15)

def you_win():
    win = True
    while win:
        gameDisplay.fill(WHITE)
        click_pressed = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                click_pressed = True

        message_to_screen("You won", DARKGREEN, -100, "large")
        message_to_screen("Congratulations", BLACK, -30)

        button("PLAY AGAIN", 150, 400, 100, 50, DARKGREEN, GREEN, action = "play", pressed = click_pressed)
        button("CONTROLS", 350, 400, 100, 50, YELLOW, LIGHTYELLOW, action = "controls", pressed = click_pressed)
        button("EXIT", 550, 400, 100, 50, DARKRED, RED, action = "quit", pressed = click_pressed)

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

def game_controls():
    control = True
    while control:
        gameDisplay.fill(WHITE)
        click_pressed = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                click_pressed = True

        message_to_screen("Controls", DARKGREEN, -100, "large")
        message_to_screen("Fire: Spacebar", BLACK, -30)
        message_to_screen("Move Turret: Up and Down arrows", BLACK, -10)
        message_to_screen("Move Tank: Left and Right arrows", BLACK, 10)
        message_to_screen("Decrease fire power: A", BLACK, 30)
        message_to_screen("Increase fire power: D", BLACK, 50)
        message_to_screen("Pause: P", BLACK, 70)

        if button("MAIN", 350, 400, 100, 50, YELLOW, LIGHTYELLOW, action = "main", pressed = click_pressed) == 1:
            control = False

        pygame.display.update()
        clock.tick(15)

def button(text, x, y, w, h, inactive_color, active_color, action = None, pressed = False):
    cur = pygame.mouse.get_pos()
    if x + w > cur[0] and x < cur[0] and y + h > cur[1] and y < cur[1]:
        pygame.draw.rect(gameDisplay, active_color, (x, y, w, h))
        if pressed and action != None:
            if action == "quit":
                pygame.quit()
                sys.exit()
            elif action == "controls":
                game_controls()
            elif action == "play":
                game_loop()
            elif action == "main":
                return 1
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, w, h))

    text_to_button(text, BLACK, x, y, w, h)
    return 0

def message_to_screen(msg, color, y_displace = 0, size = "small"):
    text_surface, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2, display_height / 2 + y_displace)
    gameDisplay.blit(text_surface, text_rect)

def tank(x, y, turret_pos):
    x = int(x)
    y = int(y)
    radius = int(tank_height / 2)

    '''possible_turrets = [(x - 27, y - 2),
                        (x - 26, y - 5),
                        (x - 25, y - 8),
                        (x - 23, y - 12),
                        (x - 20, y - 14),
                        (x - 18, y - 15),
                        (x - 15, y - 17),
                        (x - 13, y - 19),
                        (x - 11, y - 21)]'''

    possible_turrets = [(x - turret_length, y - 2)]
    # (x - cx) ** 2 + (y - cy) ** 2 = r ** 2
    for i in range(turret_length - 5):
        px = int(x - turret_length + (i + 1))
        py = int(-math.sqrt(turret_length ** 2 - (px - x) ** 2) + y)
        possible_turrets.append((px, py))

    pygame.draw.circle(gameDisplay, BLACK, (x, y), radius)
    pygame.draw.rect(gameDisplay, BLACK, (x - tank_height, y, tank_width, tank_height))

    pygame.draw.line(gameDisplay, BLACK, (x, y), possible_turrets[turret_pos], turret_width)

    max_wheels = int(tank_width / wheel_width)
    offset = 0
    wheel_x_coordinate_base = int(x - tank_height + wheel_width)
    wheel_y_coordinate_base = int(y + tank_height)
    for i in range(max_wheels - 1):
        pygame.draw.circle(gameDisplay, BLACK, (wheel_x_coordinate_base + offset, wheel_y_coordinate_base), wheel_width)
        offset += wheel_width
    return possible_turrets[turret_pos]

def enemy_tank(x, y, turret_pos):
    x = int(x)
    y = int(y)
    radius = int(tank_height / 2)

    possible_turrets = [(x + turret_length, y - 2)]
    # (x - cx) ** 2 + (y - cy) ** 2 = r ** 2
    for i in range(turret_length - 5):
        px = int(x + turret_length - (i + 1))
        py = int(-math.sqrt(turret_length ** 2 - (px - x) ** 2) + y)
        possible_turrets.append((px, py))

    pygame.draw.circle(gameDisplay, BLACK, (x, y), radius)
    pygame.draw.rect(gameDisplay, BLACK, (x - tank_height, y, tank_width, tank_height))

    pygame.draw.line(gameDisplay, BLACK, (x, y), possible_turrets[turret_pos], turret_width)

    max_wheels = int(tank_width / wheel_width)
    offset = 0
    wheel_x_coordinate_base = int(x - tank_height + wheel_width)
    wheel_y_coordinate_base = int(y + tank_height)
    for i in range(max_wheels - 1):
        pygame.draw.circle(gameDisplay, BLACK, (wheel_x_coordinate_base + offset, wheel_y_coordinate_base), wheel_width)
        offset += wheel_width
    return possible_turrets[turret_pos]

def barrier(x_location, random_height, barrier_width):
    pygame.draw.rect(gameDisplay, BLACK, (x_location, display_height - random_height, barrier_width, random_height))

def explosion(x, y, size = 50):
    pygame.mixer.Sound.play(explosion_sound)
    explode = True
    while explode:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        start_point = x, y
        color_choices = [DARKRED, RED, YELLOW, LIGHTYELLOW]
        magnitude = 1
        while magnitude < size:
            exploding_bit_x = x + random.randrange(-magnitude, magnitude)
            exploding_bit_y = y + random.randrange(-magnitude, magnitude)
            color_index = random.randrange(0, len(color_choices))
            exploding_bit_radius = random.randrange(1, 5)
            pygame.draw.circle(gameDisplay, color_choices[color_index], (exploding_bit_x, exploding_bit_y), exploding_bit_radius)
            magnitude += 1
            pygame.display.update()
            clock.tick(100)
        explode = False

def fire_shell(gun_xy, tank_x, tank_y, turret_pos, gun_power, barrier_x, barrier_h, barrier_w, e_tank_x, e_tank_y):
    pygame.mixer.Sound.play(fire_sound)
    fire = True
    damage = 0
    starting_shell = list(gun_xy)
    v0 = (50 * gun_power) / 50
    #print v0

    theta = math.atan2(gun_xy[1] - tank_y, gun_xy[0] - tank_x)
    vx = int(v0 * math.cos(theta))
    vy = int(v0 * math.sin(theta))
    g = 9.8
    t = 0

    while fire:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        #print starting_shell
        pygame.draw.circle(gameDisplay, DARKRED, starting_shell, 5)

        starting_shell[0] = int(gun_xy[0] + vx * t)
        starting_shell[1] = int(gun_xy[1] + vy * t + 0.5 * g * t * t)
        #print t, vx, vy, vx * t, vy * t + 0.5 * g * t * t, starting_shell
        t += 0.1

        #starting_shell[0] -= (12 - turret_pos) * 2
        #starting_shell[1] += int((((starting_shell[0] - gun_xy[0]) * 0.01) ** 2) - (turret_pos + turret_pos / (12 - turret_pos)))
        #print t, starting_shell[0], starting_shell[1]

        if starting_shell[1] > display_height - ground_height:
            # print "Last shell:", starting_shell
            # (x1 / y1) = (x2 / y2) => x1 = (x2 * y1) / y2
            # hit_x = int((starting_shell[0] * display_height) / starting_shell[1])
            # hit_y = int(display_height)
            # print "Impact:", v0, vx, vy, theta, gun_xy
            t_impact = (-vy + math.sqrt(vy ** 2 + 2 * ((display_height - ground_height) - gun_xy[1]) * g)) / g
            hit_y = int(display_height - ground_height)
            hit_x = int(gun_xy[0] + vx * t_impact)
            if e_tank_x + 10 > hit_x and e_tank_x - 10 < hit_x:
                print "P CRITICAL HIT"
                damage = 25
            elif e_tank_x + 15 > hit_x and e_tank_x - 15 < hit_x:
                print "P HARD HIT"
                damage = 18
            elif e_tank_x + 25 > hit_x and e_tank_x - 25 < hit_x:
                print "P MEDIUM HIT"
                damage = 10
            elif e_tank_x + 35 > hit_x and e_tank_x - 35 < hit_x:
                print "P LIGHT HIT"
                damage = 5
            explosion(hit_x, hit_y)
            fire = False

        check_x_1 = starting_shell[0] <= barrier_x + barrier_w
        check_x_2 = starting_shell[0] >= barrier_x
        check_y_1 = starting_shell[1] <= display_height
        check_y_2 = starting_shell[1] >= display_height - barrier_h

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            explosion(starting_shell[0], starting_shell[1])
            fire = False

        pygame.display.update()
        clock.tick(60)

    return damage

def enemy_fire_shell(gun_xy, tank_x, tank_y, turret_pos, gun_power, barrier_x, barrier_h, barrier_w, p_tank_x, p_tank_y):
    pygame.mixer.Sound.play(fire_sound)
    fire = True
    damage = 0
    starting_shell = list(gun_xy)
    #v0 = (50 * gun_power) / 50
    #print v0
    theta = math.atan2(gun_xy[1] - tank_y, gun_xy[0] - tank_x)
    g = 9.8
    t = 0
    v0 = int(math.sqrt(((p_tank_x - starting_shell[0]) * g) / math.sin(-2 * theta)))
    v0 = random.randrange(int(v0 * 0.9), int(v0 * 1.1)) # randomizing power (initial velocity) so that it is between 90% and 110%
    vx = int(v0 * math.cos(theta))
    vy = int(v0 * math.sin(theta))

    while fire:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        #print starting_shell
        pygame.draw.circle(gameDisplay, DARKRED, starting_shell, 5)

        starting_shell[0] = int(gun_xy[0] + vx * t)
        starting_shell[1] = int(gun_xy[1] + vy * t + 0.5 * g * t * t)
        #print t, vx, vy, vx * t, vy * t + 0.5 * g * t * t, starting_shell
        t += 0.1

        #starting_shell[0] -= (12 - turret_pos) * 2
        #starting_shell[1] += int((((starting_shell[0] - gun_xy[0]) * 0.01) ** 2) - (turret_pos + turret_pos / (12 - turret_pos)))
        #print t, starting_shell[0], starting_shell[1]

        if starting_shell[1] > display_height - ground_height:
            # print "Last shell:", starting_shell
            # (x1 / y1) = (x2 / y2) => x1 = (x2 * y1) / y2
            # hit_x = int((starting_shell[0] * display_height) / starting_shell[1])
            # hit_y = int(display_height)
            # print "Impact:", v0, vx, vy, theta, gun_xy
            t_impact = (-vy + math.sqrt(vy ** 2 + 2 * ((display_height - ground_height) - gun_xy[1]) * g)) / g
            hit_y = int(display_height - ground_height)
            hit_x = int(gun_xy[0] + vx * t_impact)
            if p_tank_x + 10 > hit_x and p_tank_x - 10 < hit_x:
                print "CRITICAL HIT"
                damage = 25
            elif p_tank_x + 15 > hit_x and p_tank_x - 15 < hit_x:
                print "HARD HIT"
                damage = 18
            elif p_tank_x + 25 > hit_x and p_tank_x - 25 < hit_x:
                print "MEDIUM HIT"
                damage = 10
            elif p_tank_x + 35 > hit_x and p_tank_x - 35 < hit_x:
                print "LIGHT HIT"
                damage = 5
            explosion(hit_x, hit_y)
            fire = False

        check_x_1 = starting_shell[0] <= barrier_x + barrier_w
        check_x_2 = starting_shell[0] >= barrier_x
        check_y_1 = starting_shell[1] <= display_height
        check_y_2 = starting_shell[1] >= display_height - barrier_h

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            explosion(starting_shell[0], starting_shell[1])
            fire = False

        pygame.display.update()
        clock.tick(60)
    return damage

def power(level):
    text = smallfont.render("Power: " + str(level) + "%", True, BLACK)
    gameDisplay.blit(text, [display_width / 2, 0])

def health_bars(player_health, enemy_health):
    if player_health > 75:
        player_health_color = DARKGREEN
    elif player_health > 50:
        player_health_color = YELLOW
    else:
        player_health_color = RED
        if player_health <= 1:
            player_health = 1

    if enemy_health > 75:
        enemy_health_color = DARKGREEN
    elif enemy_health > 50:
        enemy_health_color = YELLOW
    else:
        enemy_health_color = RED
        if enemy_health <= 1:
            enemy_health = 1

    pygame.draw.rect(gameDisplay, player_health_color, (680, 25, player_health, 25))
    pygame.draw.rect(gameDisplay, enemy_health_color, (20, 25, enemy_health, 25))

# Game loop
def game_loop():
    gameExit = False
    gameOver = False

    main_tank_x = display_width * 0.9
    main_tank_y = display_height * 0.9
    tank_move = 0

    current_tur_pos = 0
    change_tur = 0

    enemy_tank_x = display_width * 0.1
    enemy_tank_y = display_height * 0.9

    barrier_x = (display_width / 2) + random.randint(-0.1 * display_width, 0.1 * display_width)
    barrier_h = random.randrange(display_height * 0.1, display_height * 0.6)
    barrier_w = 50

    fire_power = 50
    power_change = 0

    player_health = 100
    enemy_health = 100

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
                    tank_move = -5
                elif event.key == K_RIGHT:
                    tank_move = 5
                elif event.key == K_UP:
                    change_tur = 1
                elif event.key == K_DOWN:
                    change_tur = -1
                elif event.key == K_p:
                    pause()
                elif event.key == K_SPACE:
                    damage = fire_shell(gun, main_tank_x, main_tank_y, current_tur_pos, fire_power, barrier_x, barrier_h, barrier_w, enemy_tank_x, enemy_tank_y)
                    enemy_health -= damage

                    possible_enemy_movements = ['f', 'r']
                    enemy_move_index = random.randrange(0, len(possible_enemy_movements))

                    for mov_i in range(random.randrange(0, 10)):
                        if display_width * 0.3 > enemy_tank_x and display_width * 0.03 < enemy_tank_x:
                            if possible_enemy_movements[enemy_move_index] == 'f':
                                enemy_tank_x += 5
                            elif possible_enemy_movements[enemy_move_index] == 'r':
                                enemy_tank_x -= 5

                            gameDisplay.fill(WHITE)
                            health_bars(player_health, enemy_health)
                            gun = tank(main_tank_x, main_tank_y, current_tur_pos)
                            enemy_gun = enemy_tank(enemy_tank_x, enemy_tank_y, current_tur_pos)

                            fire_power += power_change
                            if fire_power <= 0:
                                fire_power = 1
                            elif fire_power > 100:
                                fire_power = 100
                            power(fire_power)

                            barrier(barrier_x, barrier_h, barrier_w)
                            gameDisplay.fill(GREEN, rect = [0, display_height - ground_height, display_width, ground_height])

                            pygame.display.update()
                            clock.tick(FPS)

                    player_health -= enemy_fire_shell(enemy_gun, enemy_tank_x, enemy_tank_y, current_tur_pos, fire_power, barrier_x, barrier_h, barrier_w, main_tank_x, main_tank_y)
                elif event.key == K_a:
                    power_change = -1
                elif event.key == K_d:
                    power_change = 1

            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    tank_move = 0
                elif event.key == K_UP or event.key == K_DOWN:
                    change_tur = 0
                elif event.key == K_a or event.key == K_d:
                    power_change = 0

        main_tank_x += tank_move
        current_tur_pos += change_tur
        if current_tur_pos > 21:
            current_tur_pos = 21
        elif current_tur_pos < 0:
            current_tur_pos = 0

        if main_tank_x - tank_width / 2 < barrier_x + barrier_w:
            main_tank_x += 5

        gameDisplay.fill(WHITE)
        health_bars(player_health, enemy_health)
        gun = tank(main_tank_x, main_tank_y, current_tur_pos)
        enemy_gun = enemy_tank(enemy_tank_x, enemy_tank_y, current_tur_pos)

        fire_power += power_change
        if fire_power <= 0:
            fire_power = 1
        elif fire_power > 100:
            fire_power = 100
        power(fire_power)

        barrier(barrier_x, barrier_h, barrier_w)
        gameDisplay.fill(GREEN, rect = [0, display_height - ground_height, display_width, ground_height])

        pygame.display.update()

        if player_health < 1:
            game_over()
        elif enemy_health < 1:
            you_win()

        # Make the clock tick as per FPS rate set
        clock.tick(FPS)

    pygame.quit()
    # Instead of sys.exit(), we can use quit()
    sys.exit()

game_intro()