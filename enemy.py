import pygame
import random
import math
from bullet import Bullet

class Enemy:
    SPEED = 2
    SHOOT_DELAY = 600
    CHANGE_DIR_INTERVAL = 2000

    DIRECTIONS = {
        "up": (0, -SPEED),
        "down": (0, SPEED),
        "left": (-SPEED, 0),
        "right": (SPEED, 0),
    }

    def __init__(self, x, y, img, shoot_sound, explosion_sound):
        self.original_img = img
        self.img = img
        self.rect = self.img.get_rect(center=(x, y))
        self.shoot_sound = shoot_sound
        self.explosion_sound = explosion_sound
        self.health = 1
        self.destroyed = False
        self.direction = random.choice(list(self.DIRECTIONS.keys()))
        self.dx, self.dy = self.DIRECTIONS[self.direction]
        self.last_dir_change = pygame.time.get_ticks()
        self.last_shot_time = 0

    def update(self, player, blocks):
        if self.destroyed:
            return None

        now = pygame.time.get_ticks()

        if self.can_see_target(player, blocks):
            self.move_towards(player.rect.center, blocks)
        else:
            if now - self.last_dir_change > self.CHANGE_DIR_INTERVAL:
                self.last_dir_change = now
                self.change_direction(blocks)
            self.try_move(blocks)

        self.update_image_direction()

        if now - self.last_shot_time > self.SHOOT_DELAY and self.can_see_target(player, blocks):
            bullet = self.shoot()
            self.last_shot_time = now
            return bullet
        return None

    def move_towards(self, target_pos, blocks):
        x, y = self.rect.center
        tx, ty = target_pos
        dx = tx - x
        dy = ty - y

        dist_x = abs(dx)
        dist_y = abs(dy)

        if dist_y >= dist_x:
            self.direction = "up" if dy < 0 else "down"
        else:
            self.direction = "left" if dx < 0 else "right"

        self.dx, self.dy = self.DIRECTIONS[self.direction]
        self.try_move(blocks)

    def try_move(self, blocks):
        next_rect = self.rect.move(self.dx, self.dy)
        for block in blocks:
            if next_rect.colliderect(block.rect):
                self.change_direction(blocks)
                return False
        self.rect = next_rect
        return True

    def change_direction(self, blocks):
        options = list(self.DIRECTIONS.keys())
        random.shuffle(options)
        for dir_ in options:
            dx, dy = self.DIRECTIONS[dir_]
            test_rect = self.rect.move(dx, dy)
            if not any(test_rect.colliderect(b.rect) for b in blocks):
                self.direction = dir_
                self.dx, self.dy = dx, dy
                return
        self.dx = -self.dx
        self.dy = -self.dy

    def update_image_direction(self):
        angle_map = {"up": 90, "down": -90, "left": 180, "right": 0}
        angle = angle_map[self.direction]
        self.img = pygame.transform.rotate(self.original_img, angle)
        self.rect = self.img.get_rect(center=self.rect.center)

    def can_see_target(self, target, blocks):
        x1, y1 = self.rect.center
        x2, y2 = target.rect.center
        dx = x2 - x1
        dy = y2 - y1
        distance = math.hypot(dx, dy)
        if distance == 0:
            return False
        steps = int(distance // (self.rect.width // 2)) + 1
        for i in range(1, steps):
            xi = x1 + dx * i / steps
            yi = y1 + dy * i / steps
            check_rect = pygame.Rect(xi - 5, yi - 5, 10, 10)
            for block in blocks:
                if block.rect.colliderect(check_rect):
                    return False
        return True

    def shoot(self):
        self.shoot_sound.play()
        x, y = self.rect.center
        return Bullet(x, y, self.direction, image_path="bullet_red.png", scale=1.4)

    def hit(self):
        self.health -= 1
        if self.health <= 0 and not self.destroyed:
            self.destroyed = True
            self.explosion_sound.play()

    def render(self, surf):
        if not self.destroyed:
            surf.blit(self.img, self.rect)
