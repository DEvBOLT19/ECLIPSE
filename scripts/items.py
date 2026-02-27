import pygame

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item_name):
        self.items.append(item_name)

    def draw(self, screen):
        # Draw simple inventory text
        font = pygame.font.SysFont(None, 24)
        text = font.render("Inventory: " + ", ".join(self.items), True, (255, 255, 255))
        screen.blit(text, (10, 10))
