import engine
import gui
import pprint

import assembler

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

	gold = 0
	parts = 0
	parts_max = 100
	wave = 1

	gui_label_gold = None
	gui_label_parts = None
	gui_label_wave = None

	def __init__(self):
		e = engine.engine.getengine()
		e.renderer.settitle("Assembler")
		self.gui_mainmenu = gui.gui_root("assets/res/mainmenu.res")
		self.gui_assembler = gui.gui_root("assets/res/assembler.res")
		self.gui_active = self.gui_mainmenu

		assembler.assembler_init()
		
		self.gui_label_gold = self.gui_assembler.findelementbyid("label_gold")
		self.gui_label_parts = self.gui_assembler.findelementbyid("label_parts")
		self.gui_label_wave = self.gui_assembler.findelementbyid("label_wave")

		self.set_gold(100)


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
			e.entities.sync()
		if self.gui_active:
			self.gui_active.update(e.renderer.dt)

	def draw(self):
		e = engine.engine.getengine()
		e.renderer.draw_grid()
		if self.state == gamemgr.STATE_GAME:
			e.entities.draw(e.renderer)
		if self.gui_active:
			self.gui_active.draw(e.renderer)

	def switchstate(self, newstate): # change self.state next cycle
		self.__switchstate = newstate

	def __switchstatef(self, newstate):
		e = engine.engine.getengine()
		if self.state == 	gamemgr.STATE_MENU and newstate ==		gamemgr.STATE_GAME:
			e.softreset()
			self.gui_active = self.gui_assembler

			self.player = assembler.create_machine_root()
			e.entities.add(self.player)
			e.renderer.camera = self.player
			e.entities.add(assembler.create_enemy((600, 50), "textures/enemy/test.png"))
		elif self.state ==	gamemgr.STATE_GAME and newstate ==		gamemgr.STATE_PAUSED:
			self.pausescreen = e.renderer.surface.copy()
			self.gui_active = self.gui_pausemenu
		elif self.state ==	gamemgr.STATE_PAUSED and newstate ==	gamemgr.STATE_GAME:
			self.pausescreen = None
			self.gui_active = self.gui_assembler
		elif self.state ==	gamemgr.STATE_PAUSED and newstate == 	gamemgr.STATE_MENU:
			e.softreset()
			self.gui_active = self.gui_mainmenu
		else:
			raise Exception("gamemgr: invalid state transition (%s -> %s)" % (self.state, newstate))
		self.state = newstate
		self.__switchstate = None

	def set_gold(self, value):
		self.gold = value
		self.gui_label_gold.text = "Gold: %d" % self.gold
		self.gui_label_gold.gensurf()

	def add_gold(self, amount):
		self.set_gold(self.gold + amount)

	def set_parts(self, value):
		self.parts = value
		self.gui_label_parts.text = "Parts: %d/%d" % (self.parts, self.parts_max)
		self.gui_label_parts.gensurf()

	def set_wave(self, wave):
		self.wave += 1
		self.gui_label_wave.text = "Wave %d" % self.wave
		self.gui_label_wave.gensurf()

	def buypart(self, partname):
		p = assembler.add_part_nextcpoint(partname, self.player)
		try:
			self.add_gold(-p.cost)
		except AttributeError:
			pass
		