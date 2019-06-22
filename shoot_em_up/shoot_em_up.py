import pygame, random
from pygame.locals import *
from os import path

# folders
img_dir = path.join(path.dirname(__file__), 'img')
sound_dir = path.join(path.dirname(__file__), 'sound')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (200, 200, 0)

# initialization
pygame.init()
pygame.mixer.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot-em up!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surf = font.render(text, True, WHITE)
	text_rect = text_surf.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surf, text_rect)

def spawn_new_mob():
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)

def draw_shield_bar(surf, x, y, percent):
	if percent < 0:
		percent = 0

	BAR_LENGTH = 100
	BAR_HEIGHT = 10
	FILL_COLOR = GREEN
	if percent < 66 and percent >= 33:
		FILL_COLOR = YELLOW
	elif percent < 33:
		FILL_COLOR = RED

	fill_percent = (percent * BAR_LENGTH) / 100
	outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	filled_rect = pygame.Rect(x, y, fill_percent, BAR_HEIGHT)
	pygame.draw.rect(surf, FILL_COLOR, filled_rect)
	pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 30 * i
		img_rect.y = y
		surf.blit(img, img_rect)

def show_go_screen():
	display.blit(background, background_rect)
	draw_text(display, "Shoot-em up!", 64, WIDTH / 2, HEIGHT / 4)
	draw_text(display, "Left / Right arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
	draw_text(display, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 0.75)
	pygame.display.flip()
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYUP:
				waiting = False
		clock.tick(FPS)

# Player is derived class from base class pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
	# constructor
	def __init__(self):
		# call the base class constructor
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.transform.scale(player_img, (50, 38))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 20
		# pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.x_speed = 0
		self.shield = 100
		self.shoot_delay = 250	# in milliseconds
		self.last_shot = pygame.time.get_ticks()
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()
		self.power = 1
		self.power_timer = pygame.time.get_ticks()

	# override update function
	def update(self):
		# timeout for powerups
		if self.power >= 2 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
			self.power -= 1
			self.power_time = pygame.time.get_ticks()

		# unhide if hidden
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = WIDTH / 2
			self.rect.bottom = HEIGHT - 10

		self.x_speed = 0
		keys_state = pygame.key.get_pressed()

		if keys_state[K_LEFT]:
			self.x_speed = -5
		if keys_state[K_RIGHT]:
			self.x_speed = 5
		if keys_state[K_SPACE]:
			self.shoot()

		self.rect.x += self.x_speed
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def powerup(self):
		self.power += 1
		self.power_timer = pygame.time.get_ticks()

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			if self.power == 1:
				bullet = Bullet(self.rect.centerx, self.rect.top)
				all_sprites.add(bullet)
				bullets.add(bullet)
				shoot_sound.set_volume(0.5)
				shoot_sound.play()
			elif self.power >= 2:
				bullet1 = Bullet(self.rect.left, self.rect.centery)
				bullet2 = Bullet(self.rect.right, self.rect.centery)
				all_sprites.add(bullet1)
				all_sprites.add(bullet2)
				bullets.add(bullet1)
				bullets.add(bullet2)
				shoot_sound.set_volume(0.5)
				shoot_sound.play()

	def hide(self):
		# hide the player temporarily
		self.hidden = True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image_orig = random.choice(meteor_imgs)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width  * 0.85 / 2)
		# pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
		self.rect.x = random.randrange(0, WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.y_speed = random.randrange(1, 8)
		self.x_speed = random.randrange(-3, 3)
		self.rot = 0	# rotation
		self.rot_speed = random.randrange(-8, 8)
		self.last_update = pygame.time.get_ticks()

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rot = (self.rot + self.rot_speed) % 360
			new_image = pygame.transform.rotate(self.image_orig, self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.rotate()
		self.rect.x += self.x_speed
		self.rect.y += self.y_speed

		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(0, WIDTH - self.rect.width)
			self.rect.y = random.randrange(-150, -100)
			self.y_speed = random.randrange(1, 8)
			self.x_speed = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = laser_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.y_speed = -10

	def update(self):
		self.rect.y += self.y_speed
		# kill it if it moves off the top of the screen
		if self.rect.bottom < 0:
			# remove the sprites from all groups
			self.kill()

class Pow(pygame.sprite.Sprite):
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
		self.type = random.choice(['shield', 'gun'])
		self.image = powerup_images[self.type]
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.y_speed = 4

	def update(self):
		self.rect.y += self.y_speed
		# kill it if it moves off the top of the screen
		if self.rect.top > HEIGHT:
			# remove the sprites from all groups
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center, size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_anim[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 75

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

# load all game graphics
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
player_img_mini = pygame.transform.scale(player_img, (25, 19))
player_img_mini.set_colorkey(BLACK)

meteor_imgs = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_tiny1.png']
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
for img in meteor_list:
	meteor_imgs.append(pygame.image.load(path.join(img_dir, img)).convert())

laser_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(1,9):
	file_name = 'explosion{}.png'.format(i)
	img = pygame.image.load(path.join(img_dir, file_name)).convert()
	img.set_colorkey(WHITE)
	img_lg = pygame.transform.scale(img, (75, 75))
	explosion_anim['lg'].append(img_lg)
	img_sm = pygame.transform.scale(img, (32, 32))
	explosion_anim['sm'].append(img_sm)
	if i < 6:
		file_name = 'ship_explosion{}.png'.format(i)
		img = pygame.image.load(path.join(img_dir, file_name)).convert()
		img.set_colorkey(WHITE)
		explosion_anim['player'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

# load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(sound_dir, 'fire.wav'))
explosion_sound = pygame.mixer.Sound(path.join(sound_dir, 'explosion.wav'))

# game loop
running = True
game_over = True

while running:
	if game_over:
		show_go_screen()
		game_over = False
		# sprites group
		all_sprites = pygame.sprite.Group()
		mobs = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		powerups = pygame.sprite.Group()
		player = Player()
		all_sprites.add(player)
		for i in range(8):
			spawn_new_mob()

		score = 0

	# event handler
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

	# update sprite group
	all_sprites.update()

	# check to see if a bullet hit a mob
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
	for hit in hits:
		score += 50 - hit.radius
		explosion_sound.set_volume(hit.radius / 50.0)
		explosion_sound.play()
		expl = Explosion(hit.rect.center, 'lg')
		all_sprites.add(expl)
		if random.random() > 0.9:
			pu = Pow(hit.rect.center)
			all_sprites.add(pu)
			powerups.add(pu)
		spawn_new_mob()

	# check to see if a mob hit the player
	hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
	for hit in hits:
		player.shield -= hit.radius * 2
		expl = Explosion(hit.rect.center, 'sm')
		all_sprites.add(expl)
		spawn_new_mob()
		if player.shield <= 0:
			explosion_sound.set_volume(0.9)
			explosion_sound.play()
			death_explosion = Explosion(player.rect.center, 'player')
			all_sprites.add(death_explosion)
			player.hide()
			player.lives -= 1
			player.shield = 100

	# check to see if player hit a powerup
	hits = pygame.sprite.spritecollide(player, powerups, True)
	for hit in hits:
		if hit.type == 'shield':
			player.shield += random.randrange(10, 30)
			if player.shield >= 100:
				player.shield = 100
		elif hit.type == 'gun':
			player.powerup()

	# if the player died and the explosion has finished playing
	if player.lives == 0 and not death_explosion.alive():
		game_over = True

	# draw / render
	display.fill(BLACK)
	display.blit(background, background_rect)
	all_sprites.draw(display)
	draw_text(display, str(score), 18, WIDTH / 2, 10)
	draw_shield_bar(display, 5, 5, player.shield)
	draw_lives(display, WIDTH - 100, 5, player.lives, player_img_mini)

	# after drawing everything, flip (or update) display
	pygame.display.flip()

	# keep game loop at right speed
	clock.tick(FPS)

pygame.quit()
quit()