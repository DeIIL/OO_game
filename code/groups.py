from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__offset = vector()

    def draw(self, target_pos):
        window_width, window_height = get_window_dimensions()
        self.__offset.x = -( target_pos[0] - window_width / 2 )#target_pos[0] only the x part or 0 index
        self.__offset.y = -( target_pos[1] - window_height / 2)#target_pos[1] only the y part or 1 index
        for sprite in sorted(self, key = lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.__offset
            self.__display_surface.blit(sprite.image, offset_pos)