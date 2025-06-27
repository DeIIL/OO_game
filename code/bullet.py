from settings import *
from timer import Timer

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf, direction, speed):
        super().__init__(groups)
        self.bullet = True
        self.image = surf
        self.rect = self.image.get_frect( center = pos + vector( 50 * direction, 0 ))
        self.__direction = direction
        self.__speed = speed
        self.z = get_z_layers('main')
        self.timers = {'lifetime': Timer(5000) , 'reverse': Timer(250)}
        self.timers['lifetime'].activate()

    def reverse(self):
            if not self.timers['reverse'].active:
                 self.__direction *= -1
                 self.timers['reverse'].activate()

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()
        self.rect.x += self.__direction * self.__speed * dt
        if not self.timers['lifetime'].active:
            self.kill()