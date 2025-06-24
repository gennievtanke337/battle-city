import pygame
import random
from player import Player
from block import Block
from enemy import Enemy
from bullet import Bullet

class Game:
    TILE_SIZE = 60

    def __init__(self, screen, player_img, block_img, shoot_sound, explosion_sound, enemy_img):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.player_img = player_img
        self.block_img = block_img
        self.shoot_sound = shoot_sound
        self.explosion_sound = explosion_sound
        self.enemy_img = enemy_img

        self.blocks = []
        self.bullets = []
        self.enemy_bullets = []

        self.map_width = self.width // self.TILE_SIZE
        self.map_height = self.height // self.TILE_SIZE

        self.map_grid = [[0 for _ in range(self.map_height)] for _ in range(self.map_width)]
        self.generate_map()

        self.start_time = pygame.time.get_ticks()

        px = self.width // 2
        py = self.height // 2
        self.player = Player(px, py, self.player_img, self.shoot_sound, self.explosion_sound)

        self.enemies = []
        offset = 150
        positions = [
            (offset, offset),
            (self.width - offset, offset),
            (offset, self.height - offset),
            (self.width - offset, self.height - offset)
        ]
        for pos in positions:
            ex, ey = pos
            enemy = Enemy(ex, ey, self.enemy_img, self.shoot_sound, self.explosion_sound)
            self.enemies.append(enemy)

    def generate_map(self):
        for x in range(self.map_width):
            self.map_grid[x][0] = 2
            self.map_grid[x][self.map_height - 1] = 2
        for y in range(self.map_height):
            self.map_grid[0][y] = 2
            self.map_grid[self.map_width - 1][y] = 2
        self.update_blocks()

    def update_blocks(self):
        self.blocks.clear()
        for x in range(self.map_width):
            for y in range(self.map_height):
                if self.map_grid[x][y] == 2:
                    self.blocks.append(Block(x * self.TILE_SIZE, y * self.TILE_SIZE, self.block_img, destructible=False))

    def update(self):
        keys = pygame.key.get_pressed()
        shot = self.player.move(keys, self.blocks)
        if shot:
            x, y = self.player.rect.center
            direction = self.player.direction
            self.bullets.append(Bullet(x, y, direction))

        for bullet in self.bullets[:]:
            if not bullet.update(self.enemies + self.blocks):
                self.bullets.remove(bullet)
            elif bullet.off_screen(self.screen):
                self.bullets.remove(bullet)

        for eb in self.enemy_bullets[:]:
            if not eb.update([self.player] + self.enemies + self.blocks):
                self.enemy_bullets.remove(eb)
            elif eb.off_screen(self.screen):
                self.enemy_bullets.remove(eb)

        for enemy in self.enemies:
            enemy.update(self.player, self.blocks, self.enemies, self.enemy_bullets)

    def render(self):
        self.screen.fill((220, 220, 220))
        for block in self.blocks:
            block.render(self.screen)
        for bullet in self.bullets:
            bullet.render(self.screen)
        for eb in self.enemy_bullets:
            eb.render(self.screen)
        for enemy in self.enemies:
            enemy.render(self.screen)

        now = pygame.time.get_ticks()
        if now - self.start_time < 2000:
            pygame.draw.rect(self.screen, (255, 255, 255), self.player.rect.inflate(8, 8), 2)
        self.player.render(self.screen)
