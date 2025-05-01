"""Inventory"""

import pygame

class Inventory:
    def __init__(self, max_items=10, font=None):
        self.items = []
        self.max_items = max_items
        self.font = font or pygame.font.SysFont(None, 30)

    def add_item(self, item):
        if len(self.items) < self.max_items:
            self.items.append(item)
            return True
        return False

    def draw(self, screen, x=20, y=50):
        display_items = ", ".join(self.items[-5:])
        text = self.font.render("Inventory: " + display_items, True, (0, 0, 0))
        screen.blit(text, (x, y))
