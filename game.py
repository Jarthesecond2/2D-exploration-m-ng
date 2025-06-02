import pygame
import random
from settings import Settings
from Player import Player
from trash_can import TrashCan
from inventory import Inventory
from utils import search_trash_can
from shop_npc import ShopNPC
from redemption_center import RedemptionCenter
from junkyard import Junkyard

class Game:
    def __init__(self):
        self.settings = Settings()
        self.scale = 1.0
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width, self.settings.screen_height = self.screen.get_size()
        pygame.display.set_caption(self.settings.caption)
        self.shop_npc= ShopNPC(600, 200)

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
        self.inventory = Inventory(max_items=20, font=self.font, scale=self.scale)

        self.last_search_time = 0
        self.last_shop_toggle_time = 0
        self.shop_toggle_cooldown = 500
        self.cooldown = 1000

        self.inventory_open = False
        self.fullscreen = True

        self.redemption_center = RedemptionCenter(700, 300)
        self.money = 0
        self.last_redeem_time = 0
        self.redeem_cooldown = 500

        self.junkyard = Junkyard(400, 500)
        self.trash_dispose_start = None
        self.trash_dispose_duration = 3000

    def draw_shop_menu(self):
        box_width, box_height = 300, 200
        box_x = self.settings.screen_width // 2 - box_width // 2
        box_y = self.settings.screen_height // 2 - box_height // 2

        pygame.draw.rect(self.screen, (250, 250, 200), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 3)

        for i, item in enumerate(self.shop_npc.items_for_sale):
            text = self.font.render(f"{item} - $10", True, (0, 0, 0))
            self.screen.blit(text, (box_x + 20, box_y + 20 + i * 40))

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
                        if not self.shop_npc.is_open:
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
            
            if self.shop_npc.is_open and not self.player.rect.colliderect(self.shop_npc.rect):
                self.shop_npc.is_open = False

            if keys[pygame.K_e]:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shop_toggle_time >= self.shop_toggle_cooldown:
                    if self.shop_npc.is_near_player(self.player.rect):
                        self.shop_npc.is_open = not self.shop_npc.is_open
                        self.last_shop_toggle_time = current_time

                if self.redemption_center.is_near_player(self.player.rect):
                    if current_time - self.last_redeem_time >= self.redeem_cooldown:
                        if "Bottle" in self.inventory.items:
                            bottle_count = self.inventory.items.count("Bottle")
                            self.money += bottle_count * 0.1
                            self.inventory.items = [item for item in self.inventory.items if item != "Bottle"]
                            self.message = f"Redeemed {bottle_count} bottles for ${bottle_count * 0.1}"
                        else:
                            self.message = "No bottles to redeem!"
                        self.last_redeem_time = current_time
                
                if self.junkyard.is_near_player(self.player.rect):
                    if "Trash" in self.inventory.items:
                        current_time = pygame.time.get_ticks()
                        if self.trash_dispose_start is None:
                            self.trash_dispose_start = current_time
                        elapsed = current_time - self.trash_dispose_start
                        if elapsed  >= self.trash_dispose_duration:
                                trash_count = self.inventory.items.count("Trash")
                                self.inventory.items = [item for item in self.inventory.items if item != "Trash"]
                                self.message = f"Disposed of {trash_count} trash at the junkyard."
                                self.trash_dispose_start = None
                    else:
                        self.message = "No trash to dispose!"
                        self.trash_dispose_start = None
                else:
                    self.trash_dispose_start = None
    
                if current_time - self.last_search_time >= self.cooldown:
                    for can in self.trash_cans:
                        if self.player.rect.colliderect(can):
                            item = search_trash_can()
                            self.message = f"You found: {item}"
                            if item != "Nothing":
                                self.inventory.add_item(item)
                            self.last_search_time = current_time
                            break
            

            for can in self.trash_cans:
                can.draw(self.screen)
            
            self.redemption_center.draw(self.screen)
            money_text = self.font.render(f"Money: ${self.money}", True, (0, 0, 0))
            self.screen.blit(money_text, (20, 50))
            self.shop_npc.draw(self.screen)
            
            self.junkyard.draw(self.screen)
            self.player.draw(self.screen)
            message_surface = self.font.render(self.message, True, (0, 0, 0))
            self.screen.blit(message_surface, (20, 20))
        
            if self.inventory_open:
                center_x = self.settings.screen_width // 2
                center_y = self.settings.screen_height // 2
                self.inventory.draw_menu(self.screen, center_x, center_y)
            if self.shop_npc.is_open:
                self.draw_shop_menu()
            if self.trash_dispose_start:
                elapsed = pygame.time.get_ticks() - self.trash_dispose_start
                progress = min(elapsed / self.trash_dispose_duration, 1.0)
    
                bar_width = 200
                bar_height = 20
                bar_x = self.junkyard.rect.centerx - bar_width // 2
                bar_y = self.junkyard.rect.top - 30

                pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))  # Background
                pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))  # Fill
                pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)  # Border
            pygame.display.flip()
    
    def rescale_objects(self):
        new_size = int(40 * self.scale)
        self.player.rescale(new_size, new_size)
        self.player.speed = int(4 * self.scale)
        
        for can in self.trash_cans:
            can.rect.width = new_size
            can.rect.height = new_size
            
        new_font_size = int(30 * self.scale)
        self.font = pygame.font.SysFont(None, new_font_size)
        self.large_font = pygame.font.SysFont(None, int(50 * self.scale))
        self.inventory.font = self.font

        pygame.display.flip()