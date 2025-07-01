import pygame
from game import Game

pygame.init()
pygame.mixer.init()

screen_width = 576
screen_height = 576
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battle City Remake")
clock = pygame.time.Clock()

player_img = pygame.image.load("player_tank.png").convert_alpha()
block_img = pygame.image.load("block_new_1.png").convert_alpha()
block_st2_img = pygame.image.load("block_new_2.png").convert_alpha()
block_st3_img = pygame.image.load("block_new_3.png").convert_alpha()
enemy_img = pygame.image.load("enemy_tank.png").convert_alpha()

new_size = (48, 48)
player_img = pygame.transform.scale(player_img, new_size)
enemy_img = pygame.transform.scale(enemy_img, new_size)
block_img = pygame.transform.scale(block_img, new_size)
block_st2_img = pygame.transform.scale(block_st2_img, new_size)
block_st3_img = pygame.transform.scale(block_st3_img, new_size)

shoot_sound = pygame.mixer.Sound("shoot_sound.wav")
explosion_sound = pygame.mixer.Sound("explosion_sound.wav")

menu_music = "menu_background_music.mp3"
game_music = "game_background_music.mp3"

font = pygame.font.SysFont(None, 72)
title_text = font.render("Battle City Remake", True, (255, 255, 255))
start_text = font.render("1-Easy  2-Medium  3-Hard", True, (255, 255, 255))

def play_music(file, loops=-1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops)

def stop_music():
    pygame.mixer.music.stop()

def game_loop(enemy_count):
    game = Game(screen, player_img, block_img, shoot_sound, explosion_sound, enemy_img, block_st2_img, block_st3_img, enemy_count)
    game.reset_game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            result = game.handle_events(event)
            if result == "quit_to_menu":
                return True
        game.update()
        game.render()
        pygame.display.flip()
        clock.tick(60)
    return True

def main():
    in_menu = True
    running = True
    play_music(menu_music)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if in_menu and event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    stop_music()
                    play_music(game_music)
                    enemies = 3 if event.key == pygame.K_1 else 5 if event.key == pygame.K_2 else 7
                    result = game_loop(enemies)
                    stop_music()
                    play_music(menu_music)
                    in_menu = True
                    if not result:
                        running = False
        screen.fill((0, 0, 0))
        if in_menu:
            screen.blit(title_text, ((screen_width - title_text.get_width()) // 2, screen_height // 3))
            screen.blit(start_text, ((screen_width - start_text.get_width()) // 2, screen_height // 2))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
