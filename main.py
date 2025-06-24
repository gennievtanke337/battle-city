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
enemy_img = pygame.image.load("enemy_tank.png").convert_alpha()
shoot_sound = pygame.mixer.Sound("shoot_sound.wav")
explosion_sound = pygame.mixer.Sound("explosion_sound.wav")


game = Game(screen, player_img, block_img, shoot_sound, explosion_sound, enemy_img, )

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.update()
    game.render()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
