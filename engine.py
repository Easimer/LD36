import sys

import renderer
from renderer import renderer
import eventdemux
from eventdemux import eventdemux
import resources
from resources import resources

engine = None

class engine:
	def __init__(self):
		global engine
		engine = self
		
		self.renderer = renderer()
		self.eventdemux = eventdemux()
		self.resources = resources()

		self.eventdemux.register(eventdemux.QUIT, self, engine_quit)

	def enginequit(self, ev):
		pygame.quit()
		sys.exit(0)