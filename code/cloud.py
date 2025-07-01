from sprites import Sprite
from settings import *
from random import randint

class Cloud(Sprite):
    def __init__(self, pos, surf, groups, z = get_z_layers('clouds')):
        super().__init__(pos, surf, groups, z)
        self.speed = randint(50,120)
        self.direction = -1
        self.rect.midbottom = pos

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

        if self.rect.right <= 0:
            self.kill()