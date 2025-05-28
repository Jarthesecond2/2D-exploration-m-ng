import pygame

class ShopNPC:
    def __init__(self, x, y, width=40, height=60, color=(150, 75, 0)):
        
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.items_for_sale = ["Mängu lõpp"]
        self.is_open = False
                 
    def draw(self, screen):
        pygame.draw.rect(screen, self.color , self.rect)
    
    def is_near_player(self, player_rect):
        return self.rect.colliderect(player_rect)