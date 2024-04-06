import pygame, random
from wall import Wall
from zombie import Zombie
from player import Player
from title import Title
from variables import *
 
pygame.init()

fullscreen = pygame.display.Info()

width, height = 720, 800
#width, height = fullscreen.current_w/2, fullscreen.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zombie Invaders")
clock = pygame.time.Clock()

posx, posy = int(width/128)*128 + ((width%128)/2), 90
font = pygame.font.SysFont("Comic Sans MS", 30)

intro_subtitle = pygame.image.load("Zombie Invaders/Images/Zombie invaders (4).png")
intro_subtitle = pygame.transform.scale(intro_subtitle, (width, 3*(height/4)))

tile_1 = Title("Zombie Invaders/Images/Zombie invaders.png", width, height, screen, 0, 0)
tile_2 = Title("Zombie Invaders/Images/Zombie invaders (1).png", width, height, screen, 1, 1)
tile_3 = Title("Zombie Invaders/Images/Zombie invaders (3).png", width, height, screen, 2, 2)
end_game_1 = Title("Zombie Invaders/Images/Zombie invaders (7).png", width, height, screen, 0, 80)
end_game_2 = Title("Zombie Invaders/Images/Zombie invaders (6).png", width, height, screen, 1, 90)
end_game_3 = Title("Zombie Invaders/Images/Zombie invaders (5).png", width, height, screen, 2, 100)

start = False
    
# Game

#background
background = pygame.image.load("Zombie Invaders/Images/Screenshot 2023-12-08 3.44.36 PM.png")
background = pygame.transform.scale(background, (width, height))

def wall_loops(posx, posy, last_walls, walls):
    for a in range(3):
        for i in range(int(width/128)):#width of image 
            posx -= 128
            walls.add(Wall(posx, posy, screen, levels, audio))
            last_walls += 1

        posy -= 30
        posx = int(width/128)*128 + ((width%128)/2)
    wall_amount = len(walls)
    return wall_amount, last_walls, walls
wall_amount, last_walls, walls = wall_loops(posx, posy, last_walls, walls)

konomi_code = 0

