import pygame

class Block:
    def __init__(self, x, y, img):
        self.rect = img.get_rect(topleft=(x, y))
        self.img = img

    def render(self, surf):
        surf.blit(self.img, self.rect)
