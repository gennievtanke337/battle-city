import pygame
import math

class Bullet:
    SPEED = 5

    def __init__(self, x, y, direction, image_path="bullet_green.png", scale=0.7):
        original = pygame.image.load(image_path).convert_alpha()
        width = int(original.get_width() * scale)
        height = int(original.get_height() * scale)
        scaled = pygame.transform.scale(original, (width, height))

        angle_map = {
            "up": 0,
            "right": -90,
            "down": 180,
            "left": 90
        }

        self.img = pygame.transform.rotate(scaled, angle_map[direction])
        self.rect = self.img.get_rect(center=(x, y))

        self.dx, self.dy = {
            "up": (0, -self.SPEED),
            "down": (0, self.SPEED),
            "left": (-self.SPEED, 0),
            "right": (self.SPEED, 0)
        }[direction]

    def update(self, blocks, targets):
        self.rect.move_ip(self.dx, self.dy)

        for block in blocks:
            if block.destructible and self.rect.colliderect(block.rect):
                    block.health -= 1
                    if block.health == 2:
                        block.img = block.img_st2
                    elif block.health == 1:
                        block.img = block.img_st3
                    if block.health <= 0:
                        blocks.remove(block)

                    return False

        for target in targets:
            if self.rect.colliderect(target.rect):
                if hasattr(target, "hit"):
                    target.hit()
                return False
        return True

    def off_screen(self, screen):
        return not screen.get_rect().colliderect(self.rect.inflate(20, 20))

    def render(self, surf):
        surf.blit(self.img, self.rect)
