from settings import *
from sprites import Sprite

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, level, data):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (pos[0] + get_tile_size() / 2 , pos[1] + get_tile_size() / 2))
        self.z = get_z_layers('path')
        self.level = level
        self.data = data
