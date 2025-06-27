from settings import *
from asprite import AnimatedSprite
from sprites import Sprite

class ParticleEffectSprite(AnimatedSprite):
	def __init__(self, pos, frames, groups):
		super().__init__(pos, frames, groups)
		self.rect.center = pos
		self.z = get_z_layers('main')

	def animate(self, dt):
		self.frame_index += self.animation_speed * dt
		if self.frame_index < len(self.frames):
			self.image = self.frames[int(self.frame_index)]
		else:
			self.kill()