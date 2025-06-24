import pygame
from game import Game

pygame.init()
pygame.mixer.init()

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

menu_music = "menu_background_music.mp3"
game_music = "game_background_music.mp3"

font = pygame.font.SysFont(None, 72)
title_text = font.render("Battle City Remake", True, (255, 255, 255))
start_text = font.render("Press ENTER to Start", True, (255, 255, 255))

def play_music(file, loops=-1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops)

def stop_music():
    pygame.mixer.music.stop()

def main():
    in_menu = True
    running = True
    play_music(menu_music)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if in_menu and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    in_menu = False
                    stop_music()
                    play_music(game_music)
                    if not game_loop():
                        running = False
                    else:
                        in_menu = True
                        stop_music()
                        play_music(menu_music)

        screen.fill((0, 0, 0))
        if in_menu:
            screen.blit(title_text, ((screen_width - title_text.get_width()) // 2, screen_height // 3))
            screen.blit(start_text, ((screen_width - start_text.get_width()) // 2, screen_height // 2))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def game_loop():
    game = Game(screen, player_img, block_img, shoot_sound, explosion_sound, enemy_img)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        game.update()
        game.render()
        pygame.display.flip()
        clock.tick(60)
    return True

if __name__ == "__main__":
    main()
