from settings import *
from sprites import Sprite
from math import sin, cos, radians

class Spike(Sprite):
    def __init__(self, pos, surf, groups, radius, speed, start_angle, end_angle, z = get_z_layers('main')):
        self.__center = pos
        self.__radius = radius #tangente
        self.__speed = speed
        self.__start_angle = start_angle
        self.__end_angle = end_angle
        self.__angle = self.__start_angle #angulo alpha
        self.__direction = 1
        self.__full_circle = True if self.__end_angle == -1 else False
        #calculo do triangulo
        
        #cateto opositor
        y = self.__center[1] + sin(radians(self.__angle)) * self.__radius
        #cateto adjacente
        x = self.__center[0] + cos(radians(self.__angle)) * self.__radius
        super().__init__(( x, y ), surf, groups, z)


    def update(self, dt):
        self.__angle += self.__direction * self.__speed * dt

        if not self.__full_circle:
            if self.__angle >= self.__end_angle:
                self.__direction = -1
            if self.__angle < self.__start_angle:
                self.__direction = 1

        y = self.__center[1] + sin(radians(self.__angle)) * self.__radius
        x = self.__center[0] + cos(radians(self.__angle)) * self.__radius
        self.rect.center = ( x, y )

