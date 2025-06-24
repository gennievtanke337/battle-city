import pygame
import math
from bullet import Bullet

class Enemy:
    SPEED = 2
    SHOT_DELAY = 600

    def __init__(self, x, y, img, shoot_sound, explosion_sound):
        self.original_img = img
        self.img = img
        self.rect = self.img.get_rect(center=(x, y))
        self.direction = "down"
        self.shoot_sound = shoot_sound
        self.explosion_sound = explosion_sound
        self.last_shot_time = 0
        self.health = 1
        self.destroyed = False

    def update(self, player, blocks, enemies, enemy_bullets):
        if self.destroyed:
            return

        self.look_and_move(player, blocks)

        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.SHOT_DELAY and self.can_see_target(player, blocks):
            bullet = self.shoot()
            if bullet:
                enemy_bullets.append(bullet)
            self.last_shot_time = now

    def look_and_move(self, player, blocks):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance == 0:
            return
        dx /= distance
        dy /= distance

        next_pos = self.rect.move(dx * self.SPEED, dy * self.SPEED)

        if not any(next_pos.colliderect(b.rect.inflate(-8, -8)) for b in blocks):
            self.rect = next_pos
            self.update_direction(dx, dy)

    def update_direction(self, dx, dy):
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"
        angle = {"up": 90, "right": 0, "down": -90, "left": 180}[self.direction]
        self.img = pygame.transform.rotate(self.original_img, angle)
        self.rect = self.img.get_rect(center=self.rect.center)

    def can_see_target(self, target, blocks):
        x1, y1 = self.rect.center
        x2, y2 = target.rect.center
        dx = x2 - x1
        dy = y2 - y1
        steps = int(max(abs(dx), abs(dy)) // (self.rect.width // 2)) + 1
        if steps == 0:
            return False
        for i in range(1, steps):
            xi = x1 + dx * i / steps
            yi = y1 + dy * i / steps
            check_rect = pygame.Rect(xi - 5, yi - 5, 10, 10)
            for block in blocks:
                if block.rect.colliderect(check_rect):
                    return False
        return True

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.SHOT_DELAY:
            self.shoot_sound.play()
            x, y = self.rect.center
            return EnemyBullet(x, y, self.direction)
        return None

    def hit(self):
        self.health -= 1
        if self.health <= 0 and not self.destroyed:
            self.destroyed = True
            self.explosion_sound.play()

    def render(self, surf):
        if not self.destroyed:
            surf.blit(self.img, self.rect)

class EnemyBullet(Bullet):
    def __init__(self, x, y, direction):
        original = pygame.image.load("bullet_red.png").convert_alpha()
        scale_factor = 1.4
        width = int(original.get_width() * scale_factor)
        height = int(original.get_height() * scale_factor)
        scaled = pygame.transform.scale(original, (width, height))
        angle_map = {"up": 0, "right": -90, "down": 180, "left": 90}
        rotated = pygame.transform.rotate(scaled, angle_map[direction])
        self.img = rotated
        self.rect = self.img.get_rect(center=(x, y))

        self.dx, self.dy = {
            "up": (0, -Bullet.SPEED),
            "down": (0, Bullet.SPEED),
            "left": (-Bullet.SPEED, 0),
            "right": (Bullet.SPEED, 0)
        }[direction]

    def update(self, targets):
        self.rect.move_ip(self.dx, self.dy)
        for target in targets:
            if self.rect.colliderect(target.rect):
                if hasattr(target, "hit"):
                    target.hit()
                return False
        return True