while True:
    #mouse
    mouse = pygame.mouse.get_pressed()
    #background
    screen.blit(background, (0,backgroundY))
    screen.blit(background, (0,backgroundY - height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pygame.quit()
                exit()
            
            if event.key == pygame.K_SPACE:
                start = True
            
            if event.key == pygame.K_m:
                # mute button
                if mute_button == False:
                    audio = False
                    pygame.mixer.music.pause()
                    mute_button = True
                else:
                    audio = True
                    pygame.mixer.music.unpause()
                    mute_button = False
            
            if event.key == pygame.K_UP:
                if konomi_code <= 2:
                    konomi_code += 1
                else:
                    konomi_code = 0
            if event.key == pygame.K_LEFT:
                if konomi_code == 4 or konomi_code == 6:
                    konomi_code += 1
                else:
                    konomi_code = 0
            if event.key == pygame.K_RIGHT:
                if konomi_code == 5 or konomi_code == 7:
                    konomi_code += 1
                else:
                    konomi_code = 0
            if event.key == pygame.K_DOWN:
                if konomi_code == 2 or konomi_code == 3:
                    konomi_code += 1
                else:
                    konomi_code = 0
            if event.key == pygame.K_1:
                if konomi_code == 8:
                    konomi_code += 1
                else:
                    konomi_code = 0
            if event.key == pygame.K_2:
                if konomi_code == 9:
                    konomi_code += 1
                else:
                    konomi_code = 0
        
    if level == 0:
        timer = 0
        offscreen = tile_1.move(start, "Up-Down")
        tile_2.move(start, "Up-Down")
        tile_3.move(start, "Up-Down")

        if start == True:
            if music and audio:
                pygame.mixer.music.load("Zombie Invaders/music/item-obtained-123644.mp3")
                pygame.mixer.music.play()
                music = False
            if offscreen == True:
                if konomi_code == 10:
                    projectile_timer = 0
                player = Player(screen, width, height, projectile_timer, 2, extra_lives, audio)
                level += 1
                if audio:
                    pygame.mixer.music.load("Zombie Invaders/music/item-obtained-123644.mp3")
                    pygame.mixer.music.play(1, 3)
                music = True
        else:
            screen.blit(intro_subtitle, (0,(height/3)))

        if mouse[0]:
            start = True

    elif level == 1:        
        wall = pygame.sprite.Group.sprites(walls)
        
        if timer == random_spawn:
            try:
                rand_wall = random.randint(0, len(wall) - 1)
                if levels >= 2:
                    rand_zig_zag = random.randint(0, 1)
                else:
                    rand_zig_zag = 1
                zombies.add(Zombie(wall[rand_wall], height, width, screen, (levels/5) - 1, int(speed), zig_zag[rand_zig_zag], audio))
                timer = 0
                last_zombies += 1
            #ending
            except:
                levels += 1
                level += 1
                zombies_killed = 0
                timer = 0
                random_spawn = random.randint(spawn_rate, spawn_rate + 10)
        
        for i in range(len(wall)):
            if wall[i].rect.x <= 0: 
                wall_direction = "Right"
                no_move = True
            
            if wall[i].rect.x + wall[i].rect.width >= width:
                wall_direction = "Left"
                no_move_p2 = True
            
            if no_move and no_move_p2: 
                wall_direction = "None"
                no_move = False
                no_move_p2 = False
                
        no_move = False
        no_move_p2 = False

        #objects
        # pygame.sprite.Group.update(zombies, projectiles)
        for zombie in zombies:
            zdeath = zombie.update(projectiles)
            if len(zombies) < last_zombies:
                if zdeath == False:
                    zombies_killed += 1
                    points += 1
                last_zombies -= 1
        
        pygame.sprite.Group.update(walls, projectiles, wall_direction, zombies_killed)
        pygame.sprite.Group.update(projectiles)
        pygame.sprite.Group.update(extra_lives)
        death = player.update(zombies, projectiles, extra_lives)

        score = font.render("Score: " + str(points) , False, "White")
        screen.blit(score, (0,0))
            
        if len(walls) < last_walls:
            points += 1
            zombies_killed += 1
            last_walls -= 1
        
        if death == True:
            level = -1
            if audio:
                pygame.mixer.music.load("Zombie Invaders/music/game-over-8-bit-chiptune-164330.mp3")
        
        if zombies_killed >= 5 + levels and levels >= 2:
            if levels % 2 == 0:
                if music and audio:
                    pygame.mixer.music.load("Zombie Invaders/music/chiptune-grooving-142242.mp3")
                    pygame.mixer.music.play(1, 1)
                    music = False
            else:
                if music and audio:
                    pygame.mixer.music.load("Zombie Invaders/music/item-obtained-123644.mp3")
                    pygame.mixer.music.play(1, 3)
                    music = False
        
        if pygame.mixer.music.get_busy() == False and audio:
            pygame.mixer.music.play()
        
    elif level == 2:
        level_display = font.render("Level " + str(levels), False, "White")
        screen.blit(level_display, (width/2 - 45, height/3))
        if timer == 120:
            wall_amount, last_walls, walls = wall_loops(posx, posy, 0, walls)
            zombies = pygame.sprite.Group()
            level -= 1
            speed += 1/5
            if spawn_rate >= 10:
                spawn_rate -= 2
            timer = 0
            music = True
    
    else:
        start = False

        # game over sign
        end_game_1.move(start, "Up-Down")
        end_game_2.move(start, "Up-Down")
        end_game_3.move(start, "Up-Down")

        # game over subtitles
        score = font.render("Final Score: " + str(points) , False, "White")
        exit_text = font.render('Exit the game to retry', False, "White")
        exit_button = font.render("Press: P", False, "White")
        credits1 = font.render("Halen: Game Creator", False, "green3")
        credits2 = font.render("Nitin: Code Helper", False, "aqua")
        credits3 = font.render("Joseph: Image Creator", False, "darkgoldenrod1")
        music = font.render("pixel-perfect: Lesiakower, item-obtained: Lesiakower, chiptune-grooving: K00sin, gamboy-pluck: Pixabay, game-over-(8-bit-chiptune): Moonwalk1", False, "magenta2")
        music_background = font.render("pixel-perfect: Lesiakower, item-obtained: Lesiakower, chiptune-grooving: K00sin, gamboy-pluck: Pixabay, game-over-(8-bit-chiptune): Moonwalk1", False, "black")
        screen.blit(score, (width/2 - 94, 2*(height/3)))
        screen.blit(exit_text, (width/2 - 158, 2*(height/3) + 32))
        screen.blit(exit_button, (width/2 - 58, 2*(height/3) + 64))
        screen.blit(credits1, (width/2 - 144, 2*(height/3) + 96))
        screen.blit(credits2, (width/2 - 132, 2*(height/3) + 128))
        screen.blit(credits3, (width/2 - 158, 2*(height/3) + 160))
        screen.blit(music_background, (width - music_xpos - 2, 2*(height/3) + 192))
        screen.blit(music, (width - music_xpos, 2*(height/3) + 192))

        # move music creaters along screen
        if music_xpos > width + 2000:
            music_xpos = 0
        music_xpos += 5

        # game over music repeat
        if pygame.mixer.music.get_busy() == False and audio:
            pygame.mixer.music.play()
    
    if zombies_killed <= 5 + levels:
        backgroundY += 2
    else:
        if backgroundY != 0:
            backgroundY += 5    
    
    if backgroundY >= height:
        backgroundY = 0

    timer += 1
    
    pygame.display.update()
    clock.tick(60)