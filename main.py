import pygame
from game import Game

pygame.init()

screen_width = int(1920 * 0.75)
screen_height = int(720 * 0.75)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battle City Remake")
clock = pygame.time.Clock()

player_img = pygame.image.load("player_tank.png").convert_alpha()
block_img = pygame.image.load("barrel.png").convert_alpha()
shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 72)
        self.button_rect = pygame.Rect(0, 0, 300, 100)
        self.button_rect.center = (screen_width // 2, screen_height // 2)

    def draw(self):
        self.screen.fill((50, 50, 50))
        text = self.font.render("START", True, (255, 255, 255))
        pygame.draw.rect(self.screen, (100, 100, 200), self.button_rect)
        self.screen.blit(text, text.get_rect(center=self.button_rect.center))

    def check_click(self, pos):
        return self.button_rect.collidepoint(pos)

menu = Menu(screen)
game = None
in_menu = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if in_menu and event.type == pygame.MOUSEBUTTONDOWN:
            if menu.check_click(event.pos):
                game = Game(screen, player_img, block_img, shoot_sound, explosion_sound)
                in_menu = False

    if in_menu:
        menu.draw()
    else:
        game.update()
        game.render()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
