import pygame
import random
from player import Player
from block import Block
from enemy import Enemy
from bullet import Bullet
import os

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
        self.font = pygame.font.SysFont("arial", 40)

        try:
            self.background = pygame.image.load("background.png").convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except (pygame.error, FileNotFoundError):
            self.background = None

        self.reset_game()

    def reset_game(self):
        self.blocks = []
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.game_over = False
        self.game_won = False

        self.map_width = self.width // self.TILE_SIZE
        self.map_height = self.height // self.TILE_SIZE

        self.generate_border_blocks()
        self.generate_random_blocks()

        px = self.width // 2
        py = self.height // 2
        self.player = Player(px, py, self.player_img, self.shoot_sound, self.explosion_sound)

        max_enemies = 4
        attempts = 0
        padding = 2  # Відстань від краю, щоб вороги не спавнилися близько до меж

        while len(self.enemies) < max_enemies and attempts < 100:
            ex = random.randint(padding, self.map_width - 1 - padding) * self.TILE_SIZE + self.TILE_SIZE // 2
            ey = random.randint(padding, self.map_height - 1 - padding) * self.TILE_SIZE + self.TILE_SIZE // 2
            enemy_rect = pygame.Rect(ex - self.TILE_SIZE // 2, ey - self.TILE_SIZE // 2, self.TILE_SIZE, self.TILE_SIZE)
            blocked = any(block.rect.colliderect(enemy_rect) for block in self.blocks)
            if enemy_rect.colliderect(self.player.rect):
                blocked = True
            if not blocked:
                enemy = Enemy(ex, ey, self.enemy_img, self.shoot_sound, self.explosion_sound)
                self.enemies.append(enemy)
            attempts += 1

    def generate_border_blocks(self):
        for x in range(self.map_width):
            self.blocks.append(Block(x * self.TILE_SIZE, 0, self.block_img, destructible=False))
            self.blocks.append(Block(x * self.TILE_SIZE, (self.map_height - 1) * self.TILE_SIZE, self.block_img, destructible=False))
        for y in range(1, self.map_height - 1):
            self.blocks.append(Block(0, y * self.TILE_SIZE, self.block_img, destructible=False))
            self.blocks.append(Block((self.map_width - 1) * self.TILE_SIZE, y * self.TILE_SIZE, self.block_img, destructible=False))

    def generate_random_blocks(self):
        safe_zones = [
            pygame.Rect(self.width // 2 - 100, self.height // 2 - 100, 200, 200),
            pygame.Rect(100 - 60, 100 - 60, 160, 160),
            pygame.Rect(self.width - 160, 100 - 60, 160, 160),
            pygame.Rect(100 - 60, self.height - 160, 160, 160),
            pygame.Rect(self.width - 160, self.height - 160, 160, 160),
        ]
        for x in range(1, self.map_width - 1):
            for y in range(1, self.map_height - 1):
                if random.random() < 0.2:  #ЗАМІТКА ТУТ МІНЯТИ КІЛЬКІСТЬ БЛОКІВ НА КАРТИ ДЛЯ ТЕСТІВ ПРИГОДИТЬСЯ
                    rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                    if any(safe.colliderect(rect) for safe in safe_zones):
                        continue
                    self.blocks.append(Block(rect.x, rect.y, self.block_img, destructible=True))

    def update(self):
        if self.game_over or self.game_won:
            return

        keys = pygame.key.get_pressed()
        shot = self.player.move(keys, self.blocks)

        if shot:
            x, y = self.player.rect.center
            direction = self.player.direction
            self.bullets.append(Bullet(x, y, direction, image_path="bullet_green.png", scale=0.7))
            self.shoot_sound.play()

        for enemy in self.enemies:
            bullet = enemy.update(self.player, self.blocks)
            if bullet:
                self.enemy_bullets.append(bullet)
                self.shoot_sound.play()

        self.enemies = [enemy for enemy in self.enemies if not enemy.destroyed]

        for bullet in self.bullets[:]:
            alive = bullet.update(self.blocks, self.enemies)
            if not alive or bullet.off_screen(self.screen):
                self.bullets.remove(bullet)

        for e_bullet in self.enemy_bullets[:]:
            alive = e_bullet.update(self.blocks, [self.player])
            if not alive or e_bullet.off_screen(self.screen):
                self.enemy_bullets.remove(e_bullet)

        if self.player.health <= 0:
            self.game_over = True

        if len(self.enemies) == 0:
            self.game_won = True

    def render(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((255, 255, 255))  

        for block in self.blocks:
            block.render(self.screen)
        for bullet in self.bullets:
            bullet.render(self.screen)
        for e_bullet in self.enemy_bullets:
            e_bullet.render(self.screen)
        self.player.render(self.screen)
        for enemy in self.enemies:
            enemy.render(self.screen)
        if self.game_over:
            self.show_restart_screen()
        elif self.game_won:
            self.show_win_screen()

    def show_restart_screen(self):
        text = self.font.render("Game Over", True, (255, 0, 0))
        btn = self.font.render("Press R to Restart", True, (0, 0, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 60))
        self.screen.blit(btn, (self.width // 2 - btn.get_width() // 2, self.height // 2 + 10))

    def show_win_screen(self):
        text = self.font.render("You Win!", True, (0, 128, 0))
        btn_restart = self.font.render("Press R to Restart", True, (0, 0, 0))
        btn_exit = self.font.render("Press Q to Quit", True, (0, 0, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 80))
        self.screen.blit(btn_restart, (self.width // 2 - btn_restart.get_width() // 2, self.height // 2))
        self.screen.blit(btn_exit, (self.width // 2 - btn_exit.get_width() // 2, self.height // 2 + 60))

    def handle_events(self, event):
        if self.game_over or self.game_won:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
