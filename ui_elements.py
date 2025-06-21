import pygame

class Button:
    def __init__(self, text, pos, size):
        self.rect = pygame.Rect(pos, size)
        self.text = text
        self.font = pygame.font.SysFont(None, 30)
        self.color = (80, 160, 200)

    def render(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
        txt = self.font.render(self.text, True, (255,255,255))
        surf.blit(txt, (self.rect.x+20, self.rect.y+10))

    def is_clicked(self, evt):
        return evt.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evt.pos)
