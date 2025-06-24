import pygame
import random
from player import Player
from block import Block
from bullet import Bullet

class Game:
    TILE_SIZE = 54
    PLAYER_SCALE = 0.75

    def __init__(self, screen, player_img, block_img, shoot_sound, explosion_sound):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.player_img = pygame.transform.smoothscale(
            player_img,
            (int(player_img.get_width() * self.PLAYER_SCALE), int(player_img.get_height() * self.PLAYER_SCALE))
        )
        self.block_img = pygame.transform.smoothscale(block_img, (self.TILE_SIZE, self.TILE_SIZE))
        self.shoot_sound = shoot_sound
        self.explosion_sound = explosion_sound

        self.blocks = []
        self.bullets = []

        self.map_width = self.width // self.TILE_SIZE
        self.map_height = self.height // self.TILE_SIZE

        self.map_grid = [[0 for _ in range(self.map_height)] for _ in range(self.map_width)]
        self.generate_map()

        spawn_pos = self.find_spawn_position()
        px = spawn_pos[0] * self.TILE_SIZE + self.TILE_SIZE // 2
        py = spawn_pos[1] * self.TILE_SIZE + self.TILE_SIZE // 2
        self.player = Player(px, py, self.player_img, self.shoot_sound, self.explosion_sound)

    def generate_map(self):
        for x in range(self.map_width):
            self.map_grid[x][0] = 2
            self.map_grid[x][self.map_height - 1] = 2
        for y in range(self.map_height):
            self.map_grid[0][y] = 2
            self.map_grid[self.map_width - 1][y] = 2

        for x in range(1, self.map_width - 1):
            for y in range(1, self.map_height - 1):
                if random.random() < 0.10:
                    self.map_grid[x][y] = 1

        corridor_rows = [1, self.map_height // 3, (self.map_height * 2) // 3]
        for y in corridor_rows:
            for x in range(1, self.map_width - 1):
                self.map_grid[x][y] = 0

        self.update_blocks()

    def update_blocks(self):
        self.blocks.clear()
        for x in range(self.map_width):
            for y in range(self.map_height):
                cell = self.map_grid[x][y]
                if cell == 1:
                    self.blocks.append(Block(x * self.TILE_SIZE, y * self.TILE_SIZE, self.block_img))
                elif cell == 2:
                    self.blocks.append(Block(x * self.TILE_SIZE, y * self.TILE_SIZE, self.block_img, indestructible=True))

    def find_spawn_position(self):
        free_positions = [
            (x, y) for x in range(2, self.map_width - 2)
            for y in range(3, self.map_height - 2)
            if self.map_grid[x][y] == 0
        ]
        random.shuffle(free_positions)
        for x, y in free_positions:
            rect = pygame.Rect(
                x * self.TILE_SIZE,
                y * self.TILE_SIZE,
                self.TILE_SIZE,
                self.TILE_SIZE
            )
            neighbors = [
                (x - 1, y), (x + 1, y),
                (x, y - 1), (x, y + 1)
            ]
            if any(
                nx < 0 or ny < 0 or nx >= self.map_width or ny >= self.map_height or self.map_grid[nx][ny] == 1
                for nx, ny in neighbors
            ):
                continue
            if not any(rect.colliderect(b.rect.inflate(-10, -10)) for b in self.blocks):
                return (x, y)
        return (1, 3)

    def update(self):
        keys = pygame.key.get_pressed()
        shot = self.player.move(keys, self.blocks)
        if shot:
            x, y = self.player.rect.center
            direction = self.player.direction
            self.bullets.append(Bullet(x, y, direction))

        for bullet in self.bullets[:]:
            alive = bullet.update(self.blocks)
            if not alive or bullet.off_screen(self.screen):
                self.bullets.remove(bullet)

        self.blocks = [b for b in self.blocks if not getattr(b, 'destroyed', False)]

    def render(self):
        self.screen.fill((220, 220, 220))
        for block in self.blocks:
            block.render(self.screen)
        for bullet in self.bullets:
            bullet.render(self.screen)
        self.player.render(self.screen)
