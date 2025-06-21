import pygame
from game import Game
from ui_elements import Button

class SceneManager:
    def __init__(self, screen, logger, player_img, block_img, shoot_sound, explosion_sound):
        self.screen = screen
        self.logger = logger
        self.player_img = player_img
        self.block_img = block_img
        self.shoot_sound = shoot_sound
        self.explosion_sound = explosion_sound
        self.scene = "menu"
        self.game = Game(screen, logger, player_img, block_img, shoot_sound, explosion_sound)
        self.start_btn = Button("Start Game", (220, 200), (200, 50))

    def handle_event(self, evt):
        if self.scene == "menu" and self.start_btn.is_clicked(evt):
            self.logger.log("Game started")
            self.scene = "game"

    def update(self):
        if self.scene == "game":
            self.game.update()

    def render(self):
        self.screen.fill((30, 30, 30))
        if self.scene == "menu":
            self.start_btn.render(self.screen)
        if self.scene == "game":
            self.game.render()
