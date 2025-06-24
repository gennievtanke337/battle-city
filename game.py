import pygame
import random
from player import Player
from block import Block
from bullet import Bullet
from enemy import Enemy

class Game:
    TILE_SIZE = 60

    def __init__(self, screen, player_img, block_img, shoot_sound, explosion_sound, enemy_img):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.player_img = player_img
        self.block_img = block_img
        self.enemy_img = enemy_img
        self.shoot_sound = shoot_sound
        self.explosion_sound = explosion_sound

        self.blocks = []
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []

        self.map_width = self.width // self.TILE_SIZE
        self.map_height = self.height // self.TILE_SIZE

        self.generate_border_blocks()

        px = self.width // 2
        py = self.height // 2
        self.player = Player(px, py, self.player_img, self.shoot_sound, self.explosion_sound)

        margin = 100
        positions = [
            (margin, margin),
            (self.width - margin, margin),
            (margin, self.height - margin),
            (self.width - margin, self.height - margin),
        ]
        for pos in positions:
            enemy = Enemy(pos[0], pos[1], self.enemy_img, self.shoot_sound, self.explosion_sound)
            self.enemies.append(enemy)

    def generate_border_blocks(self):
        self.blocks.clear()
        for x in range(self.map_width):
            self.blocks.append(Block(x * self.TILE_SIZE, 0, self.block_img, destructible=False))
            self.blocks.append(Block(x * self.TILE_SIZE, (self.map_height - 1) * self.TILE_SIZE, self.block_img, destructible=False))
        for y in range(1, self.map_height - 1):
            self.blocks.append(Block(0, y * self.TILE_SIZE, self.block_img, destructible=False))
            self.blocks.append(Block((self.map_width - 1) * self.TILE_SIZE, y * self.TILE_SIZE, self.block_img, destructible=False))

    def update(self):
        keys = pygame.key.get_pressed()
        shot = self.player.move(keys, self.blocks)
        if shot:
            x, y = self.player.rect.center
            direction = self.player.direction
            self.bullets.append(Bullet(x, y, direction))

        for enemy in self.enemies:
            enemy.update(self.player, self.blocks, self.enemies, self.enemy_bullets)

        for bullet in self.bullets[:]:
            bullet.rect.move_ip(bullet.dx, bullet.dy)

            hit_block = None
            for block in self.blocks:
                if block.destructible and bullet.rect.colliderect(block.rect):
                    block.health -= 1
                    if block.health <= 0:
                        self.blocks.remove(block)
                    hit_block = block
                    break

            hit_enemy = None
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.hit()
                    hit_enemy = enemy
                    break

            if hit_block or hit_enemy or bullet.off_screen(self.screen):
                self.bullets.remove(bullet)

        for e_bullet in self.enemy_bullets[:]:
            e_bullet.rect.move_ip(e_bullet.dx, e_bullet.dy)

            hit_targets = [self.player] + self.enemies
            hit_something = False
            for target in hit_targets:
                if e_bullet.rect.colliderect(target.rect):
                    target.hit()
                    hit_something = True
                    break

            if hit_something or e_bullet.off_screen(self.screen):
                self.enemy_bullets.remove(e_bullet)

    def render(self):
        self.screen.fill((220, 220, 220))
        for block in self.blocks:
            block.render(self.screen)

        for bullet in self.bullets:
            bullet.render(self.screen)

        for e_bullet in self.enemy_bullets:
            e_bullet.render(self.screen)

        self.player.render(self.screen)

        for enemy in self.enemies:
            enemy.render(self.screen)
