import pygame
import sys
from player import Player
from map_loader import Map
from cutscenes import Cutscene
from items import Inventory

# Initialize Pygame
pygame.init()

# Window setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ECLIPSE ⚔️")

# Clock for FPS
clock = pygame.time.Clock()
FPS = 60

# Load initial map and story scene
current_map = Map("maps/village.json")
cutscene = Cutscene("story_scenes/intro.json")
player = Player(100, 100)  # Starting position
inventory = Inventory()

# Game loop
running = True
cutscene.play()  # Play intro cutscene

while running:
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    player.move(keys, current_map)

    # Draw map and player
    current_map.draw(screen)
    player.draw(screen)

    # Draw HUD
    inventory.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
