import pygame
from atypes import vector
from atypes import transform

class renderer:
	surface = None
	camera = None # an entity with a Transform component
	width = 0
	height = 0

	lasttime = 0

	def __init__(self, width = 1280, height = 720):
		
		pygame.init()
		self.surface = pygame.display.set_mode((width, height))
		self.lasttime = pygame.time.get_ticks()
		self.width = width
		self.height = height
		self.clock = pygame.time.Clock()
		print("pygame renderer initialized")

	def postdraw(self):
		pygame.display.flip()

	@property
	def dt(self):
		t = pygame.time.get_ticks()
		dt = t - self.lasttime
		self.lasttime = t
		return dt

	def quit(self):
		pygame.quit()

	def predraw(self):
		self.surface.fill((127, 104, 94))

	def postdraw(self):
		pygame.display.flip()

	def settitle(self, title):
		pygame.display.set_caption(title)

	def drawsurf(self, surface, x, y):
		# translate world coordinates to screen coordinates
		tx = x
		ty = y
		if self.camera:
			for comp in self.camera.components:
				if isinstance(comp, transform):
					newcoord = comp.position - vector(x, y)
					tx = self.width / 2 + newcoord.x
					ty = self.height / 2 + newcoord.y
					break
		self.surface.blit(surface, (tx, ty))

	def drawsurfgui(self, surface, x, y):
		# don't translate coordinates
		self.surface.blit(surface, (x, y))

	def getsurf(self, w = 128, h = 128):
		return pygame.Surface((w, h))

	def getrect(self, x = 0, y = 0, w = 128, h = 128):
		return pygame.Rect(x, y, w, h)

	def shutdown(self):
		pygame.quit()

	def fratecap(self, fps):
		self.clock.tick(fps)

	def draw_grid(self): # fill screen with a white grid
		s = pygame.Surface((1280, 720))
		s.set_colorkey((0, 0, 0))
		s.set_alpha(128)
		# draw main lines
		y = 0
		for i in range(10):
			pygame.draw.line(s, (255, 255, 255), (0, y), (1280, y), 2 if y % 48 == 0 else 1)
			y += 72
		x = 0
		for i in range(18):
			pygame.draw.line(s, (255, 255, 255), (x, 0), (x, 720), 2 if x % 48 == 0 else 1)
			x += 72

		self.surface.blit(s, (0,0))

	def setcamera(self, newcamera):
		self.camera = newcamera