import json
import sys
from pathlib import Path

import pygame

from combat import Combat, Weapon
from cutscenes import Cutscene
from enemies import Enemy
from items import Inventory
from map_loader import Map
from player import Player
from time_travel import TimeTravel

BASE_DIR = Path(__file__).resolve().parents[1]


def project_path(*parts):
    return str(BASE_DIR.joinpath(*parts))


def play_scene(scene_name, game_screen):
    Cutscene(project_path("story_scenes", scene_name), game_screen).play()


def give_item(inventory, item_name):
    if item_name not in inventory.items:
        inventory.add_item(item_name)


def load_save_data():
    save_path = BASE_DIR / "save_data" / "save1.json"
    if not save_path.exists():
        return {}
    try:
        with save_path.open(encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def write_save_data(chapter, location, in_past, inventory_items, companion_unlocked):
    save_path = BASE_DIR / "save_data" / "save1.json"
    payload = {
        "chapter": chapter,
        "location": location,
        "is_in_past": in_past,
        "items": inventory_items,
        "companion_unlocked": companion_unlocked,
    }
    with save_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ECLIPSE ⚔️")
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 22)

maps = {
    "village": Map(project_path("maps", "village.json")),
    "past_village": Map(project_path("maps", "past_village.json")),
    "city": Map(project_path("maps", "city.json")),
    "past_city": Map(project_path("maps", "past_city.json")),
    "castle": Map(project_path("maps", "castle.json")),
    "past_castle": Map(project_path("maps", "past_castle.json")),
}

# time travel per location
travel_managers = {
    "village": TimeTravel(maps["village"], maps["past_village"]),
    "city": TimeTravel(maps["city"], maps["past_city"]),
    "castle": TimeTravel(maps["castle"], maps["past_castle"]),
}

current_location = "village"
current_map = travel_managers[current_location].current_map

player = Player(100, 100)
inventory = Inventory()
sword = Weapon(name="Father's Blade", damage=18)
active_enemies = [Enemy(450, 320, "Goblin", hp=35, damage=5), Enemy(560, 250, "Wolf", hp=45, damage=7)]
combat_system = Combat(player, active_enemies, sword)

chapter = 1
companion_unlocked = False
father_boss_spawned = False
queen_phase = 0
ending_shown = False
message = "Find the glowing key in the village (press SPACE near markers)."

save_data = load_save_data()
if save_data:
    chapter = int(save_data.get("chapter", chapter))
    current_location = save_data.get("location", current_location)
    if current_location not in travel_managers:
        current_location = "village"
    current_map = travel_managers[current_location].current_map
    if save_data.get("is_in_past"):
        current_map = travel_managers[current_location].switch_time()
    for item in save_data.get("items", []):
        give_item(inventory, item)
    companion_unlocked = bool(save_data.get("companion_unlocked", companion_unlocked))
    if chapter >= 7:
        father_boss_spawned = False
    message = "Loaded save. Continue your mission."

zones = {
    "village_key": pygame.Rect(260, 180, 50, 50),
    "to_city": pygame.Rect(740, 250, 50, 90),
    "old_man": pygame.Rect(500, 120, 60, 60),
    "riverbank": pygame.Rect(120, 520, 80, 60),
    "castle_gate": pygame.Rect(700, 500, 70, 70),
    "powerups": pygame.Rect(100, 120, 70, 70),
    "father_boss": pygame.Rect(360, 220, 80, 80),
    "queen_boss": pygame.Rect(560, 220, 90, 90),
}

required_true_ending_items = {
    "Father's Blade",
    "Temporal Shard",
    "Cursed Key",
    "Smoke Bomb",
    "Potion",
    "Guard Disguise",
    "Hidden Passage Blueprint",
}

play_scene("intro.json", screen)

