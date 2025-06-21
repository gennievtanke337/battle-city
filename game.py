import pygame
from player import Player
from block import Block

class Game:
    def __init__(self, screen, logger, player_img, block_img, shoot_sound, explosion_sound):
        self.screen = screen
        self.logger = logger
        self.player = Player(60, 400, player_img, shoot_sound, explosion_sound, logger)
        self.blocks = []

        
        for x in range(0, 640, 60):
            if x not in [0, 60, 120]:
                self.blocks.append(Block(x, 100, block_img))
                self.blocks.append(Block(x, 300, block_img))

        
        for y in range(160, 280, 60):
            self.blocks.append(Block(200, y, block_img))
            self.blocks.append(Block(400, y, block_img))

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.blocks)

    def render(self):
        self.screen.fill((220, 220, 220))
        for block in self.blocks:
            block.render(self.screen)
        self.player.render(self.screen)
