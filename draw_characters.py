import pygame
from constants import (PLANKS_X, PLANKS_Y,
    CELLS_X, CELLS_Y, CELLS_GAP_X, CELLS_GAP_Y, CELL_SIZE, PLAYERS)

class DrawCharacters:
    def __init__(self, screen):
        self.screen = screen
        self.pixel_font = pygame.font.Font(None, 50)

        self.fly_icon = pygame.image.load("./img/Fly.png").convert_alpha()
        self.fly_icon = pygame.transform.scale(self.fly_icon, (CELL_SIZE, CELL_SIZE))
        self.fly_d_icon = pygame.image.load("./img/Fly_d.png").convert_alpha()
        self.fly_d_icon = pygame.transform.scale(self.fly_d_icon, (CELL_SIZE, CELL_SIZE))

        # self.frog_icon = pygame.image.load("./img/cell2.png").convert_alpha()
        # self.frog_icon = pygame.transform.scale(self.frog_icon, (CELL_SIZE, CELL_SIZE))

        # self.fly_icon = pygame.image.load("./img/cell2.png").convert_alpha()
        # self.fly_icon = pygame.transform.scale(self.fly_icon, (CELL_SIZE, CELL_SIZE))

        self.green_tick_icon = pygame.image.load("./img/green_tick.png").convert_alpha()
        self.green_tick_icon = pygame.transform.scale(self.green_tick_icon, (CELL_SIZE / 4, CELL_SIZE / 4))

        self.players_icons = [self.fly_icon]
        self.players_drowned_icons = [self.fly_d_icon]

    def draw_characters(self, number, characters):
        message = True
        for i in range(number):
            x = characters[PLAYERS[i]]['position'][0]
            y = characters[PLAYERS[i]]['position'][1]

            if characters[PLAYERS[i]]['if_out']:
                character_rect = self.players_drowned_icons[i].get_rect(center=self.get_position(x, y))
                self.screen.blit(self.players_drowned_icons[i], character_rect)
                if characters[PLAYERS[i]]['steps_out'] == 0:
                    green_tick_rect = self.green_tick_icon.get_rect(topleft=self.get_position(x, y))
                    self.screen.blit(self.green_tick_icon, green_tick_rect)
                else:
                    steps_text_surface = self.pixel_font.render(str(characters[PLAYERS[i]]['steps_out']), False, "Red")
                    steps_text_rect = steps_text_surface.get_rect(topleft=self.get_position(x, y))
                    self.screen.blit(steps_text_surface, steps_text_rect)
                    message = False
            else:
                character_rect = self.players_icons[i].get_rect(center = self.get_position(x, y))
                self.screen.blit(self.players_icons[i], character_rect)
                message = False
        return message

    def get_position(self, x, y):
        if x == 0:
            position_x = PLANKS_X - CELLS_GAP_X - CELL_SIZE / 2
        else:
            x -= 1
            initial_x = PLANKS_X + CELLS_X + CELLS_GAP_X + CELL_SIZE / 2
            position_x = initial_x + (CELL_SIZE + CELLS_GAP_X * 2) * x

        if y == 0:
            position_y = PLANKS_Y - CELL_SIZE / 2
        else:
            y -= 1
            initial_y = PLANKS_Y + CELLS_Y + CELL_SIZE / 2
            position_y = initial_y + (CELL_SIZE + CELLS_GAP_Y * 2) * y
        return position_x, position_y
