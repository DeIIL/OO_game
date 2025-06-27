import pygame
from settings import *
from menu import Menu

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'VolumeM'
        self.volmx, self.volmy = self.mid_w, self.mid_h 
        self.volcX, self.volcY = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.volmx + self.offset, self.volmy)
        self.music_volume = 0.1
        self.cenary_volume = 0.1

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 220, self.game.window_width / 2, self.game.window_height/ 2 - 200)
            self.game.draw_text("Music Volume {:.1f}".format(self.music_volume), 150, self.volmx, self.volmy)
            self.game.draw_text("Cenary Volume {:.1f}".format(self.cenary_volume), 150, self.volcX, self.volcY)
            self.draw_cursor()
            self.blit_screen()

    def draw_cursor(self):
        self.game.draw_text('>', 150, self.cursor_rect.x - 100, self.cursor_rect.y)
        self.game.draw_text('<', 150, self.cursor_rect.x + 600, self.cursor_rect.y)

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.current_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'VolumeM':
                self.state = 'VolumeC'
                self.cursor_rect.midtop = (self.volcX + self.offset, self.volcY)
            elif self.state == 'VolumeC':
                self.state = 'VolumeM'
                self.cursor_rect.midtop = (self.volmx + self.offset, self.volmy)
        elif self.game.START_KEY:
            if self.state == 'VolumeM':
                if self.music_volume >= 0.9:
                    self.music_volume = -0.1
                self.music_volume = self.music_volume + 0.1
                pygame.mixer.music.set_volume(self.music_volume)
            elif self.state == 'VolumeC':
                if self.cenary_volume >= 0.9:
                    self.cenary_volume = -0.1
                self.cenary_volume = self.cenary_volume + 0.1
            pass