import sys

from renderer import renderer
from eventdemux import eventdemux
from resources import resources
from entities import entities
from gamemgr import gamemgr

__engine = None

class engine:
	__unregisterme__ = False
	def __init__(self):
		global __engine
		__engine = self
		
		self.renderer = renderer()
		self.softreset()
		self.gamemgr = gamemgr()

		print("engine init %s" % str(self))

	def loop(self):
		dt = self.renderer.dt
		self.renderer.predraw()
		self.gamemgr.update()
		self.renderer.postdraw()

	def softreset(self): # reset everything, except the renderer and the gamemanager
		self.eventdemux = eventdemux()
		self.resources = resources()
		self.entities = entities()
		self.eventdemux.register(eventdemux.QUIT, self, engine.quit)

	def quit(self, ev):
		self.renderer.shutdown()
		sys.exit(0)

	@staticmethod
	def getengine():
		return __engine