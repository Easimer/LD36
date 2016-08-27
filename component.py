class component:
	parent = None
	__unregisterme__ = False
	def update(self, dt):
		pass
	def draw(self, target):
		pass

	def __del__(self):
		pass