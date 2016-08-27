from component import component

class entity:
	name = ""
	components = []
	__unregisterme__ = False

	def __init__(self, name = "", *args):
		self.name = name
		self.components = []
		for arg in args:
			arg.parent = self
			self.components.append(arg)

	def update(self, dt):
		for c in self.components:
			c.update(dt)

	def draw(self, target):
		for c in self.components:
			c.draw(target)

	def __del__(self):
		for component in self.components:
			component.__del__()

	def addcomponent(self, component):
		component.parent = self
		self.components.append(component)
