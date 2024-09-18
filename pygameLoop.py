import pygame
from sys import exit
from constants import (FPS, WIDTH, HEIGHT)

from draw_sprites import DrawScreen
from game_GUI import GameGUI
from lobby import Lobby

class PygameLogic:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('MindBlow')
        self.clock = pygame.time.Clock()

        self.lobby = Lobby(self.screen)
        self.game_gui = GameGUI(self.screen, ["fly"], 5)
        self.draw = DrawScreen(self.screen)

        self.game_status = "game"

        self.update()

    def update(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.game_status == "lobby":
                            self.lobby.mouse_pressed()
                            self.game_status = "game"
                        elif self.game_status == "game":
                            if self.game_gui.game_status == "wait":
                                self.game_gui.game_status = "overlay"
                            elif self.game_gui.game_status == "wait_for_new":
                                self.game_gui.game_status = "refresh"
                            elif self.game_gui.game_status == "movement_info":
                                self.game_gui.game_status = "step"

                    elif event.button == 3:
                        if self.game_status == "game":
                            if self.game_gui.game_status == "movement_info":
                                self.game_gui.game_status = "get_a_result"

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.game_status == "lobby":
                            self.lobby.mouse_released()

            if self.game_status == "lobby":
                self.lobby.draw_lobby()
            elif self.game_status == "game":
                self.game_gui.draw_game()
    #
            pygame.display.update()
            self.clock.tick(FPS)

p = PygameLogic()