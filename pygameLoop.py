import pygame
from sys import exit
from constants import FPS, WIDTH, HEIGHT, PLAYERS, BUSH_STOP_X
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
        self.players_turn = 0

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
            if self.game_status == "lobby":
                self.draw.draw_leaves()
                self.game_status = "start"
            if self.game_status == "start":
                self.draw_background()
                self.game.create_characters(self.game_level, self.cells_numb)
                self.draw.draw_characters(self.game_level, self.game.characters)
                self.game_status = "move"
            if self.game_status == "move":
                self.draw_background()
                self.draw.draw_characters(self.game_level, self.game.characters)

                self.draw.bush_right_rect = self.draw.bush_right_rect.move(5, 0)
                self.draw.bush_left_rect = self.draw.bush_left_rect.move(-5, 0)
                self.draw.draw_leaves()

                if self.draw.bush_right_rect.centerx >= BUSH_STOP_X:
                    self.game_status = "game"
            if self.game_status == "step":
                self.draw_background()
                self.draw.draw_leaves()
                self.draw.move_character(self.game_level, self.game.characters)
                self.game_status = "game"

            pygame.display.update()
            self.clock.tick(FPS)

    def draw_background(self):
        self.draw.draw_water()
        self.draw.draw_planks()
        self.draw.draw_cells()

p = PygameLogic()