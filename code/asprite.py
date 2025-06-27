from sprites import *
from settings import *

class AnimatedSprite(Sprite):
    def __init__(self, position, frames, groups, z = get_z_layers('main'), animation_speed = get_animation_speed()):
        self.__frames, self.__frame_index = frames, 0
        super().__init__(position, self.__frames[self.__frame_index], groups, z)
        self.__animation_speed = animation_speed

    @property
    def frames(self):
        return self.__frames

    @frames.setter
    def frames(self, value):
        self.__frames = value

    # Getter e Setter para frame_index
    @property
    def frame_index(self):
        return self.__frame_index

    @frame_index.setter
    def frame_index(self, value):
        self.__frame_index = value

    # Getter e Setter para animation_speed
    @property
    def animation_speed(self):
        return self.__animation_speed

    @animation_speed.setter
    def animation_speed(self, value):
        self.__animation_speed = value

    def animate(self, dt):
        self.__frame_index += self.__animation_speed * dt
        self.image = self.__frames[int(self.__frame_index % len(self.__frames))]

    def update(self, dt):
        self.animate(dt)