import pygame

class Player:
    def __init__(self, x, y, img, shoot_sound, explosion_sound, logger):
        self.original_img = img
        self.img = img
        self.rect = self.img.get_rect(topleft=(x, y))
        self.shoot_sound = shoot_sound
        self.explosion_sound = explosion_sound
        self.logger = logger
        self.last_shot_time = 0
        self.shot_delay = 1000
        self.direction = "up"

    def move(self, keys, blocks):
        dx = dy = 0
        if keys[pygame.K_a]:
            dx = -3
            self.direction = "left"
        elif keys[pygame.K_d]:
            dx = 3
            self.direction = "right"
        elif keys[pygame.K_w]:
            dy = -3
            self.direction = "up"
        elif keys[pygame.K_s]:
            dy = 3
            self.direction = "down"

        new_rect = self.rect.move(dx, dy)
        if not any(new_rect.colliderect(b.rect) for b in blocks):
            self.rect = new_rect

        self.rotate_image()

        if keys[pygame.K_SPACE]:
            self.shoot()

    def rotate_image(self):
        angle = {"up": 90, "right": 0, "down": -90, "left": 180}[self.direction]
        self.img = pygame.transform.rotate(self.original_img, angle)
        self.rect = self.img.get_rect(center=self.rect.center)


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shot_delay:
            self.shoot_sound.play()
            self.logger.log("Player shot")
            self.last_shot_time = now

    def render(self, surf):
        surf.blit(self.img, self.rect)
