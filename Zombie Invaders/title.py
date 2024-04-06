import pygame

class Title:
    def __init__(self, image, width, height, screen, a, size):
        self.image = pygame.transform.scale(pygame.image.load(image), (width + size*4, 3*(height/4)))
        self.acceleration_y = a
        self.a = a
        self.size = size
        self.ypos = -height/7
        self.xpos = 0
        self.height = height
        self.width = width
        self.screen = screen
        self.vel = 1
    
    def move(self, start, direction):
        if direction == "Up-Down":
            if start == False:
                if self.ypos < self.height/100:    self.acceleration_y += 1
                else:   self.acceleration_y -= 1
            else:
                self.acceleration_y -= 1
                
            self.ypos += self.acceleration_y
            
            if self.ypos + self.height < 0:
                return True
                
        if direction == "Left-Right":
            if self.xpos > self.width/12:   self.vel = -1
            if self.xpos < -self.width/12:  self.vel = 1
            self.xpos += self.vel
            
        self.screen.blit(self.image, (self.xpos - self.size*2,self.ypos))