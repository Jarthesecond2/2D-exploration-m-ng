"""Inventory"""

import pygame
import os

class Inventory:
    def __init__(self, max_items=10, font=None, scale=1.0):
        self.items = []
        self.max_items = max_items
        self.font = font or pygame.font.SysFont(None, 30)
        self.scale = scale
        
        
        self.icons = {
            "Bottle": pygame.image.load(os.path.join("assets", "bottle.png")).convert_alpha(),
            "Trash": pygame.image.load(os.path.join("assets", "trash.png")).convert_alpha(),
            "Token": pygame.image.load(os.path.join("assets", "token.png")).convert_alpha()
        }

    def add_item(self, item):
        if len(self.items) < self.max_items:
            self.items.append(item)
            return True
        return False

    def draw_menu(self, screen, center_x, center_y):
        slot_width = int(60 * self.scale)
        slot_height = int(60 * self.scale)
        margin = int(10 * self.scale)
        cols = 6
        rows = 4
        total_width = cols * slot_width + (cols - 1) * margin
        total_height = rows * slot_height + (rows - 1) * margin
        start_x = center_x - total_width // 2
        start_y = center_y - total_height // 2
        
        for i in range(self.max_items):
            row = i // cols
            col = i % cols
            x = start_x + col * (slot_width + margin)
            y = start_y + row * (slot_height + margin)
            
            pygame.draw.rect(screen, (200, 200, 200), (x, y, slot_width, slot_height))


            if i < len(self.items):
                item_name = self.items[i]
                icon = self.icons.get(item_name)
                if icon:
                    icon = pygame.transform.scale(icon, (int(40 * self.scale), int(40 * self.scale)))
                    screen.blit(icon, (x + 10, y + 10))
                else:
                    item_text = self.font.render(item_name, True, (0, 0, 0))
                    screen.blit(item_text, (x + 5, y + 20))