import engine
import gui

class gamemgr:
	STATE_MENU = 0
	STATE_GAME = 1
	STATE_PAUSED = 2

	state = STATE_MENU

	lastcheck = 0

	pausescreen = None

	def __init__(self):
		e = engine.engine.getengine()
		self.gui = gui.gui("assets/res/mainmenu.res")
		e.renderer.settitle("Assembler")

	def update(self):
		e = engine.engine.getengine()
		self.lastcheck += 1
		if self.lastcheck == 8:
			e.eventdemux.checkhandlers() # check if a handler should be removed
			self.lastcheck = 0
		e.eventdemux.update()
		if self.state == gamemgr.STATE_GAME:
			e.entities.update(e.renderer.dt)
		self.gui.update(e.renderer.dt)
		

	def draw(self):
		e = engine.engine.getengine()
		if self.state == gamemgr.STATE_GAME:
			e.entitites.draw(e.renderer)
		self.gui.draw(e.renderer)

	def switchstate(self, newstate):
		e = engine.engine.getengine()
		if self.state == 	gamemgr.STATE_MENU and newstate ==		gamemgr.STATE_GAME:
			e.softreset()
		elif self.state ==	gamemgr.STATE_GAME and newstate ==		gamemgr.STATE_PAUSED:
			self.pausescreen = e.renderer.surface.copy()
		elif self.state ==	gamemgr.STATE_PAUSED and newstate ==	gamemgr.STATE_GAME:
			print("yes")
			self.pausescreen = None
		elif self.state ==	gamemgr.STATE_PAUSED and newstate == 	gamemgr.STATE_MENU:
			e.softreset()
		else:
			raise Exception("gamemgr: invalid state transition (%s -> %s)" % (self.state, newstate))