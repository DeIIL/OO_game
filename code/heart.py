from asprite import AnimatedSprite
from random import randint

class Heart(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False


    def animate(self,dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0

    def update(self, dt):
        if self.active:
            self.animate(dt)
        else:
            if randint(0,2000) == 1:
                self.active = True