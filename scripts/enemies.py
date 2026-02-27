import pygame
import random

class Enemy:
    def __init__(self, x, y, name="Enemy", hp=50, damage=5, color=(255,0,0)):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 48
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.name = name
        self.hp = hp
        self.damage = damage
        self.color = color
        self.speed = 2

    def move_towards_player(self, player):
        # Simple AI: move towards player if close
        if abs(player.x - self.x) < 200:
            if player.x > self.x:
                self.x += self.speed
            elif player.x < self.x:
                self.x -= self.speed
        if abs(player.y - self.y) < 200:
            if player.y > self.y:
                self.y += self.speed
            elif player.y < self.y:
                self.y -= self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def take_damage(self, dmg):
        self.hp -= dmg
        return self.hp <= 0  # Returns True if enemy dies
