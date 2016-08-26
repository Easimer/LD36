class renderer:
	pygame = None
	surface = None

	lasttime = 0

	def __init__(self, width = 1280, height = 720):
		global current
		current = self
		import pygame
		self.pygame = pygame 
		self.pygame.init()
		self.surface = self.pygame.display.set_mode((width, height))
		self.lasttime = self.pygame.time.get_ticks()
		print("pygame renderer initialized")

	@property
	def width(self):
		return self.pygame.display.Info().current_w

	@property
	def height(self):
		return self.pygame.display.Info().current_h

	def postdraw(self):
		self.pygame.display.flip()

	@property
	def dt(self):
		t = self.pygame.time.get_ticks()
		dt = t - self.lasttime
		self.lasttime = t
		return dt

	def quit(self):
		self.pygame.quit()

	def predraw(self):
		pass

	def postdraw(self):
		pass
