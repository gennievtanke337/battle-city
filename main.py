import pygame
from scene_manager import SceneManager
from logger import Logger

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
logger = Logger("game.log")

player_img = pygame.image.load("player_tank.png").convert_alpha()
block_img = pygame.image.load("barrel.png").convert_alpha()
shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")

scene_manager = SceneManager(screen, logger, player_img, block_img, shoot_sound, explosion_sound)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene_manager.handle_event(event)
    scene_manager.update()
    scene_manager.render()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
