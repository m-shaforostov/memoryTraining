import pygame
from constants import (TABLE_INITIAL)

class DrawTable:
    def __init__(self, screen):
        self.screen = screen
        self.pixel_font = pygame.font.Font(None, 50)

        self.table_text_surface = self.pixel_font.render("", False, "White")
        self.table_text_rect = self.table_text_surface.get_rect(center=TABLE_INITIAL)

        self.table_icon = pygame.image.load("./img/long_board.png").convert_alpha()
        self.table_icon = pygame.transform.scale_by(self.table_icon, 0.5)
        self.table_rect = self.table_icon.get_rect(center=TABLE_INITIAL)

        self.table_speed = 0
        self.table_text = ""
        self.speed_acceleration = 1
        self.gravity_acceleration = 0.05

    def move_table(self, move_to, text):
        self.table_rect = self.table_rect.move(0, move_to)
        self.screen.blit(self.table_icon, self.table_rect)

        self.draw_table_text(text)

    def draw_table(self, text):
        self.screen.blit(self.table_icon, self.table_rect)
        self.draw_table_text(text)

    def draw_table_text(self, text):
        text_arr = text.split('\n')
        for index, line in enumerate(text_arr):
            self.table_text_surface = self.pixel_font.render(line, False, "White")
            x = self.table_rect.centerx
            y = self.table_rect.centery - 50 * (len(text_arr) / 2 - 0.5)
            self.table_text_rect = self.table_text_surface.get_rect(center=(x, y + 50 * index))
            self.screen.blit(self.table_text_surface, self.table_text_rect)

    def move_table_in(self):
        if self.table_speed >= -15:
            print(self.table_speed, 111)
            self.move_table(self.table_speed, self.table_text)
            self.table_speed -= self.speed_acceleration
            self.speed_acceleration += self.gravity_acceleration
        else:
            self.move_table(0, self.table_text)
            return True

    def move_table_out(self):
        self.move_table(self.table_speed, self.table_text)
        self.table_speed += self.speed_acceleration
        self.speed_acceleration += self.gravity_acceleration