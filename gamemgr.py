import engine
import gui
import signal

class gamemgr:
	STATE_MENU = 0
	STATE_GAME = 1
	STATE_PAUSED = 2

	state = STATE_MENU

	lastcheck = 0

	pausescreen = None

	__switchstate = None

	gui_active = None
	gui_mainmenu = None
	gui_assembler = None
	gui_pausemenu = None

	def __init__(self):
		e = engine.engine.getengine()
		e.renderer.settitle("Assembler")
		self.gui_mainmenu = gui.gui_root("assets/res/mainmenu.res")
		self.gui_assembler = gui.gui_root("assets/res/assembler.res")
		self.gui_active = self.gui_mainmenu
		print("active: %s mm: %s assembler: %s" % (self.gui_active, self.gui_mainmenu, self.gui_assembler))


	def update(self):
		if self.__switchstate:
			self.__switchstatef(self.__switchstate)
		e = engine.engine.getengine()
		self.lastcheck += 1
		if self.lastcheck == 8:
			e.eventdemux.checkhandlers() # check if a handler should be removed
			self.lastcheck = 0
		e.eventdemux.update()
		if self.state == gamemgr.STATE_GAME:
			e.entities.update(e.renderer.dt)
		if self.gui_active:
			self.gui_active.update(e.renderer.dt)
		

	def draw(self):
		e = engine.engine.getengine()
		if self.state == gamemgr.STATE_GAME:
			e.entitites.draw(e.renderer)
		if self.gui_active:
			self.gui_active.draw(e.renderer)

	def switchstate(self, newstate): # change self.state next cycle
		self.__switchstate = newstate

	def __switchstatef(self, newstate):
		e = engine.engine.getengine()
		if self.state == 	gamemgr.STATE_MENU and newstate ==		gamemgr.STATE_GAME:
			e.softreset()
			self.gui_active = self.gui_assembler
		elif self.state ==	gamemgr.STATE_GAME and newstate ==		gamemgr.STATE_PAUSED:
			self.pausescreen = e.renderer.surface.copy()
			self.gui_active = self.gui_pausemenu
		elif self.state ==	gamemgr.STATE_PAUSED and newstate ==	gamemgr.STATE_GAME:
			print("yes")
			self.pausescreen = None
			self.gui_active = self.gui_assembler
		elif self.state ==	gamemgr.STATE_PAUSED and newstate == 	gamemgr.STATE_MENU:
			e.softreset()
			self.gui_active = self.gui_mainmenu
		else:
			raise Exception("gamemgr: invalid state transition (%s -> %s)" % (self.state, newstate))
		self.__switchstate = None