import pygame

class Extra_lives(pygame.sprite.Sprite):
    def __init__(self, width, height, screen, live_num):
        super().__init__()
        self.image = pygame.image.load("Zombie Invaders/Images/pixil-frame-0 (7).png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width/10, height/10))
        #self.image = self.image.pygam
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = (0 + (self.rect.width*live_num), height - self.rect.height)
        self.screen = screen
    
    def update(self):
        self.screen.blit(self.image, self.pos)