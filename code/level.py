from settings import *
from sprites import Sprite
from msprites import MovingSprite
from player import Player
from groups import AllSprites
from asprite import AnimatedSprite
from spike import Spike
from random import uniform
from tooth import Tooth
from shell import Shell
from bullet import Bullet

class Level:
    def __init__(self, tmx_map, level_frames):
        self.__display_surface = pygame.display.get_surface()

        #groups
        self.__all_sprites = AllSprites()
        self.__collision_sprites = pygame.sprite.Group()
        self.__semi_collision_sprites = pygame.sprite.Group()
        self.__damage_sprites = pygame.sprite.Group()
        self.__tooth_sprites = pygame.sprite.Group()
        self.__bullet_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)
        self.__pearl_surf = level_frames['pearl']

    def setup(self, tmx_map, level_frames):
        #tiles
        for layer in [ 'BG', 'Terrain', 'FG', 'Platforms' ]:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.__all_sprites]
                if layer == 'Terrain': groups.append(self.__collision_sprites)
                if layer == 'Platforms': groups.append(self.__semi_collision_sprites)
                match layer:
                    case 'BG': z = get_z_layers( 'bg tiles' )
                    case 'FG': z = get_z_layers( 'bg tiles' )
                    case _: z = get_z_layers( 'main' )
                Sprite((x * get_tile_size(),y * get_tile_size()), surf, groups, z)
        #bg details
        for obj in tmx_map.get_layer_by_name( 'BG details' ):
            if obj.name == 'static':
                Sprite( ( obj.x, obj.y ), obj.image, self.__all_sprites, z = get_z_layers( 'bg tiles' ) )
            else:
                AnimatedSprite( ( obj.x, obj.y ), level_frames[obj.name], self.__all_sprites, z = get_z_layers( 'bg tiles' ) )
                if obj.name == 'candle':
                    AnimatedSprite( (obj.x, obj.y) + vector( -20, -20 ), level_frames['candle_light'], self.__all_sprites, z = get_z_layers( 'bg tiles' ) )

        #objects
        for obj in tmx_map.get_layer_by_name( 'Objects' ):
            if obj.name == 'player':
                self.__player = Player(
                    position = (obj.x, obj.y), 
                    groups = self.__all_sprites, 
                    collision_sprites = self.__collision_sprites, 
                    semi_collision_sprites = self.__semi_collision_sprites,
                    frame = level_frames['player']
                    )
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite( ( obj.x, obj.y ), obj.image, ( self.__all_sprites, self.__collision_sprites ) )
                else:
                    #frames
                    frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
                    if obj.name == 'floor_spike' and obj.properties['inverted']:
                        frames = [pygame.transform.flip(frame, False, True) for frame in frames]
                    #groups
                    groups = [self.__all_sprites]
                    if obj.name in ( 'palm_small', 'palm_large' ): groups.append(self.__semi_collision_sprites)
                    if obj.name in ( 'saw', 'floor_spike'): groups.append(self.__damage_sprites)
                    #z index
                    z = get_z_layers('main') if not 'bg' in obj.name else get_z_layers('bg details')
                    #animation speed
                    animation_speed = get_animation_speed() if not 'palm' in obj.name else get_animation_speed() + uniform( -1, 1 )
                    AnimatedSprite( ( obj.x, obj.y ), frames, groups, z, animation_speed )

        #moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
           if obj.name == 'spike':
               Spike(
                   pos = ( obj.x + obj.width / 2, obj.y + obj.height / 2 ),
                   surf = level_frames['spike'],
                   groups = (self.__all_sprites, self.__damage_sprites),
                   radius = obj.properties['radius'],
                   speed = obj.properties['speed'],
                   start_angle = obj.properties['start_angle'],
                   end_angle = obj.properties['end_angle'])
               
               
               for i in range( 0, obj.properties['radius'], 20 ):
                Spike(
                   pos = ( obj.x + obj.width / 2, obj.y + obj.height/ 2 ),
                   surf = level_frames['spike_chain'],
                   groups = self.__all_sprites,
                   radius = i,
                   speed = obj.properties['speed'],
                   start_angle = obj.properties['start_angle'],
                   end_angle = obj.properties['end_angle'],
                   z = get_z_layers('bg details'))

           else:
               frames = level_frames[obj.name]
               groups = ( self.__all_sprites, self.__semi_collision_sprites ) if obj.properties['platform'] else ( self.__all_sprites, self.__damage_sprites )
               if obj.width > obj.height: #horizontal moviment
                   move_dir = 'x'
                   start_pos = ( obj.x, obj.y + obj.height / 2 )
                   end_pos =  ( obj.x + obj.width, obj.y + obj.height / 2 )
               else:
                move_dir = 'y'
                start_pos = ( obj.x + obj.width / 2, obj.y)
                end_pos =  ( obj.x + obj.width / 2, obj.y + obj.height )

               speed = obj.properties['speed']
               MovingSprite( frames, groups , start_pos, end_pos, move_dir, speed, obj.properties['flip'] )

               if obj.name == 'saw':
                   if move_dir == 'x':
                       y = start_pos[1] - level_frames['saw_chain'].get_height() / 2
                       left, right = int( start_pos[0] ), int( end_pos[0] )
                       for x in range(left, right, 20):
                           Sprite( ( x , y ), level_frames['saw_chain'], self.__all_sprites, get_z_layers('bg details') )
                   else: 
                       x = start_pos[0] - level_frames['saw_chain'].get_width() / 2
                       top, bottom = int( start_pos[1] ), int( end_pos[1] )
                       for y in range(top, bottom, 20):
                           Sprite( ( x , y ), level_frames['saw_chain'], self.__all_sprites, get_z_layers('bg details') )

        #enemies
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth( ( obj.x, obj.y ), level_frames['tooth'], ( self.__all_sprites, self.__damage_sprites, self.__tooth_sprites ), self.__collision_sprites )
            if obj.name == 'shell':
                Shell( 
                    pos = ( obj.x, obj.y ),
                    frame = level_frames['shell'],
                    groups = ( self.__all_sprites, self.__collision_sprites ),
                    reverse = obj.properties['reverse'],
                    player = self.__player, 
                    create_pearl = self.create_bullet )

    def create_bullet(self, pos, direction):
        Bullet(pos, 
               groups = ( self.__all_sprites, self.__damage_sprites, self.__bullet_sprites ), 
               surf = self.__pearl_surf, 
               direction = direction, 
               speed = 150)

    def bullet_collision(self):
        for sprite in self.__collision_sprites:
            pygame.sprite.spritecollide(sprite, self.__bullet_sprites, True)

    def hit_collision(self):
        for sprite in self.__damage_sprites:
            if sprite.rect.colliderect(self.__player.hitbox_rect):
                if hasattr(sprite, 'bullet'):
                    sprite.kill()

    def run(self, dt):
        self.__display_surface.fill('black')
        
        self.__all_sprites.update(dt)
        self.bullet_collision()
        self.hit_collision()
        
        self.__all_sprites.draw(self.__player.hitbox_rect.center)