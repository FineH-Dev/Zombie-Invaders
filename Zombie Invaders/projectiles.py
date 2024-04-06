import pygame, math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen, xpos, ypos, player_angle):
        super().__init__()
        speed = 10
        self.screen = screen
        self.angle = player_angle
        self.x = math.sin(self.angle * (math.pi/180)) * speed
        self.y = -math.cos(self.angle * (math.pi/180)) * speed
        self.pos = pygame.math.Vector2(xpos, ypos)
        self.image = pygame.image.load("Zombie Invaders/Images/pixil-frame-0 (8).png").convert_alpha()
        self.og_image = self.image
        self.rect = self.image.get_rect(topleft = self.pos)

    def rotation(self):
        self.image = pygame.transform.rotate(self.og_image, -self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
    
    def update(self):
        self.rotation()
        self.rect.move_ip(self.x, self.y)
        if self.rect.y < 0:
            self.kill()
        
        self.screen.blit(self.image, (self.rect.x, self.rect.y))