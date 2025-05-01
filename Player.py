"""Player"""

import pygame

class Player:
    def __init__(self, x, y, width=40, height=40, color=(0, 100, 255), speed=4):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed
                 
    def handle_movement(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)