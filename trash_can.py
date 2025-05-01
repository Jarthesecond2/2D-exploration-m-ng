"""Trash Can"""

import pygame

class TrashCan:
    def __init__(self, x, y, width=40, height=40, color=(100, 100, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def is_colliding_with(self, player_rect):
        return self.rect.colliderect(player_rect)
