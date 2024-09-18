from draw_characters import DrawCharacters
from draw_sprites import DrawScreen
from draw_table import DrawTable
from game_logic import GameLogic

from constants import TABLE_IN_SPEED, TABLE_OUT_SPEED, BUSH_STOP_OUT_X, BUSH_STOP_IN_X, TABLE_INITIAL, \
    TABLE_IN_SPEED_CENTER, PLAYERS


class GameGUI:
    def __init__(self, screen, characters, cells):
        self.screen = screen

        self.game = GameLogic()
        self.character = DrawCharacters(self.screen)
        self.draw = DrawScreen(self.screen)
        self.table = DrawTable(self.screen)

        self.characters_n = len(characters)
        self.cells_n = cells

        self.game_status = "initiate"
        self.status_actions = {
            'initiate': self.initiate(),
            'open_field': self.open_field(),
        }
        self.text_status = ""
        self.whose_turn = 0


    def draw_game(self):
        if self.game_status == "initiate":
            self.initiate()

        if self.game_status == "open_field":
            self.open_field()

        if self.game_status == "wait":
            self.wait_for_action()

        if self.game_status == "overlay":
            self.overlay_field("get_table")

        if self.game_status == "get_table":
            self.get_table()

        if self.game_status == "step":
            self.step()

        if self.game_status == "get_a_result":
            # self.open_field()
            self.get_result()

        if self.game_status == "show_result":
            self.show_result()

        if self.game_status == "refresh":
            self.overlay_field("initiate")


    def initiate(self):
        self.draw_background()
        self.game.create_characters(self.characters_n, self.cells_n)
        self.character.draw_characters(self.characters_n, self.game.characters)
        self.draw.leaves()

        self.table.table_text = "Memorise!"
        self.table.table_speed = TABLE_IN_SPEED
        self.game_status = "open_field"

    def open_field(self):
        self.draw_background()
        self.character.draw_characters(self.characters_n, self.game.characters)
        fl = self.move_leaves_out()
        self.table.move_table_in()

        if fl:
            self.table.speed_acceleration = 1
            self.table.table_speed += TABLE_OUT_SPEED
            self.game_status = "wait"

            # if self.text_status == "greeting":
            #     self.play.play_memorise()
            # elif self.text_status == "won":
            #     self.play.play_result(1)
            # elif self.text_status == "lose":
            #     self.play.play_result(0)

    def wait_for_action(self):
        self.draw_background()
        self.character.draw_characters(self.characters_n, self.game.characters)
        self.draw.leaves()
        self.table.draw_table(self.table.table_text)

    def overlay_field(self, next):
        self.draw_background()
        self.character.draw_characters(self.characters_n, self.game.characters)
        fl = self.move_leaves_in()
        self.table.move_table_out()

        if fl:
            self.table.speed_acceleration = 1
            self.table.table_speed = TABLE_IN_SPEED
            self.table.table_rect.center = TABLE_INITIAL
            self.game_status = next

    def get_table(self):
        # if self.text_status == "controllers_explanation":
        self.table.table_text = "Left btn - step\nRight btn - stop"
        self.draw.leaves()
        fl = self.table.move_table_in()

        if fl:
            self.game_status = "movement_info"

    def step(self):
        self.draw.leaves()

        self.whose_turn = (self.whose_turn + 1) % self.characters_n
        self.game.make_step(PLAYERS[self.whose_turn])
        self.table.table_text = self.game.message
        self.table.draw_table(self.table.table_text)
        # self.play.play_step(PLAYERS[self.players_turn], self.game.current_step)
        self.game_status = "movement_info"

    def get_result(self):
        result = self.character.draw_characters(self.characters_n, self.game.characters)
        if result:
            self.table.table_text = "You win!"
        else:
            self.table.table_text = "You lose!"
        self.table.table_speed = TABLE_IN_SPEED
        self.table.speed_acceleration = 1
        self.game_status = "show_result"

    def show_result(self):
        self.draw_background()
        self.character.draw_characters(self.characters_n, self.game.characters)
        fl = self.move_leaves_out()
        self.table.move_table_in()

        if fl:
            self.table.speed_acceleration = 1
            self.table.table_speed += TABLE_OUT_SPEED
            self.game_status = "wait_for_new"

    def draw_background(self):
        self.draw.water()
        self.draw.planks()
        self.draw.cells()

    def move_leaves_out(self):
        self.draw.bush_right_rect = self.draw.bush_right_rect.move(10, 0)
        self.draw.bush_left_rect = self.draw.bush_left_rect.move(-10, 0)
        self.draw.leaves()

        if self.draw.bush_right_rect.centerx >= BUSH_STOP_OUT_X:
            return True

    def move_leaves_in(self):
        self.draw.bush_right_rect = self.draw.bush_right_rect.move(-10, 0)
        self.draw.bush_left_rect = self.draw.bush_left_rect.move(10, 0)
        self.draw.leaves()

        if self.draw.bush_right_rect.topright[0] <= BUSH_STOP_IN_X:
            return True