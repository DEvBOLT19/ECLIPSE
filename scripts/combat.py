import pygame

class Weapon:
    def __init__(self, name="Sword", damage=10, color=(0,255,0)):
        self.name = name
        self.damage = damage
        self.color = color
        self.width = 20
        self.height = 5

    def attack(self, enemy):
        killed = enemy.take_damage(self.damage)
        return killed

class Combat:
    def __init__(self, player, enemies, weapon):
        self.player = player
        self.enemies = enemies
        self.weapon = weapon

    def update(self):
        # Check collision and attack
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                killed = self.weapon.attack(enemy)
                if killed:
                    self.enemies.remove(enemy)

    def draw_enemies(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
