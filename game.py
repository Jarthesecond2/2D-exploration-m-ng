import pygame
import random
from settings import Settings

pygame.init()
item = None
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Homeless simulator")

GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 50)

player = pygame.Rect(100, 100, 40, 40)
player_speed = 4




trash_cans = [
    pygame.Rect(200, 150, 40, 40),
    pygame.Rect(500, 400, 40, 40),
    pygame.Rect(300, 250, 40, 40)
]

message = ""

def search_trash_can():
    roll = random.randint(1, 100)
    if roll <= 15:
        return "Bottle"
    elif roll <= 74:
        return "Trash"
    elif roll <= 75:
        return "Token"
    else:
        return "Nothing"

def draw_play_button():
    screen.fill(GREEN)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60)
    pygame.draw.rect(screen, LIGHT_GRAY, button_rect)
    text = large_font.render("Play", True, DARK_GRAY)
    screen.blit(text, (button_rect.x + (button_rect.width - text.get_width()) // 2,
                       button_rect.y + (button_rect.height - text.get_height()) // 2))
    pygame.display.flip()
    return button_rect

def wait_for_play():
    waiting = True
    while waiting:
        button_rect = draw_play_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                waiting = False

wait_for_play()
inventory = []

running = True
clock = pygame.time.Clock()
last_search_time = 0
cooldown = 1000
while running:
    clock.tick(60)
    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= player_speed
    if keys[pygame.K_d]:
        player.x += player_speed
    if keys[pygame.K_w]:
        player.y -= player_speed
    if keys[pygame.K_s]:
        player.y += player_speed

    if keys[pygame.K_e]:
        current_time = pygame.time.get_ticks()
        if current_time - last_search_time >= cooldown:
            for can in trash_cans:
                if player.colliderect(can):
                    item = search_trash_can()
                    message = "You found: " + item
                    inventory.append(item)
                    last_search_time = current_time
                    break

    pygame.draw.rect(screen, BLUE, player)

    for can in trash_cans:
        pygame.draw.rect(screen, GRAY, can)

    text_surface = font.render(message, True, BLACK)
    screen.blit(text_surface, (20, 20))
    inv_text = font.render("Inventory: " + ", ".join(inventory[-5:]), True, BLACK)
    screen.blit(inv_text, (20, 50))
    pygame.display.flip()

pygame.quit()
