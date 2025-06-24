import pygame

class Block:
    def __init__(self, x, y, img, destructible=True):
        self.img = img
        self.rect = self.img.get_rect(topleft=(x, y))
        self.destructible = destructible
        self.health = 3 if destructible else None

    def hit(self):
        if self.destructible and self.health is not None:
            self.health -= 1
            if self.health <= 0:
                return True
        return False

    def render(self, surf):
        surf.blit(self.img, self.rect)
