import pygame
from settings import *
from menu import Menu
from pygame import mixer

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.NewGameX, self.NewGameY = self.mid_w, self.mid_h 
        self.continueX, self.continueY = self.mid_w, self.mid_h + 70
        self.optionsX, self.optionsY = self.mid_w, self.mid_h + 140
        self.cursor_rect.midtop = (self.NewGameX + self.offset, self.NewGameY)
        self.backgroud = pygame.image.load('OO_game/Backgroud.jpg')
        mixer.music.load('OO_game/bgmusic.mp3')
        mixer.music.play(-1)
        

    def display_menu(self): 
     self.run_display = True
     while self.run_display:
        self.game.check_events()
        self.check_input()
        self.game.display.blit(self.backgroud, (0,0))
        self.game.draw_text("Main menu", 350, self.game.window_width/2 , self.game.window_height/2 - 200)
        self.game.draw_text("New Game", 150, self.NewGameX, self.NewGameY)
        self.game.draw_text("Continue", 150, self.continueX, self.continueY)
        self.game.draw_text("Options", 150, self.optionsX, self.optionsY)
        self.draw_cursor()
        self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.continueX + self.offset, self.continueY)
                self.state = 'Continue'
            elif self.state == 'Continue':
                self.cursor_rect.midtop = (self.optionsX + self.offset, self.optionsY)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.NewGameX + self.offset, self.NewGameY)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsX + self.offset, self.optionsY)
                self.state = 'Options'
            elif self.state == 'Continue':
                self.cursor_rect.midtop = (self.NewGameX + self.offset, self.NewGameY)
                self.state = 'Start'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.continueX + self.offset, self.continueY)
                self.state = 'Continue'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.current_menu = self.game.run()
            elif self.state == 'Continue':
                self.game.current_menu = self.game.continueM
            elif self.state == 'Options':
                self.game.current_menu = self.game.options
            self.run_display = False