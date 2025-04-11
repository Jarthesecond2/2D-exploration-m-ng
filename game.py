"""Game"""
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Homeless simulator")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Player setup
player = pygame.Rect(100, 100, 40, 40)
player_speed = 4

# Trash cans
trash_cans = [
    pygame.Rect(200, 150, 40, 40),
    pygame.Rect(500, 400, 40, 40),
    pygame.Rect(300, 250, 40, 40)
]

# Font
font = pygame.font.SysFont(None, 30)
message = ""

# Search function
def search_trash_can():
    roll = random.randint(1, 100)
    if roll <= 15:
        return "Bottle"
    elif roll <= 74:
        return "Trash"
    elif roll <= 75:
        return "Sad Bacon"
    else:
        return "Poop"

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= player_speed
    if keys[pygame.K_d]:
        player.x += player_speed
    if keys[pygame.K_w]:
        player.y -= player_speed
    if keys[pygame.K_s]:
        player.y += player_speed

    # Interaction
    if keys[pygame.K_e]:
        for can in trash_cans:
            if player.colliderect(can):
                message = "You found: " + search_trash_can()
                break

    # Draw player
    pygame.draw.rect(screen, BLUE, player)

    # Draw trash cans
    for can in trash_cans:
        pygame.draw.rect(screen, GRAY, can)

    # Display message
    text_surface = font.render(message, True, BLACK)
    screen.blit(text_surface, (20, 20))

    # Update screen
    pygame.display.flip()

pygame.quit()