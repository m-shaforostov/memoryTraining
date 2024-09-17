import pygame

from button import Button
from constants import (TABLE_INITIAL, LOBBY_BUTTON_WIDTH, LOBBY_BUTTON_HEIGHT, FLY_BUTTON_X, FLY_BUTTON_Y, BUG_BUTTON_Y,
                       BUG_BUTTON_X)

class Lobby:
    def __init__(self, screen):
        self.screen = screen

        self.fly_selection = Button("./img/Fly_button.png", "./img/Fly_button_hover.png",
                                    "./img/Fly_button_pressed.png", (FLY_BUTTON_X, FLY_BUTTON_Y))

        self.pixel_font_50 = pygame.font.Font(None, 50)
        self.pixel_font_100 = pygame.font.Font(None, 100)

    def characters_selection(self):
        self.fly_selection.draw_button(self.screen)