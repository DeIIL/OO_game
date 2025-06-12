from pygame.time import get_ticks

class Timer:
	def __init__(self, duration, func = None, repeat = False):
		self.__duration = duration
		self.func = func
		self.__start_time = 0
		self.__active = False
		self.__repeat = repeat

	@property
	def active(self):
		return self.__active
	
	@active.setter
	def active(self, value):
		self.__active = value

	def activate(self):
		self.__active = True
		self.__start_time = get_ticks()

	def deactivate(self):
		self.__active = False
		self.__start_time = 0
		if self.__repeat:
			self.activate()

	def update(self):
		current_time = get_ticks()
		if current_time - self.__start_time >= self.__duration:
			if self.func and self.__start_time != 0:
				self.func()
			self.deactivate()

