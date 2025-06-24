import pygame

class Player:
    def __init__(self, x, y, img, shoot_sound, explosion_sound):
        self.original_img = img
        self.img = img
        self.rect = self.img.get_rect(center=(x, y))
        self.shoot_sound = shoot_sound
        self.explosion_sound = explosion_sound
        self.last_shot_time = 0
        self.shot_delay = 600
        self.direction = "up"
        self.health = 3

    def move(self, keys, blocks):
        dx = dy = 0
        if keys[pygame.K_a]:
            dx = -3; self.direction = "left"
        elif keys[pygame.K_d]:
            dx = 3; self.direction = "right"
        elif keys[pygame.K_w]:
            dy = -3; self.direction = "up"
        elif keys[pygame.K_s]:
            dy = 3; self.direction = "down"

        new_rect = self.rect.move(dx, dy)
        if not any(new_rect.colliderect(b.rect.inflate(-8, -8)) for b in blocks):
            self.rect = new_rect

        self.rotate_image()
        if keys[pygame.K_SPACE]:
            return self.shoot()
        return False

    def rotate_image(self):
        angle = {"up": 90, "right": 0, "down": -90, "left": 180}[self.direction]
        self.img = pygame.transform.rotate(self.original_img, angle)
        self.rect = self.img.get_rect(center=self.rect.center)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shot_delay:
            self.shoot_sound.play()
            self.last_shot_time = now
            return True
        return False

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.explosion_sound.play()

    def render(self, surf):
        surf.blit(self.img, self.rect)
