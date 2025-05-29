"""Player"""

import pygame

class Player:
    def __init__(self, x, y, width=512, height=512, speed=4):
        self.speed = speed
        self.image = pygame.image.load("assets/character.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
                 
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
        screen.blit(self.image, self.rect)

    def rescale(self, width, height):
        self.image = pygame.image.load("assets/character.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        self.player.rescale(240, 240)
