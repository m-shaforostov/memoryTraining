import pygame
from sys import exit
from constants import (FPS, WIDTH, HEIGHT, PLAYERS, BUSH_STOP_IN_X, BUSH_STOP_OUT_X, TABLE_IN_SPEED, TABLE_OUT_SPEED,
                       TABLE_INITIAL, TABLE_IN_SPEED_CENTER)

from draw_characters import DrawCharacters
from draw_sprites import DrawScreen
from draw_table import DrawTable
from game_GUI import GameGUI
from lobby import Lobby
from game_logic import GameLogic
from sound_logic import SoundEffects

class PygameLogic:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('MindBlow')
        self.clock = pygame.time.Clock()

        self.lobby = Lobby(self.screen)
        self.game_gui = GameGUI(self.screen, ["fly"], 5)
        self.draw = DrawScreen(self.screen)
        self.play = SoundEffects()

        self.game_status = "lobby"
        self.text_status = "greeting"
        self.table_index = 0


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
                                # self.table.table_text = self.game.message

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

            if self.game_status == "game":
                self.game_gui.draw_game()
    #             self.draw_background()
    #             self.game.create_characters(self.game_level, self.cells_numb)
    #             self.character.draw_characters(self.game_level, self.game.characters)
    #             self.game_status = "move_out"
    #             self.table.table_speed = TABLE_IN_SPEED
    #
    #         if self.game_status == "move_out":
    #             if self.text_status == "greeting":
    #                 self.table.table_text = "Memorise!"
    #             elif self.text_status == "won":
    #                 self.table.table_text = "You won!"
    #             elif self.text_status == "lose":
    #                 self.table.table_text = "You lose"
    #
    #             self.draw_background()
    #             self.character.draw_characters(self.game_level, self.game.characters)
    #             fl = self.move_leaves_out()
    #             self.table.move_table_in()
    #
    #             if fl:
    #                 self.game_status = "wait_for_move_in"
    #                 self.table.speed_acceleration = 1
    #                 self.table.table_speed += TABLE_OUT_SPEED
    #
    #                 if self.text_status == "greeting":
    #                     self.play.play_memorise()
    #                 elif self.text_status == "won":
    #                     self.play.play_result(1)
    #                 elif self.text_status == "lose":
    #                     self.play.play_result(0)
    #
    #         if self.game_status == "move_in":
    #             self.draw_background()
    #             self.character.draw_characters(self.game_level, self.game.characters)
    #             fl = self.move_leaves_in()
    #             self.table.move_table_out()
    #
    #             if fl:
    #                 if self.text_status == "greeting":
    #                     self.game_status = "get_table"
    #                     self.text_status = "controllers_explanation"
    #                 elif self.text_status == "lose" or self.text_status == "won":
    #                     self.game_status = "start"
    #                     self.text_status = "greeting"
    #                 self.table.speed_acceleration = 1
    #                 self.table.table_speed = TABLE_IN_SPEED
    #                 self.table.table_rect.center = TABLE_INITIAL
    #
    #         if self.game_status == "get_table":
    #             if self.text_status == "controllers_explanation":
    #                 self.table.table_text = "Left btn - step\nRight btn - stop"
    #             self.draw.leaves()
    #             fl = self.table.move_table_in()
    #
    #             if fl:
    #                 self.game_status = "game"
    #
    #         if self.game_status == "step":
    #             self.draw.leaves()
    #             self.table.draw_table(self.table.table_text)
    #             self.play.play_step(PLAYERS[self.players_turn], self.game.current_step)
    #             self.game_status = "game"
    #
            pygame.display.update()
            self.clock.tick(FPS)
    #
    # def draw_background(self):
    #     self.draw.water()
    #     self.draw.planks()
    #     self.draw.cells()
    #
    # def move_leaves_out(self):
    #     self.draw.bush_right_rect = self.draw.bush_right_rect.move(10, 0)
    #     self.draw.bush_left_rect = self.draw.bush_left_rect.move(-10, 0)
    #     self.draw.leaves()
    #
    #     if self.draw.bush_right_rect.centerx >= BUSH_STOP_OUT_X:
    #         return True
    #
    # def move_leaves_in(self):
    #     self.draw.bush_right_rect = self.draw.bush_right_rect.move(-10, 0)
    #     self.draw.bush_left_rect = self.draw.bush_left_rect.move(10, 0)
    #     self.draw.leaves()
    #
    #     if self.draw.bush_right_rect.topright[0] <= BUSH_STOP_IN_X:
    #         return True

p = PygameLogic()