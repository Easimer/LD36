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
		self.eventdemux = eventdemux()
		self.eventdemux.register(eventdemux.QUIT, self, engine.quit)
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

	def softreset(self):	
		self.resources = resources()
		self.entities = entities()
		

	def quit(self, ev):
		self.renderer.shutdown()
		sys.exit(0)

	def __repr__(self):
		return "engine\n\trenderer: %s\n\tentities: %s\n\tgamemgr: %s\n\teventdemux: %s" % (self.renderer, self.entities, self.gamemgr, self.eventdemux)

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


	