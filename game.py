import pygame
import random
from player import Player
from block import Block
from enemy import Enemy
from bullet import Bullet

class Game:
    TILE_SIZE = 60 

    def __init__(self, screen, player_img, block_img, shoot_sound, explosion_sound, enemy_img, block_st2, block_st3, max_enemies):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.player_img = player_img
        self.block_img = block_img
        self.block_st2 = block_st2
        self.block_st3 = block_st3
        self.enemy_img = enemy_img
        self.shoot_sound = shoot_sound
        self.explosion_sound = explosion_sound
        self.font = pygame.font.SysFont("arial", 40)
        self.max_enemies = max_enemies
        try:
            self.background = pygame.image.load("background.png").convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except (pygame.error, FileNotFoundError):
            self.background = None

    def reset_game(self):
        self.blocks = []
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.game_over = False
        self.game_won = False
        self.map_width = self.width // self.TILE_SIZE
        self.map_height = self.height // self.TILE_SIZE
        self.tile_size = 48  
        

        self.level_map = [
            "  B   B   ",
            "          ",
            "   BBB   B",
            "          ",
            "       BB ",
            "  BB      ",
            "   B     B",
            "   BB   B ",
            "          ",
            "  B   BBB ",
        ]
        
        self.generate_border_blocks()
        self.generate_brick_blocks()

        px = self.width // 2
        py = self.height // 2
        self.player = Player(px, py, self.player_img, self.shoot_sound, self.explosion_sound)


        all_positions = []
        for y in range(1, self.map_height - 1):
            for x in range(1, self.map_width - 1):
                all_positions.append((
                    x * self.tile_size + self.tile_size // 2,
                    y * self.tile_size + self.tile_size // 2
                ))
        

        enemy_size = self.enemy_img.get_rect().size
        spawn_positions = []
        
        for pos in all_positions:
            x, y = pos
            can_spawn = True
            enemy_rect = pygame.Rect(0, 0, *enemy_size)
            enemy_rect.center = (x, y)
            

            for block in self.blocks:
                if block.rect.colliderect(enemy_rect):
                    can_spawn = False
                    break
            

            if can_spawn:
                player_dist = pygame.math.Vector2(x - px, y - py).length()
                if player_dist < 200: 
                    can_spawn = False
            
            if can_spawn:
                spawn_positions.append(pos)
        
        random.shuffle(spawn_positions)
        

        spawn_positions = spawn_positions[:min(len(spawn_positions), self.max_enemies * 3)]
        

        spawned = 0
        for pos in spawn_positions:
            if spawned >= self.max_enemies:
                break
                
            x, y = pos
            enemy = Enemy(x, y, self.enemy_img, self.shoot_sound, self.explosion_sound)
            self.enemies.append(enemy)
            spawned += 1

    def generate_brick_blocks(self):
        for row_index, row in enumerate(self.level_map):
            for col_index, cell in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                if cell == "B":
                    self.blocks.append(Block(x, y, self.block_img, self.block_st2, self.block_st3, destructible=True))

    def generate_border_blocks(self):
        cols = self.width // self.tile_size
        rows = self.height // self.tile_size
        for x in range(cols):
            for y in (0, rows - 1):
                self.blocks.append(Block(x * self.tile_size, y * self.tile_size, self.block_img, self.block_st2, self.block_st3, destructible=False))
        for y in range(1, rows - 1):
            for x in (0, cols - 1):
                self.blocks.append(Block(x * self.tile_size, y * self.tile_size, self.block_img, self.block_st2, self.block_st3, destructible=False))

    def update(self):
        if self.game_over or self.game_won:
            return
        keys = pygame.key.get_pressed()
        shot = self.player.move(keys, self.blocks)
        if shot:
            x, y = self.player.rect.center
            direction = self.player.direction
            self.bullets.append(Bullet(x, y, direction, image_path="bullet_green.png", scale=0.7))
            self.shoot_sound.play()
        for enemy in self.enemies:
            bullet = enemy.update(self.player, self.blocks)
            if bullet:
                self.enemy_bullets.append(bullet)
                self.shoot_sound.play()
        self.enemies = [enemy for enemy in self.enemies if not enemy.destroyed]
        for bullet in self.bullets[:]:
            alive = bullet.update(self.blocks, self.enemies)
            if not alive or bullet.off_screen(self.screen):
                self.bullets.remove(bullet)
        for e_bullet in self.enemy_bullets[:]:
            alive = e_bullet.update(self.blocks, [self.player])
            if not alive or e_bullet.off_screen(self.screen):
                self.enemy_bullets.remove(e_bullet)
        if self.player.health <= 0:
            self.game_over = True
        if len(self.enemies) == 0:
            self.game_won = True

    def render(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((255, 255, 255))
        for block in self.blocks:
            block.render(self.screen)
        for bullet in self.bullets:
            bullet.render(self.screen)
        for e_bullet in self.enemy_bullets:
            e_bullet.render(self.screen)
        self.player.render(self.screen)
        for enemy in self.enemies:
            enemy.render(self.screen)
        if self.game_over:
            self.show_restart_screen()
        elif self.game_won:
            self.show_win_screen()

    def show_restart_screen(self):
        text = self.font.render("Game Over", True, (255, 0, 0))
        btn = self.font.render("Press R to Restart", True, (0, 0, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 60))
        self.screen.blit(btn, (self.width // 2 - btn.get_width() // 2, self.height // 2 + 10))

    def show_win_screen(self):
        text = self.font.render("You Win!", True, (0, 128, 0))
        btn_restart = self.font.render("Press R to Restart", True, (0, 0, 0))
        btn_exit = self.font.render("Press Q to Quit", True, (0, 0, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 80))
        self.screen.blit(btn_restart, (self.width // 2 - btn_restart.get_width() // 2, self.height // 2))
        self.screen.blit(btn_exit, (self.width // 2 - btn_exit.get_width() // 2, self.height // 2 + 60))

    def handle_events(self, event):
        if self.game_over or self.game_won:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    return "quit_to_menu"
        return None