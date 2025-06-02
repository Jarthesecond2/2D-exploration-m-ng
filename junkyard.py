import pygame

class Junkyard:
    def __init__(self, x, y, width=60, height=80, color=(100, 50, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def is_near_player(self, player_rect):
        return self.rect.colliderect(player_rect)
