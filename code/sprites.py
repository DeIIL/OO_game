from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, surface = pygame.Surface((get_tile_size(), get_tile_size())), groups = None, z = get_z_layers('main')):
        super().__init__(groups)
        self.__image = surface
        ##self.__image.fill('white')
        self.__rect = self.__image.get_frect(topleft = position)
        self.__old_rect = self.__rect.copy()
        self.__z = z

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
    def old_rect(self):
        return self.__old_rect
    
    @old_rect.setter
    def old_rect(self, value):
        self.__old_rect = value

    @property
    def z(self):
        return self.__z
    
    @z.setter
    def z(self, value):
        self.__z = value