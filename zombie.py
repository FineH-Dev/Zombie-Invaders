import pygame, random

class Zombie(pygame.sprite.Sprite):
    def __init__(self, wall, height, width, screen, life, speed, zig_zag, audio):
        self.wall = wall
        self.height = height
        self.width = width
        super().__init__()
        self.image = pygame.image.load("Zombie Invaders/Images/pixil-frame-0 (3).png").convert_alpha()
        self.pos = pygame.math.Vector2(random.randint(0 + wall.rect.x, wall.rect.width - self.image.get_width() + wall.rect.x), wall.rect.y + wall.rect.height)
        self.zrect = self.image.get_rect(topleft = self.pos)
        self.screen = screen
        self.speed = random.randint(speed-1, speed)
        self.life = life
        self.zig_zag = zig_zag
        self.xpos = 0
        if zig_zag == False:
            self.direction = "none"
        else:
            direction = ["Left", "Right"]
            chance = random.randint(0, 1)
            self.direction = direction[chance]
            if self.direction == "Left":
                self.image = pygame.transform.rotate(self.image, -45)
            else:
                self.image = pygame.transform.rotate(self.image, 45)
        
        # sound
        self.audio = audio

    def move(self):
        if self.zrect.y >= self.height - self.zrect.height:  
            self.kill()

        if self.zig_zag == True:
            if self.zrect.x + self.zrect.width >= self.width:
                self.direction = "Left"
                self.image = pygame.transform.rotate(self.image, -90)
            if self.zrect.x <= 0:
                self.direction = "Right"
                self.image = pygame.transform.rotate(self.image, 90)
        
        if self.direction == "Left":
            self.zrect.move_ip(-self.speed-1, 0) 
        elif self.direction == "Right":
            self.zrect.move_ip(self.speed+1, 0)
        else:
            self.xpos = 0
        
        self.zrect.move_ip(0, self.speed)
        self.screen.blit(self.image, (self.zrect.x, self.zrect.y))
    
    def hit(self, projectiles):
        projectile = pygame.sprite.Group.sprites(projectiles)
        for bullet in projectile:
            
            # projectile xpos within zombie xpos
            if self.zrect.x + self.zrect.width> bullet.rect.x and self.zrect.x < bullet.rect.x + bullet.rect.width:
                
                # projectile ypos within zombie ypos
                if self.zrect.y + self.zrect.height > bullet.rect.y and self.zrect.y < bullet.rect.y + bullet.rect.height:
                    bullet.kill()
                    if self.audio:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("Zombie Invaders/music/gameboy-pluck-41265.mp3"))
                    if self.life <= 0:
                        self.kill()
                        return False
                    self.life -= 1
    
    def update(self, projectiles):
        self.move()
        return self.hit(projectiles)