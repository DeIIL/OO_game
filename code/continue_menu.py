import pygame
from settings import *
from menu import Menu

class ContinueMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'sim'
        self.simX, self.simY = self.mid_w, self.mid_h
        self.naoX, self.naoY = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.simX + self.offset, self.simY)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Continuar jogo salvo?', 220, self.game.window_width/2 , self.game.window_height/2 - 200)
            self.game.draw_text("Sim", 150, self.simX, self.simY)
            self.game.draw_text("Nao", 150, self.naoX, self.naoY)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.current_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'sim':
                self.state = 'nao'
                self.cursor_rect.midtop = (self.naoX + self.offset, self.naoY)
            elif self.state == 'nao':
                self.state = 'sim'
                self.cursor_rect.midtop = (self.simX + self.offset, self.simY)
        elif self.game.START_KEY:
            if self.state == 'sim':
                self.game.current_menu = self.game.run()
            elif self.state == 'nao':
                self.game.current_menu = self.game.main_menu
            self.run_display = False
