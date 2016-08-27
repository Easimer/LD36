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
		self.gamemgr.draw()
		self.renderer.postdraw()
		self.renderer.fratecap(60)

	def softreset(self): # reset everything, except the renderer and the gamemanager
		if hasattr(self, 'eventdemux'):
			self.eventdemux.deleteall()
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

def dot(v1, v2):
	s = 0
	for i in range(min(len(v1), len(v2))):
		s += v1[i] * v2[i]
	return s

def ptinrect(p, r, xywh = False):
	return not ((r[1] + r[3] <= p[1]) or (r[1] >= p[1]) or (r[0] >= p[0]) or (r[0] + r[2] <= p[0]))


	