import pygame
from constants import (WIDTH, HEIGHT, FIELD_WIDTH, FIELD_HEIGHT, PLANKS_X, PLANKS_Y, PLANK_WIDTH, PLANK_HEIGHT,
    CELLS_X, CELLS_Y, CELLS_GAP_X, CELLS_GAP_Y, CELL_SIZE, CELLS)

class DrawScreen:
    def __init__(self, screen):
        self.screen = screen

        self.water_img = pygame.image.load("./img/Water.png").convert_alpha()  # background image
        self.water_img = pygame.transform.scale(self.water_img, (WIDTH * 2, HEIGHT * 2))

        self.planks_img = pygame.image.load("./img/Planks.png").convert_alpha()  # planks image
        self.planks_img = pygame.transform.scale(self.planks_img, (FIELD_WIDTH, FIELD_HEIGHT))

        self.cell_img = pygame.image.load("./img/cell2.png").convert_alpha()
        self.cell_img = pygame.transform.scale(self.cell_img, (CELL_SIZE, CELL_SIZE))


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
