import pygame, random

# trasnistion between scenes
level = 0
# level count
levels = 1

# player start game + extra lives group
extra_lives = pygame.sprite.Group()
start = False

# background start
backgroundY = 0

# walls counter + sprite group
walls = pygame.sprite.Group()
last_walls = 0

# wall direction + checks
wall_direction = "Right"
no_move = False
no_move_p2 = False

# zombie group and track how many killed
zombies = pygame.sprite.Group()
zombies_killed = 0
last_zombies = 0

# spawn rate
spawn_rate = 110
random_spawn = random.randint(spawn_rate, 120)
# zombie og speed + zig zag
speed = 3
zig_zag = [True, False]

# point counter
points = 0

# projectile group + timer
projectiles = pygame.sprite.Group()
projectile_timer = 20

# projectile direction
direction = "None"

# timer
timer = 0

#audio on or off
audio = True # True: on # False: off
mute_button = False

# music
pygame.mixer.init()
if audio:
    pygame.mixer.music.load("Zombie Invaders/music/pixel-perfect-112527.mp3")
    pygame.mixer.music.play()
music = True

# Game over
music_xpos = 0