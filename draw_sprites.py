import pygame
from constants import (WIDTH, HEIGHT, FIELD_WIDTH, FIELD_HEIGHT, PLANKS_X, PLANKS_Y, PLANK_WIDTH, PLANK_HEIGHT,
    CELLS_X, CELLS_Y, CELLS_GAP_X, CELLS_GAP_Y, CELL_SIZE, CELLS, PLAYERS)

class DrawScreen:
    def __init__(self, screen):
        self.screen = screen

        self.bush_right_img = pygame.image.load("./img/Bush_right2.png").convert_alpha()
        self.bush_right_rect = self.bush_right_img.get_rect(topright = (1100, 0))

        self.bush_left_img = pygame.image.load("./img/Bush_left_shadowed.png").convert_alpha()
        self.bush_left_rect = self.bush_left_img.get_rect(topleft=(-100, 0))

        self.water_img = pygame.image.load("./img/Water.png").convert_alpha()  # background image
        self.water_img = pygame.transform.scale(self.water_img, (WIDTH * 2, HEIGHT * 2))

        self.planks_img = pygame.image.load("./img/Planks.png").convert_alpha()  # planks image
        self.planks_img = pygame.transform.scale(self.planks_img, (FIELD_WIDTH, FIELD_HEIGHT))

        self.cell_img = pygame.image.load("./img/cell2.png").convert_alpha()
        self.cell_img = pygame.transform.scale(self.cell_img, (CELL_SIZE, CELL_SIZE))

        self.fly_icon = pygame.image.load("./img/Fly.png").convert_alpha()
        self.fly_icon = pygame.transform.scale(self.fly_icon, (CELL_SIZE, CELL_SIZE))

        # self.frog_icon = pygame.image.load("./img/cell2.png").convert_alpha()
        # self.frog_icon = pygame.transform.scale(self.frog_icon, (CELL_SIZE, CELL_SIZE))

        # self.fly_icon = pygame.image.load("./img/cell2.png").convert_alpha()
        # self.fly_icon = pygame.transform.scale(self.fly_icon, (CELL_SIZE, CELL_SIZE))

        self.players_icons = [self.fly_icon]
        self.character_rects = []

    def draw_leaves(self):
        self.screen.blit(self.bush_right_img, self.bush_right_rect)
        self.screen.blit(self.bush_left_img, self.bush_left_rect)

    def draw_water(self):
        self.screen.blit(self.water_img, (0, 0))

    def draw_planks(self):
        self.screen.blit(self.planks_img, (PLANKS_X, PLANKS_Y))

    def draw_cells(self):
        initial_x = PLANKS_X + CELLS_X + CELLS_GAP_X + CELL_SIZE / 2
        initial_y = PLANKS_Y + CELLS_Y + CELL_SIZE / 2
        for i in range(CELLS):
            for j in range(CELLS):
                cell_rect = self.cell_img.get_rect(center=(initial_x + (CELL_SIZE + CELLS_GAP_X * 2) * j,
                                                           initial_y + (CELL_SIZE + CELLS_GAP_Y * 2) * i))
                self.screen.blit(self.cell_img, cell_rect)

    def draw_characters(self, number, characters):
        for i in range(number):
            x = characters[PLAYERS[i]]['position'][0]
            y = characters[PLAYERS[i]]['position'][1]

            position_x, position_y = self.get_position(x, y)

            self.character_rects.append(self.players_icons[i].get_rect(center=(position_x, position_y)))
            self.screen.blit(self.players_icons[i], self.character_rects[i])

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

    def move_character(self, number, characters):
        for i in range(number):
            x = characters[PLAYERS[i]]['position'][0]
            y = characters[PLAYERS[i]]['position'][1]

            position_x, position_y = self.get_position(x, y)

            self.character_rects[i].center = (position_x, position_y)
            self.screen.blit(self.players_icons[i], self.character_rects[i])