import pygame

from button import Button
from constants import (FLY_BUTTON_X, FLY_BUTTON_Y, BUG_BUTTON_Y,
                       BUG_BUTTON_X, FROG_BUTTON_Y, FROG_BUTTON_X)
from draw_sprites import DrawScreen


class Lobby:
    def __init__(self, screen):
        self.screen = screen

        self.fly_button = Button("./img/Fly_button.png", "./img/Fly_button_hover.png",
                                    "./img/Fly_button_pressed.png", (FLY_BUTTON_X, FLY_BUTTON_Y))
        self.bug_button = Button("./img/Bug_button.png", "./img/Bug_button_hover.png",
                                    "./img/Bug_button_pressed.png", (BUG_BUTTON_X, BUG_BUTTON_Y))
        self.frog_button = Button("./img/Frog_button.png", "./img/Frog_button_hover.png",
                                    "./img/Frog_button_pressed.png", (FROG_BUTTON_X, FROG_BUTTON_Y))

        self.pixel_font_50 = pygame.font.Font(None, 50)
        self.pixel_font_100 = pygame.font.Font(None, 100)

        self.draw = DrawScreen(screen)

    def characters_selection(self):
        self.fly_button.draw(self.screen)
        self.bug_button.draw(self.screen)
        self.frog_button.draw(self.screen)

    def draw_lobby(self):
        self.draw.leaves()
        self.characters_selection()

    def mouse_pressed(self):
        if self.fly_button.is_hovered():
            self.fly_button.press()

        if self.bug_button.is_hovered():
            self.bug_button.press()

        if self.frog_button.is_hovered():
            self.frog_button.press()

    def mouse_released(self):
        self.fly_button.release()
        self.bug_button.release()
        self.frog_button.release()