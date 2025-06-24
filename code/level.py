from settings import *
from sprites import Sprite
from msprites import MovingSprite
from player import Player
from groups import AllSprites
from asprite import AnimatedSprite

class Level:
    def __init__(self, tmx_map, level_frames):
        self.__display_surface = pygame.display.get_surface()

        #groups
        self.__all_sprites = AllSprites()
        self.__collision_sprites = pygame.sprite.Group()
        self.__semi_collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        #tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.__all_sprites]
                if layer == 'Terrain': groups.append(self.__collision_sprites)
                if layer == 'Platforms': groups.append(self.__semi_collision_sprites)
                match layer:
                    case 'BG': z = get_z_layers('bg tiles')
                    case 'FG': z = get_z_layers('fg')
                    case _: z = get_z_layers('main')
                Sprite((x * get_tile_size(),y * get_tile_size()), surf, groups, z)

        #objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.__player = Player((obj.x, obj.y), self.__all_sprites, self.__collision_sprites, self.__semi_collision_sprites)
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image, (self.__all_sprites, self.__collision_sprites))
                else:
                    if 'palm' not in obj.name:
                        frames = level_frames[obj.name]
                        AnimatedSprite((obj.x, obj.y), frames, self.__all_sprites)


        #moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
           if obj.name == 'helicopter':
               
               if obj.width > obj.height: #horizontal moviment
                   move_dir = 'x'
                   start_pos = ( obj.x, obj.y + obj.height / 2 )
                   end_pos =  ( obj.x + obj.width, obj.y + obj.height / 2 )
               else:
                move_dir = 'y'
                start_pos = ( obj.x + obj.width / 2, obj.y)
                end_pos =  ( obj.x + obj.width / 2, obj.y + obj.height )

               speed = obj.properties['speed']
               MovingSprite((self.__all_sprites, self.__semi_collision_sprites), start_pos, end_pos, move_dir, speed)
               
    def run(self, dt):
        self.__all_sprites.update(dt)
        self.__display_surface.fill('black')
        self.__all_sprites.draw(self.__player.hitbox_rect.center)