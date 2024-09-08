import pygame
from sys import exit
from constants import (FPS, WIDTH, HEIGHT, PLAYERS, BUSH_STOP_IN_X, BUSH_STOP_OUT_X, TABLE_IN_SPEED, TABLE_OUT_SPEED,
                       TABLE_INITIAL, TABLE_IN_SPEED_CENTER)
from draw_sprites import DrawScreen
from main import GameLogic

class PygameLogic:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('MindBlow')
        self.clock = pygame.time.Clock()

        self.draw = DrawScreen(self.screen)
        self.game = GameLogic()
        self.game_status = "lobby"
        self.text_status = "greeting"
        self.table_text = ""
        self.players_turn = 0
        self.table_index = 0
        self.table_speed = 0
        self.speed_acceleration = 1
        self.gravity_acceleration = 0.05

        self.game_level = 1
        self.cells_numb = 5


        self.update()

    def update(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.game_status == "game":
                            self.game_status = "step"
                            self.game.make_step(PLAYERS[self.players_turn])
                            self.players_turn = (self.players_turn + 1) % self.game_level
                            self.text_status = "step"
                            self.table_text = self.game.message

                        if self.game_status == "wait_for_move_in":
                            self.game_status = "move_in"

                    elif event.button == 3:
                        if self.game_status == "game":
                            self.game_status = "move_out"
                            self.draw_background()
                            game_result = self.draw.draw_characters(self.game_level, self.game.characters)
                            self.draw.draw_leaves()

                            if game_result:
                                self.text_status = "won"
                                self.table_speed = TABLE_IN_SPEED_CENTER
                            else:
                                self.text_status = "lose"
                                self.table_speed = TABLE_IN_SPEED_CENTER


            if self.game_status == "lobby":
                self.draw.draw_leaves()
                self.game_status = "start"

            if self.game_status == "start":
                self.draw_background()
                self.game.create_characters(self.game_level, self.cells_numb)
                self.draw.draw_characters(self.game_level, self.game.characters)
                self.game_status = "move_out"
                self.table_speed = TABLE_IN_SPEED

            if self.game_status == "move_out":
                if self.text_status == "greeting":
                    self.table_text = "Memorise!"
                elif self.text_status == "won":
                    self.table_text = "You won!"
                elif self.text_status == "lose":
                    self.table_text = "You lose"

                self.draw_background()
                self.draw.draw_characters(self.game_level, self.game.characters)
                fl = self.move_leaves_out()
                self.move_table_in()

                if fl:
                    self.game_status = "wait_for_move_in"
                    self.speed_acceleration = 1
                    self.table_speed += TABLE_OUT_SPEED

            if self.game_status == "move_in":
                self.draw_background()
                self.draw.draw_characters(self.game_level, self.game.characters)
                fl = self.move_leaves_in()
                self.move_table_out()

                if fl:
                    if self.text_status == "greeting":
                        self.game_status = "get_table"
                        self.text_status = "controllers_explanation"
                    elif self.text_status == "lose" or self.text_status == "won":
                        self.game_status = "start"
                        self.text_status = "greeting"
                    self.speed_acceleration = 1
                    self.table_speed = TABLE_IN_SPEED
                    self.draw.table_rect.center = TABLE_INITIAL

            if self.game_status == "get_table":
                if self.text_status == "controllers_explanation":
                    self.table_text = "Left btn - step\nRight btn - stop"
                self.draw.draw_leaves()
                fl = self.move_table_in()

                if fl:
                    self.game_status = "game"

            if self.game_status == "step":
                self.draw.draw_leaves()
                self.draw.draw_table(self.table_text)
                self.game_status = "game"

            pygame.display.update()
            self.clock.tick(FPS)

    def draw_background(self):
        self.draw.draw_water()
        self.draw.draw_planks()
        self.draw.draw_cells()

    def move_leaves_out(self):
        self.draw.bush_right_rect = self.draw.bush_right_rect.move(10, 0)
        self.draw.bush_left_rect = self.draw.bush_left_rect.move(-10, 0)
        self.draw.draw_leaves()

        if self.draw.bush_right_rect.centerx >= BUSH_STOP_IN_X:
            return True

    def move_leaves_in(self):
        self.draw.bush_right_rect = self.draw.bush_right_rect.move(-10, 0)
        self.draw.bush_left_rect = self.draw.bush_left_rect.move(10, 0)
        self.draw.draw_leaves()

        if self.draw.bush_right_rect.topright[0] <= BUSH_STOP_OUT_X:
            return True

    def move_table_in(self):
        if self.table_speed >= -15:
            self.draw.move_table(self.table_speed, self.table_text)
            self.table_speed -= self.speed_acceleration
            self.speed_acceleration += self.gravity_acceleration
        else:
            self.draw.move_table(0, self.table_text)
            return True

    def move_table_out(self):
        self.draw.move_table(self.table_speed, self.table_text)
        self.table_speed += self.speed_acceleration
        self.speed_acceleration += self.gravity_acceleration

p = PygameLogic()