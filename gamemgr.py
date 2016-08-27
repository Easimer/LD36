import engine

class gamemgr:
	STATE_MENU = 0
	STATE_GAME = 1
	STATE_PAUSED = 2

	state = STATE_MENU

	lastcheck = 0

	def update(self):
		e = engine.engine.getengine()
		self.lastcheck += 1
		if self.lastcheck == 8:
			e.eventdemux.checkhandlers() # check if a handler should be removed
			self.lastcheck = 0
		e.eventdemux.update()
		if self.state == gamemgr.STATE_GAME:
			e.entities.update(e.renderer.dt)
		

	def draw(self):
		e = engine.engine.getengine()
		e.entitites.draw(e.renderer)