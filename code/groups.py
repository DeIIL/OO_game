from settings import *
from sprites import Sprite
from cloud import Cloud
from random import choice, randint
from timer import Timer

class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, clouds, horizon_line, bg_tile = None, top_limit = 0):
        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__offset = vector()
        self.width, self.height =  width * get_tile_size(), height * get_tile_size()
        self.borders = {
			'left': 0,
			'right': -self.width + get_window_width(),
			'bottom': -self.height + get_window_height(),
			'top': top_limit}
        self.sky = not bg_tile
        self.horizon_line = horizon_line

        if bg_tile:
            for col in range(width):
                for row in range(-int(top_limit / get_tile_size()) - 1, height):
                    x, y = col * get_tile_size(), row * get_tile_size()
                    Sprite((x,y), bg_tile, self, -1)
        else:
            self.large_cloud = clouds['large']
            self.small_clouds = clouds['small']
            self.cloud_direction = -1

            self.large_cloud_speed = 100
            self.large_cloud_x = 0
            self.large_cloud_tiles = int(self.width / self.large_cloud.get_width()) + 2
            self.large_cloud_width, self.large_cloud_height = self.large_cloud.get_size()

            self.cloud_timer = Timer(2500, self.create_cloud, True)
            self.cloud_timer.activate()
            for cloud in range(20):
                pos = (randint(0,self.width), randint(self.borders['top'], self.horizon_line))
                surf = choice(self.small_clouds)
                Cloud(pos, surf, self)


    def camera_contraint(self):
        self.__offset.x = self.__offset.x if self.__offset.x < self.borders['left'] else self.borders['left']
        self.__offset.x = self.__offset.x if self.__offset.x > self.borders['right'] else self.borders['right'] 
        self.__offset.y = self.__offset.y if self.__offset.y > self.borders['bottom'] else self.borders['bottom']
        self.__offset.y = self.__offset.y if self.__offset.y < self.borders['top'] else self.borders['top']

    def draw_sky(self):
        self.__display_surface.fill('#ddc6a1')
        horizon_pos = self.horizon_line + self.__offset.y

        sea_rect = pygame.FRect(0,horizon_pos, get_window_width(), get_window_height() - horizon_pos)
        pygame.draw.rect(self.__display_surface, '#92a9ce' , sea_rect)

        pygame.draw.line(self.__display_surface, '#f5f1d3' , (0 , horizon_pos) , (get_window_width(), horizon_pos) , 4)

    def draw_large_cloud(self, dt):
            self.large_cloud_x += self.cloud_direction * self.large_cloud_speed * dt
            if self.large_cloud_x <= -self.large_cloud_width:
                self.large_cloud_x = 0
            for cloud in range(self.large_cloud_tiles):
                left = self.large_cloud_x + self.large_cloud_width * cloud + self.__offset.x
                top = self.horizon_line - self.large_cloud_height + self.__offset.y
                self.__display_surface.blit(self.large_cloud, (left,top))
    
    def create_cloud(self):
        pos = (randint(self.width + 500, self.width + 600), randint(self.borders['top'], self.horizon_line))
        surf = choice(self.small_clouds)
        Cloud(pos, surf, self)

    def draw(self, target_pos, dt):
        window_width, window_height = get_window_dimensions()
        self.__offset.x = -( target_pos[0] - window_width / 2 )#target_pos[0] only the x part or 0 index
        self.__offset.y = -( target_pos[1] - window_height / 2)#target_pos[1] only the y part or 1 index
        self.camera_contraint()

        if self.sky:
            self.cloud_timer.update()
            self.draw_sky()
            self.draw_large_cloud(dt)


        for sprite in sorted(self, key = lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.__offset
            self.__display_surface.blit(sprite.image, offset_pos)