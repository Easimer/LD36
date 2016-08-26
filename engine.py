import sys

from renderer import renderer
from eventdemux import eventdemux
from resources import resources

engine = None

class engine:
	def __init__(self):
		global engine
		engine = self
		
		self.renderer = renderer()
		self.eventdemux = eventdemux()
		self.resources = resources()

		self.eventdemux.register(eventdemux.QUIT, self, engine.quit)

	def quit(self, ev):
		pygame.quit()
		sys.exit(0)