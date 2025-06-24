from settings import *
from sprites import *

class MovingSprite(Sprite):
    def __init__(self, groups, start_pos, end_pos, move_dir, speed):
        surface = pygame.Surface((200,50))
        super().__init__(start_pos, surface, groups)
        if move_dir == 'x':
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos

        self.__start_pos = start_pos
        self.__end_pos = end_pos

        #moviment
        self.__moving = True
        self.__speed = speed
        self.direction = vector(1,0) if move_dir == 'x' else vector(0,1)
        self.__move_dir = move_dir

        @property
        def start_pos(self):
            return self.__start_pos
        
        @start_pos.setter
        def start_pos(self, value):
            self.__start_pos = value

        @property
        def end_pos(self):
            return self.__end_pos
        
        @end_pos.setter
        def end_pos(self, value):
            self.__end_pos = value

        @property
        def speed(self):
            return self.__speed
        
        @speed.setter
        def speed(self, value):
            self.__speed = value

        @property
        def move_dir(self):
            return self.__move_dir
        
        @move_dir.setter
        def move_dir(self, value):
            self.__move_dir = value

        @property
        def moving(self):
            return self.__moving
        
        @moving.setter
        def moving(self, value):
            self.__moving = value
        


    def check_border(self):
        if self.__move_dir == 'x':
            if self.rect.right >= self.__end_pos[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.__end_pos[0]
            if self.rect.left <= self.__start_pos[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.__start_pos[0]
        else:
            if self.rect.bottom >= self.__end_pos[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.__end_pos[1]
            if self.rect.top <= self.__start_pos[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.__start_pos[1]

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.__speed * dt
        self.check_border()
