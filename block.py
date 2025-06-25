import pygame

class Block:
    def __init__(self, x, y, img, img_st2, img_st3,  destructible=True):
        self.img = img
        self.img_st2 = img_st2
        self.img_st3 = img_st3
        self.rect = self.img.get_rect(topleft=(x, y))
        self.destructible = destructible
        self.health = 3 if destructible else -1

    def render(self, surf):
        surf.blit(self.img, self.rect)
