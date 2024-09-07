import pygame
from sys import exit
from constants import FPS, WIDTH, HEIGHT
from draw_sprites import DrawScreen

class PygameLogic:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('MindBlow')
        self.clock = pygame.time.Clock()

        self.draw = DrawScreen(self.screen)

        self.update()

    def update(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.draw.draw_water()
            self.draw.draw_planks()
            self.draw.draw_cells()

            pygame.display.update()
            self.clock.tick(FPS)

p = PygameLogic()