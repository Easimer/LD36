class component:
	parent = None
	__unregisterme__ = False
	def update(self, parent, dt):
		pass
	def draw(self, parent, target):
		pass

	def __del__(self):
		pass