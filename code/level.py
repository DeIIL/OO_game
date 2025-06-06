from settings import *
from sprites import Sprite
from player import Player

class Level:
    def __init__(self, tmx_map):
        self.__display_surface = pygame.display.get_surface()

        #groups
        self.__all_sprites = pygame.sprite.Group()
        self.__collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x,y,surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * get_tile_size(),y * get_tile_size()), surf, (self.__all_sprites, self.__collision_sprites))

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                Player((obj.x, obj.y), self.__all_sprites, self.__collision_sprites)


    def run(self, dt):
        self.__all_sprites.update(dt)
        self.__display_surface.fill('black')
        self.__all_sprites.draw(self.__display_surface)