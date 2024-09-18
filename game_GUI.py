from draw_characters import DrawCharacters
from draw_sprites import DrawScreen
from draw_table import DrawTable
from game_logic import GameLogic

from constants import TABLE_IN_SPEED, TABLE_OUT_SPEED, BUSH_STOP_OUT_X, BUSH_STOP_IN_X, TABLE_INITIAL, \
    TABLE_IN_SPEED_CENTER, PLAYERS
from sound_logic import SoundEffects


class GameGUI:
    def __init__(self, screen, characters, cells):
        self.screen = screen

        self.game = GameLogic()
        self.character = DrawCharacters(self.screen)
        self.draw = DrawScreen(self.screen)
        self.table = DrawTable(self.screen)
        self.play = SoundEffects()

        self.characters_n = len(characters)
        self.cells_n = cells

        self.text_status = ""
        self.whose_turn = 0

        self.game_status = "initiate"
        self.status_actions = {
            'initiate': self.initiate,
            'open_field': self.open_field,
            'wait': self.wait_for_action,
            'overlay': self.overlay_field,
            'controllers_explanation': self.controllers_explanation,
            'step': self.step,
            'get_a_result': self.get_result,
            'show_result': self.show_result,
            'refresh': self.refresh_game,
        }


    def draw_game(self):
        exceptions = ['movement_info', 'wait', 'wait_for_new']
        if self.game_status not in exceptions:
            self.status_actions[self.game_status]()

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

            if self.table.table_text == "Memorise!":
                self.play.play_memorise()

    def wait_for_action(self):
        self.draw_background()
        self.character.draw_characters(self.characters_n, self.game.characters)
        self.draw.leaves()
        self.table.draw_table(self.table.table_text)

    def overlay_field(self):
        self.draw_background()
        self.character.draw_characters(self.characters_n, self.game.characters)
        fl = self.move_leaves_in()
        self.table.move_table_out()

        if fl:
            self.table.speed_acceleration = 1
            self.table.table_speed = TABLE_IN_SPEED
            self.table.table_rect.center = TABLE_INITIAL
            self.game_status = "controllers_explanation"

    def controllers_explanation(self):
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
        self.play.play_step(PLAYERS[self.whose_turn], self.game.current_step)
        self.game_status = "movement_info"

    def get_result(self):
        result = self.character.draw_characters(self.characters_n, self.game.characters)
        self.draw.leaves()
        if result:
            self.table.table_text = "You win!"
            self.play.play_result(1)
        else:
            self.table.table_text = "You lose!"
            self.play.play_result(0)
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

    def refresh_game(self):
        self.draw_background()
        self.character.draw_characters(self.characters_n, self.game.characters)
        fl = self.move_leaves_in()
        self.table.move_table_out()

        if fl:
            self.table.speed_acceleration = 1
            self.table.table_speed = TABLE_IN_SPEED
            self.table.table_rect.center = TABLE_INITIAL
            self.game_status = "initiate"

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