running = True
while running:
    screen.fill((0, 0, 0))
    interact_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t and chapter >= 6:
                current_map = travel_managers[current_location].switch_time()
                if chapter == 6 and travel_managers[current_location].is_in_past:
                    play_scene("chapter6_time_reveal.json", screen)
                    chapter = 7
                    message = "Face your cursed father in the castle hall."
            if event.key == pygame.K_SPACE:
                interact_pressed = True

    keys = pygame.key.get_pressed()
    player.move(keys, current_map)

    for enemy in active_enemies:
        enemy.move_towards_player(player)
    combat_system.update()

    # chapter progression
    if interact_pressed:
        if chapter == 1 and player.rect.colliderect(zones["village_key"]):
            give_item(inventory, "Cursed Key")
            play_scene("chapter1_key_found.json", screen)
            chapter = 2
            message = "Go to the city gate on the east side of the village."

        elif chapter == 2 and player.rect.colliderect(zones["to_city"]):
            current_location = "city"
            current_map = travel_managers[current_location].current_map
            player.x, player.y = 80, 300
            player.rect.topleft = (player.x, player.y)
            play_scene("chapter2_city_arrival.json", screen)
            message = "Find the old swordsman in the city."

        elif chapter == 2 and current_location == "city" and player.rect.colliderect(zones["old_man"]):
            give_item(inventory, "Guard Disguise")
            give_item(inventory, "Hidden Passage Blueprint")
            play_scene("old_man_intro.json", screen)
            chapter = 3
            message = "Return to the riverbank and meet your companion."

        elif chapter == 3 and current_location in {"city", "village"}:
            if current_location == "city" and player.rect.colliderect(zones["to_city"]):
                current_location = "village"
                current_map = travel_managers[current_location].current_map
                player.x, player.y = 650, 300
                player.rect.topleft = (player.x, player.y)
            if current_location == "village" and player.rect.colliderect(zones["riverbank"]):
                companion_unlocked = True
                give_item(inventory, "Father's Blade")
                give_item(inventory, "Castle Map")
                play_scene("chapter3_companion.json", screen)
                chapter = 4
                message = "Infiltrate the castle and uncover the truth."

        elif chapter == 4 and current_location == "village" and player.rect.colliderect(zones["castle_gate"]):
            current_location = "castle"
            current_map = travel_managers[current_location].current_map
            player.x, player.y = 120, 500
            player.rect.topleft = (player.x, player.y)
            play_scene("castle_secret.json", screen)
            chapter = 5
            message = "Collect power-ups and prepare for difficult fights."

        elif chapter == 5 and current_location == "castle" and player.rect.colliderect(zones["powerups"]):
            give_item(inventory, "Smoke Bomb")
            give_item(inventory, "Potion")
            give_item(inventory, "Temporal Shard")
            play_scene("chapter5_powerups.json", screen)
            chapter = 6
            message = "Press T to time travel and reveal the hidden truth."

    if chapter >= 7 and current_location == "castle" and not father_boss_spawned:
        active_enemies.clear()
        active_enemies.append(Enemy(380, 240, "Cursed Father", hp=110, damage=11, color=(180, 0, 180)))
        father_boss_spawned = True

    if chapter == 7 and father_boss_spawned and len(active_enemies) == 0:
        play_scene("chapter7_father_saved.json", screen)
        chapter = 8
        queen_phase = 1
        active_enemies.append(Enemy(560, 220, "Corrupted Queen (Phase 1)", hp=90, damage=10, color=(255, 120, 0)))
        message = "Defeat the corrupted queen (phase 1)."

    if chapter == 8 and queen_phase == 1 and len(active_enemies) == 0:
        queen_phase = 2
        active_enemies.append(Enemy(560, 220, "Corrupted Queen (Phase 2)", hp=130, damage=14, color=(255, 40, 40)))
        message = "Final phase! Defeat the corrupted queen."

    if chapter == 8 and queen_phase == 2 and len(active_enemies) == 0:
        chapter = 9
        message = "Ending unlocked. Press SPACE near the throne zone to finish."

    if chapter == 9 and player.rect.colliderect(zones["queen_boss"]) and interact_pressed and not ending_shown:
        if required_true_ending_items.issubset(set(inventory.items)) and companion_unlocked:
            play_scene("chapter9_true_ending.json", screen)
            message = "TRUE ENDING: Kingdom restored, hidden history revealed."
        else:
            play_scene("chapter9_normal_ending.json", screen)
            message = "ENDING: Kingdom restored. Collect all key items for true ending."
        ending_shown = True

    current_map.draw(screen)
    for name, zone in zones.items():
        marker_color = (255, 255, 0) if "boss" not in name else (255, 80, 80)
        pygame.draw.rect(screen, marker_color, zone, 2)

    player.draw(screen)
    combat_system.draw_enemies(screen)
    inventory.draw(screen)

    chapter_text = font.render(f"Chapter {chapter}", True, (255, 255, 255))
    loc_text = small_font.render(
        f"Location: {current_location}{' (Past)' if travel_managers[current_location].is_in_past else ' (Present)'}",
        True,
        (190, 220, 255),
    )
    msg_text = small_font.render(message[:95], True, (255, 230, 180))

    screen.blit(chapter_text, (10, 36))
    screen.blit(loc_text, (10, 64))
    screen.blit(msg_text, (10, 88))

    if companion_unlocked:
        companion_text = small_font.render("Companion: Kiro (active)", True, (120, 255, 180))
        screen.blit(companion_text, (10, 112))

    if chapter < 6:
        hint_text = small_font.render("Time travel unlocks in Chapter 6 (press T)", True, (170, 170, 170))
        screen.blit(hint_text, (10, 136))

    write_save_data(
        chapter,
        current_location,
        travel_managers[current_location].is_in_past,
        inventory.items,
        companion_unlocked,
    )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
