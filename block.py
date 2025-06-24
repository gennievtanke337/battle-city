import pygame

class Block:
    def __init__(self, x, y, img, destructible=True):
        self.img = img
        self.rect = self.img.get_rect(topleft=(x, y))
        self.destructible = destructible
        self.health = 3 if destructible else -1

    def render(self, surf):
        surf.blit(self.img, self.rect)
