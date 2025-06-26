from settings import *
from random import choice
from timer import Timer

class Shell(pygame.sprite.Sprite):
    def __init__(self, pos, frame, groups, reverse, player, create_pearl):
        super().__init__(groups)

        if reverse:
            self.__frames = {}
            for key, surfs in frame.items():
                self.__frames[ key ] = [ pygame.transform.flip( surf, True, False ) for surf in surfs ]
            self.__bullet_direction = -1
        else:
            self.__frames = frame
            self.__bullet_direction = 1

        self.__frame_index = 0
        self.__state = 'idle'
        self.image = self.__frames[self.__state][self.__frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = get_z_layers('main')
        self.player = player
        self.shoot_timer = Timer(2000)
        self.__has_fired = False
        self.__create_pearl = create_pearl
    
    def state_management(self):
        player_pos, shell_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = shell_pos.distance_to(player_pos) < 500
        player_front = shell_pos.x < player_pos.x if self.__bullet_direction > 0 else shell_pos.x > player_pos.x
        player_level = abs( shell_pos.y - player_pos.y ) < 60
        
        if player_near and player_front and player_level and not self.shoot_timer.active:
            self.__state = 'fire'
            self.__frame_index = 0
            self.shoot_timer.activate()

        @property
        def image(self):
            return self.__image
        
        @image.setter
        def image(self, value):
            self.__image = value
        @property
        def rect(self):
            return self.__rect
        
        @rect.setter
        def rect(self, value):
            self.__rect = value
        @property
        def z(self):
            return self.__z
        
        @z.setter
        def z(self, value):
            self.__z = value

    def update(self, dt):
        self.shoot_timer.update()
        self.state_management()
        #animation / attacking
        self.__frame_index += get_animation_speed() * dt
        if self.__frame_index < len( self.__frames[self.__state] ):
            self.image = self.__frames[self.__state][int(self.__frame_index)]
        #shooting animation
            if self.__state == 'fire' and int( self.__frame_index ) == 3 and not self.__has_fired:
                self.__create_pearl( self.rect.center, self.__bullet_direction )
                self.__has_fired = True
        else:
            self.__frame_index = 0
            if self.__state == 'fire':
                self.__state = 'idle'
                self.__has_fired = False
