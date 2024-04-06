import pygame

class Wall(pygame.sprite.Sprite):

    def __init__(self, posx, posy, screen, levels, audio):
        super().__init__()
        self.moves = True
        self.pos = pygame.math.Vector2(posx, posy)
        self.screen = screen
        self.speed = 0
        self.image = pygame.image.load("Zombie Invaders/Images/pixil-frame-0 (4).png").convert_alpha()
        self.rect = self.image.get_rect(topleft = self.pos)
        self.life = int(levels/2)
        self.levels = levels

        # sound
        self.audio = audio

    def move(self, direction, zombies_killed):
        if zombies_killed >= 5 + self.levels:
            if self.rect.y < self.pos.y:
                if self.speed % 2 == 0:
                    self.rect.move_ip(0, 1)
            else: 
                if direction == "Right":    self.rect.move_ip(1, 0)
                if direction == "Left":    self.rect.move_ip(-1, 0)
        else:
            self.rect.y = self.pos.y - (3*self.rect.height) - self.rect.height

        self.speed += 1
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        
    def hit(self, projectiles):
        
        projectile = pygame.sprite.Group.sprites(projectiles)
        for i in range(len(projectile)):
            
            # projectile xpos within zombie xpos
            if self.rect.x + self.rect.width> projectile[i].rect.x and self.rect.x < projectile[i].rect.x + projectile[i].rect.width:
                
                # projectile ypos within zombie ypos
                if self.rect.y + self.rect.height > projectile[i].rect.y and self.rect.y < projectile[i].rect.y + projectile[i].rect.height:
                    projectile[i].kill()
                    if self.life == 0:
                        self.kill()
                    else:
                        self.image = pygame.image.load("Zombie Invaders/Images/pixil-frame-0 (6).png").convert_alpha()
                    self.life -= 1
                    if self.audio:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("Zombie Invaders/music/gameboy-pluck-41265.mp3"))
    
    def update(self, projectiles, direction, zombies_killed):
        self.move(direction, zombies_killed)
        self.hit(projectiles)