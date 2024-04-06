import pygame
from projectiles import Projectile
from extra_lives import Extra_lives

#blueprint for player
class Player:
    # initalized variables
    def __init__(self, screen, width, height, projectile_timer, lives, extra_lives, audio):
        # windows settings
        self.screen = screen
        self.screen_width = width
        # sound
        pygame.mixer.init()
        self.audio = audio
        
        # player image: rectangle + original position
        self.image = pygame.image.load("Zombie Invaders/Images/pixil-frame-0 (7).png").convert_alpha()
        self.og_image = self.image
        self.og_rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(width/2 - self.og_rect.width/2, height - self.og_rect.height/2)
        self.rect = self.image.get_rect(center = self.pos)
        
        # lives counter
        self.lives = lives
        
        for i in range(lives):
            extra_lives.add(Extra_lives(width, height, screen, i))
        
        # bullet spawning settings
        self.projectile_timer = projectile_timer
        self.og_timer = projectile_timer
        self.shooting = True
        self.offset = pygame.math.Vector2(-10, -150)
        self.angle = 0
    
    # inputs
    def inputs(self, projectiles):
        
        # keboard and mouse
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        
        #move player left
        if keys[pygame.K_a]: 
            if self.rect.x >= 0: 
                self.rect.move_ip(int(-self.screen_width/64), 0)
                self.angle = -20
            
        #move player right
        if keys[pygame.K_d]:
            if self.rect.x <= self.screen_width - self.rect.width:  
                self.rect.move_ip(int(self.screen_width/64), 0)
                self.angle = 20

        # shoot projectiles/ bullets, where and when
        if keys[pygame.K_SPACE] or mouse[0]:
            if self.projectile_timer <= 0 and self.shooting == True:
                spawn_pos = self.rect.center + self.offset.rotate(self.angle)
                projectiles.add(Projectile(self.screen, spawn_pos[0], spawn_pos[1], self.angle))
                if self.audio:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("Zombie Invaders/music/mixkit-short-laser-gun-shot-1670.wav"))
                # restarts peramiters.
                self.projectile_timer = self.og_timer
                if self.projectile_timer > 0:
                    self.shooting = False
        
        #timer for shooting
        if keys[pygame.K_SPACE] == False and mouse[0] == False:
            self.shooting = True
        
        self.projectile_timer -= 1
    
    def rotation(self):
        # mouse_xpos, mouse_ypos = pygame.mouse.get_pos()
        # rel_x, rel_y = mouse_ypos - self.rect.centery, mouse_xpos - self.rect.centerx
        # self.angle = math.degrees(math.atan2(rel_x, rel_y)) + 90
        # if self.angle >= 45:
        #     self.angle = 45
        #     self.image = pygame.transform.rotate(self.og_image, -self.angle)
        # elif self.angle <= -45:
        #     self.angle = -45
        #     self.image = pygame.transform.rotate(self.og_image, -self.angle)
        # else:
        #     self.angle = 0
        self.image = pygame.transform.rotate(self.og_image, -self.angle)
        self.angle = 0

        #self.image = pygame.transform.rotate(self.og_image, -self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
    
    def hit(self, zombies, extra_lives):
        extra_lives = pygame.sprite.Group.sprites(extra_lives)
        for zombie in zombies:
            
            # player xpos within zombie xpos
            if self.rect.x + self.rect.width> zombie.zrect.x and self.rect.x < zombie.zrect.x + zombie.zrect.width:
                
                # player ypos within zombie ypos
                if self.rect.y + self.rect.height > zombie.zrect.y and self.rect.y < zombie.zrect.y + zombie.zrect.height:
                    self.lives -= 1
                    if self.lives < 0:
                        return True
                    zombie.kill()
                    extra_lives[len(extra_lives)-1].kill()
    
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
            
    def update(self, zombies, projectiles, extra_lives):
        self.inputs(projectiles)
        self.rotation()
        return self.hit(zombies, extra_lives)