from settings import *
from sprites import Sprite
from asprite import AnimatedSprite
from world_sprites import WorldSprites
from random import randint
from node import Node
from icon import Icon

class Overworld:
    def __init__(self, tmx_map, data, overworld_frames):
        self.display_surface = pygame.display.get_surface()
        self.data = data

        #groups
        self.all_sprites = WorldSprites(data)

        self.setup(tmx_map, overworld_frames)

    def setup(self,tmx_map,overworld_frames):
        #tiles
        for layer in ['main' , 'top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * get_tile_size() ,y * get_tile_size()), surf, self.all_sprites, get_z_layers('bg tiles'))

        #water
        for col in range(tmx_map.width):
            for row in range(tmx_map.height):
                AnimatedSprite((col * get_tile_size() ,row * get_tile_size()), overworld_frames['water'], self.all_sprites,get_z_layers('bg'))

        #objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'palm':
                AnimatedSprite((obj.x, obj.y), overworld_frames['palms'], self.all_sprites, get_z_layers('main'), randint(4,6))
            else: 
                z = get_z_layers('bg details')
                Sprite((obj.x , obj.y), obj.image, self.all_sprites, z)

        #nodes and player
        for obj in tmx_map.get_layer_by_name('Nodes'):

            #player
            if obj.name == 'Node' and obj.properties['stage'] == self.data.current_level:
                self.icon = Icon((obj.x + get_tile_size() / 2 , obj.y + get_tile_size() / 2 ), self.all_sprites, overworld_frames['icon'] )
            #nodes
            if obj.name == 'Node':
                Node(pos = (obj.x, obj.y) , 
                     surf = overworld_frames['path']['node'], 
                     groups = self.all_sprites,
                     level = obj.properties['stage'],
                     data = self.data)

    def run(self,dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.icon.rect.center)