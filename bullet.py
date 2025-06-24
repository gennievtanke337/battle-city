import pygame

class Bullet:
    SPEED = 6

    def __init__(self, x, y, direction):
        original = pygame.image.load("bullet_green.png").convert_alpha()

        scale_factor = 0.7  
        width = int(original.get_width() * scale_factor)
        height = int(original.get_height() * scale_factor)

        scaled = pygame.transform.scale(original, (width, height))

        angle_map = {"up": 0, "right": -90, "down": 180, "left": 90}
        rotated = pygame.transform.rotate(scaled, angle_map[direction])
        self.img = rotated
        self.rect = self.img.get_rect(center=(x, y))

        self.dx, self.dy = {
            "up": (0, -self.SPEED),
            "down": (0, self.SPEED),
            "left": (-self.SPEED, 0),
            "right": (self.SPEED, 0)
        }[direction]

    def update(self, targets):
        self.rect.move_ip(self.dx, self.dy)
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
