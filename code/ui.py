from settings import *
from heart import Heart
from timer import Timer
import os
from os.path import join
import pygame 

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font

        #hearts 
        self.heart_frames = frames['heart']
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 7

        #coins
        self.coin_aumount = 0
        self.coin_timer = Timer(1000)
        self.coin_surf = frames['coin']

    def create_hearts(self, aumont):
        for sprite in self.sprites:
            sprite.kill()
        for heart in range(aumont):
            x = 10 + heart * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x,y), self.heart_frames, self.sprites)

    def display_text(self):
        if self.coin_timer.active:
            script_dir = os.path.dirname(__file__)  
            self.font = pygame.font.Font(os.path.join(script_dir, '..', 'graphics', 'Litebulb 8-bit.ttf'), 40)
            text_surf = self.font.render(str(self.coin_aumount), False, 'white')
            text_rect = text_surf.get_frect(topleft = (16,34))
            self.display_surface.blit(text_surf, text_rect)

            coin_rect = self.coin_surf.get_frect(center = text_rect.bottomleft).move(0, -6)
            self.display_surface.blit(self.coin_surf, coin_rect)

    def show_coins(self,amount):
        self.coin_aumount = amount
        self.coin_timer.activate()

    def update(self, dt):
        self.sprites.update(dt)
        self.coin_timer.update()
        self.sprites.draw(self.display_surface)
        self.display_text()
