import pygame
import json

TILE_SIZE = 32

class Map:
    def __init__(self, map_file):
        self.map_file = map_file
        self.tiles = []
        self.load_map()

    def load_map(self):
        with open(self.map_file) as f:
            data = json.load(f)
            self.tiles = data["tiles"]

    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                color = (50, 50, 50) if tile == 1 else (0, 100, 0)
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def is_blocked(self, x, y):
        tile_x = x // TILE_SIZE
        tile_y = y // TILE_SIZE
        if tile_y >= len(self.tiles) or tile_x >= len(self.tiles[0]):
            return True
        return self.tiles[tile_y][tile_x] == 1
