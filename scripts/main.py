import pygame
import sys
from player import Player
from map_loader import Map
from cutscenes import Cutscene
from items import Inventory
from enemies import Enemy
from combat import Weapon, Combat
from time_travel import TimeTravel

# ----------------------------
# Pygame setup
# ----------------------------
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ECLIPSE ⚔️")
clock = pygame.time.Clock()
FPS = 60

# ----------------------------
# Load maps
# ----------------------------
village_map = Map("maps/village.json")
past_village_map = Map("maps/past_village.json")
time_manager = TimeTravel(village_map, past_village_map)
current_map = time_manager.current_map

# ----------------------------
# Load player & inventory
# ----------------------------
player = Player(100, 100)
inventory = Inventory()

# ----------------------------
# Weapons & combat
# ----------------------------
sword = Weapon(name="Bolt's Sword", damage=15)
enemies = [
    Enemy(400, 300, "Goblin", hp=30, damage=5),
    Enemy(600, 200, "Wolf", hp=50, damage=8)
]
combat_system = Combat(player, enemies, sword)

# ----------------------------
# Story cutscenes
# ----------------------------
intro_cutscene = Cutscene("story_scenes/intro.json", screen)
intro_cutscene.play()

# ----------------------------
# Game loop
# ----------------------------
running = True
while running:
    screen.fill((0, 0, 0))

    # ------------------------
    # Event handling
    # ------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Time-travel switch
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                current_map = time_manager.switch_time()

    # ------------------------
    # Player movement
    # ------------------------
    keys = pygame.key.get_pressed()
    player.move(keys, current_map)

    # ------------------------
    # Update combat
    # ------------------------
    combat_system.update()

    # ------------------------
    # Draw everything
    # ------------------------
    current_map.draw(screen)
    player.draw(screen)
    combat_system.draw_enemies(screen)
    inventory.draw(screen)

    # ------------------------
    # Check for special zones (story triggers)
    # ------------------------
    # Example: enter castle triggers cutscene
    castle_zone = pygame.Rect(700, 500, 50, 50)
    if player.rect.colliderect(castle_zone):
        castle_cutscene = Cutscene("story_scenes/castle_secret.json", screen)
        castle_cutscene.play()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
