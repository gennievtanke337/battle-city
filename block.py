import pygame

class Block:
    def __init__(self, x, y, img, indestructible=False):
        self.img = img
        self.rect = self.img.get_rect(topleft=(x, y))
        self.health = 3 if not indestructible else -1
        self.indestructible = indestructible
        self.destroyed = False

    def hit(self):
        if self.indestructible:
            return
        self.health -= 1
        if self.health <= 0:
            self.destroyed = True

    def render(self, surf):
        if not self.destroyed:
            surf.blit(self.img, self.rect)
