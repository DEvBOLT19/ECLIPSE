import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.width = 32
        self.height = 48
        self.color = (0, 255, 255)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys, game_map):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        # Collision check with map
        if not game_map.is_blocked(self.x + dx, self.y):
            self.x += dx
        if not game_map.is_blocked(self.x, self.y + dy):
            self.y += dy
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
