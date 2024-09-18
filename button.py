import pygame
from constants import (LOBBY_BUTTON_WIDTH, LOBBY_BUTTON_HEIGHT, BUTTON_SCALE)

class Button:
    def __init__(self, image, hovered_image, pressed_image, pos):
        self.pos = pos

        self.image = pygame.image.load(image).convert_alpha()
        self.hovered_image = pygame.image.load(hovered_image).convert_alpha()
        self.pressed_image = pygame.image.load(pressed_image).convert_alpha()

        self.is_pressed = 0

    def draw(self, screen):
        if self.is_hovered():
            if self.is_pressed:
                image = self.pressed_image
            else:
                image = self.hovered_image
        else:
            image = self.image
        image = pygame.transform.scale_by(image, BUTTON_SCALE)
        button_rect = image.get_rect(center=self.pos)
        screen.blit(image, button_rect)

    def is_hovered(self):
        xm, ym = pygame.mouse.get_pos()
        x, y = self.pos
        if (x + LOBBY_BUTTON_WIDTH / 2 >= xm >= x - LOBBY_BUTTON_WIDTH / 2 and
                y + LOBBY_BUTTON_HEIGHT / 2 >= ym >= y - LOBBY_BUTTON_HEIGHT / 2):
            return True
        return False

    def press(self):
        self.is_pressed = 1

    def release(self):
        self.is_pressed = 0
        #action