from settings import *
from random import choice
from timer import Timer

class Tooth(pygame.sprite.Sprite):
    def __init__(self, pos, frame, groups, collision_sprites):
        super().__init__(groups)
        self.__z = get_z_layers('main')
        self.__frames = frame
        self.__frame_index = 0
        self.__image = self.__frames[self.__frame_index]
        self.__rect = self.__image.get_frect(topleft = pos)

        self.__direction = choice( ( -1, 1 ) )
        self.__collision_rects = [sprite.rect for sprite in collision_sprites]
        self.__speed = 200

        self.hit_timer = Timer(250)

    def reverse(self):
        if not self.hit_timer.active:
            self.__direction *= -1
            self.hit_timer.activate()

    def update(self, dt):
        self.hit_timer.update()

        #animation
        self.__frame_index += get_animation_speed() * dt
        self.__image = self.__frames[ int( self.__frame_index % len( self.__frames ) ) ]
        #straight direction
        self.__image = pygame.transform.flip(self.__image, True, False) if self.__direction < 0 else self.__image
        #move
        self.__rect.x += self.__direction * self.__speed * dt
        #reverse the direction
        floor_rect_right = pygame.FRect( self.rect.bottomright, ( 1,1 ) )
        floor_rect_left = pygame.FRect( self.rect.bottomleft, ( -1,1 ) )
        wall_rect = pygame.FRect( self.rect.topleft + vector( -1,0 ), ( self.rect.width + 2, 1 ) )

        if floor_rect_right.collidelist(self.__collision_rects) < 0 and self.__direction > 0 or\
           floor_rect_left.collidelist(self.__collision_rects) < 0 and self.__direction < 0 or\
           wall_rect.collidelist(self.__collision_rects) != -1:
            self.__direction *= -1

    @property
    def image(self):
        return self.__image
    
    @property
    def rect(self):
        return self.__rect
    
    @property
    def z(self):
        return self.__z
    
    @image.setter
    def image(self, value):
        self.__image = value
    
    @rect.setter
    def rect(self, value):
        self.__rect = value

    @z.setter
    def z(self, value):
        self.__z = value