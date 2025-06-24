from settings import *
from sprites import Sprite
from msprites import MovingSprite
from player import Player

class Level:
    def __init__(self, tmx_map):
        self.__display_surface = pygame.display.get_surface()

        #groups
        self.__all_sprites = pygame.sprite.Group()
        self.__collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        #tiles
        for x,y,surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * get_tile_size(),y * get_tile_size()), surf, (self.__all_sprites, self.__collision_sprites))

        #objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                Player((obj.x, obj.y), self.__all_sprites, self.__collision_sprites)

        #moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
           if obj.name == 'helicopter':
               
               if obj.width > obj.height: #horizontal moviment
                   move_dir = 'x'
                   print(obj.x)
                   start_pos = ( obj.x, obj.y + obj.height / 2 )
                   end_pos =  ( obj.x + obj.width, obj.y + obj.height / 2 )
               else:
                move_dir = 'y'
                start_pos = ( obj.x + obj.width / 2, obj.y)
                end_pos =  ( obj.x + obj.width / 2, obj.y + obj.height )

               print(start_pos)
               speed = obj.properties['speed']
               MovingSprite((self.__all_sprites, self.__collision_sprites), start_pos, end_pos, move_dir, speed)
               
    def run(self, dt):
        self.__all_sprites.update(dt)
        self.__display_surface.fill('black')
        self.__all_sprites.draw(self.__display_surface)