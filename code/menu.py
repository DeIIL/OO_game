import pygame
from settings import *

class Menu():
    def __init__(self,game):
        self.__game = game
        window_width, window_height = get_window_dimensions()
        self.__mid_w = window_width/2
        self.__mid_h = window_height/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,300,300)
        self.offset = - 100

    @property
    def game(self):
        return self.__game

    @game.setter
    def game(self, value):
        self.__game = value

    # Getter e Setter para __mid_w
    @property
    def mid_w(self):
        return self.__mid_w

    @mid_w.setter
    def mid_w(self, value):
        self.__mid_w = value

    # Getter e Setter para __mid_h
    @property
    def mid_h(self):
        return self.__mid_h

    @mid_h.setter
    def mid_h(self, value):
        self.__mid_h = value

    def draw_cursor(self):
        self.game.draw_text('>', 150, self.cursor_rect.x, self.cursor_rect.y)
        self.game.draw_text('<', 150, self.cursor_rect.x + 500, self.cursor_rect.y)

    def blit_screen(self):
            self.game.display_surface.blit(self.game.display, (0,0))
            pygame.display.update()
            self.game.reset_keys()

   