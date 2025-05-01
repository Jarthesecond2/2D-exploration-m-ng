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
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Homeless Simulator")

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
        self.inventory = Inventory(font=self.font)
        self.last_search_time = 0
        self.cooldown = 1000


    def search_trash_can(self):
        roll = random.randint(1, 100)
        if roll <= 15:
            return "Bottle"
        elif roll <= 74:
            return "Trash"
        elif roll <= 75:
            return "Token"
        else:
            return "Nothing"

    def draw_play_button(self):
        self.screen.fill((0, 200, 0))
        button_rect = pygame.Rect(self.settings.screen_width // 2 - 100, self.settings.screen_height // 2 - 30, 200, 60)
        pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
        text = self.large_font.render("Play", True, (50, 50, 50))
        self.screen.blit(text, (button_rect.x + (button_rect.width - text.get_width()) // 2,
                                button_rect.y + (button_rect.height - text.get_height()) // 2))
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
                elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                    waiting = False
                    
                    
    def run(self):
        self.wait_for_play()
        running = True
        while running:
            self.clock.tick(60)
            self.screen.fill((0, 200, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.player.handle_movement(keys)

            if keys[pygame.K_e]:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_search_time >= self.cooldown:
                    for can in self.trash_cans:
                        if self.player.rect.colliderect(can):
                            item = self.search_trash_can()
                            self.message = f"You found: {item}"
                            self.inventory.add_item(item)
                            self.last_search_time = current_time
                            break

            self.player.draw(self.screen)

            for can in self.trash_cans:
                can.draw(self.screen)

            message_surface = self.font.render(self.message, True, (0, 0, 0))
            self.screen.blit(message_surface, (20, 20))

            self.inventory.draw(self.screen)

            pygame.display.flip()