import pygame
import random
from settings import Settings
from Player import Player
from trash_can import TrashCan
from inventory import Inventory
from utils import search_trash_can

class Game:
    def __init__(self):
        self.settings = Settings()
        self.scale = 1.0
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width, self.settings.screen_height = self.screen.get_size()
        pygame.display.set_caption(self.settings.caption)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.large_font = pygame.font.SysFont(None, 50)
            
        self.player = Player(100, 100, 40, 40, 4)
        self.trash_cans = [
            TrashCan(200, 150),
            TrashCan(500, 400),
            TrashCan(300, 250),
        ]
        self.message = ""
        self.inventory = Inventory(max_items=24, font=self.font, scale=self.scale)
        self.last_search_time = 0
        self.cooldown = 1000
        self.inventory_open = False
        self.fullscreen = True


    def draw_play_button(self):
        self.screen.fill((0, 200, 0))
        button_rect = pygame.Rect(
            self.settings.screen_width // 2 - 100,
            self.settings.screen_height // 2 - 30,
            200,
            60
        )
        pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
        text = self.large_font.render("Play", True, (50, 50, 50))
        self.screen.blit(
            text,
            (
                button_rect.x + (button_rect.width - text.get_width()) // 2,
                button_rect.y + (button_rect.height - text.get_height()) // 2
            )
        )
        pygame.display.flip()
        return button_rect


    def wait_for_play(self):
        waiting = True
        while waiting:
            button_rect = self.draw_play_button()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse click at:", event.pos)
                    if button_rect.collidepoint(event.pos):
                        print("Play button clicked!")
                        waiting = False
            pygame.time.delay(50)
                    
                    
    def run(self):
        self.wait_for_play()
        print("Game loop starting...")
        running = True
        while running:
            self.clock.tick(60)
            self.screen.fill((0, 200, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        self.inventory_open = not self.inventory_open
                    elif event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((800, 600))
                        self.settings.screen_width, self.settings.screen_height = self.screen.get_size()
                        self.scale = self.settings.screen_width / 800.0
                        self.rescale_objects()

            keys = pygame.key.get_pressed()
            self.player.handle_movement(keys)

            if keys[pygame.K_e]:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_search_time >= self.cooldown:
                    for can in self.trash_cans:
                        if self.player.rect.colliderect(can):
                            item = search_trash_can()
                            self.message = f"You found: {item}"
                            if item != "Nothing":
                                self.inventory.add_item(item)
                            self.last_search_time = current_time
                            break

            self.player.draw(self.screen)

            for can in self.trash_cans:
                can.draw(self.screen)

            message_surface = self.font.render(self.message, True, (0, 0, 0))
            self.screen.blit(message_surface, (20, 20))

            if self.inventory_open:
                center_x = self.settings.screen_width // 2
                center_y = self.settings.screen_height // 2
                self.inventory.draw_menu(self.screen, center_x, center_y)
            
            pygame.display.flip()
    
    def rescale_objects(self):
        new_size = int(40 * self.scale)
        self.player.rect.width = new_size
        self.player.rect.height = new_size
        self.player.speed = int(4 * self.scale)
        
        for can in self.trash_cans:
            can.rect.width = new_size
            can.rect.height = new_size
            
        new_font_size = int(30 * self.scale)
        self.font = pygame.font.SysFont(None, new_font_size)
        self.large_font = pygame.font.SysFont(None, int(50 * self.scale))
        self.inventory.font = self.font

        pygame.display.flip()