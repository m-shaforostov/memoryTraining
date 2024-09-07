import pygame
from sys import exit
from constants import (FPS, WIDTH, HEIGHT, PLAYERS, BUSH_STOP_IN_X, BUSH_STOP_OUT_X, TABLE_IN_SPEED, TABLE_OUT_SPEED,
                       TABLE_INITIAL)
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
                        if self.game_status == "wait_for_move_in":
                            self.game_status = "move_in"
                    elif event.button == 3:
                        if self.game_status == "game":
                            self.game_status = "move_out"
                            self.draw_background()
                            self.draw.move_character(self.game_level, self.game.characters)
                            self.draw.draw_leaves()


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
                self.draw_background()
                self.draw.draw_characters(self.game_level, self.game.characters)

                self.draw.bush_right_rect = self.draw.bush_right_rect.move(10, 0)
                self.draw.bush_left_rect = self.draw.bush_left_rect.move(-10, 0)
                self.draw.draw_leaves()
                print(self.table_index)

                if self.text_status == "greeting":
                    self.table_text = "Memorise!"
                if self.table_speed >= -15:
                    self.draw.move_table(self.table_speed, self.table_text)
                    self.table_speed -= self.speed_acceleration
                    self.speed_acceleration += self.gravity_acceleration
                else:
                    self.draw.move_table(0, self.table_text)

                if self.draw.bush_right_rect.centerx >= BUSH_STOP_IN_X:
                    self.game_status = "wait_for_move_in"
                    self.speed_acceleration = 1
                    self.table_speed += TABLE_OUT_SPEED
            if self.game_status == "move_in":
                self.draw_background()
                self.draw.draw_characters(self.game_level, self.game.characters)

                self.draw.bush_right_rect = self.draw.bush_right_rect.move(-10, 0)
                self.draw.bush_left_rect = self.draw.bush_left_rect.move(10, 0)
                self.draw.draw_leaves()

                self.draw.move_table(self.table_speed, self.table_text)
                self.table_speed += self.speed_acceleration
                self.speed_acceleration += self.gravity_acceleration

                if self.draw.bush_right_rect.topright[0] <= BUSH_STOP_OUT_X:
                    self.game_status = "game"
                    self.speed_acceleration = 1
                    self.table_speed = TABLE_IN_SPEED
                    self.draw.table_rect.center = TABLE_INITIAL
                    self.draw.table_rect.center = TABLE_INITIAL

            if self.game_status == "step":
                self.draw_background()
                self.draw.draw_leaves()
                # self.draw.move_character(self.game_level, self.game.characters)
                self.game_status = "game"

            pygame.display.update()
            self.clock.tick(FPS)

    def draw_background(self):
        self.draw.draw_water()
        self.draw.draw_planks()
        self.draw.draw_cells()

p = PygameLogic()