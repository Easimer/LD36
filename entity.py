from component import component

class entity:
	name = ""
	components = []
	__unregisterme__ = False

	def __init__(self, name = "", *args):
		self.name = name
		self.components = []
		print("creating entity with name \"%s\"" % name)
		for arg in args:
			arg.parent = self
			self.components.append(arg)
			print("\tcomponent \"%s\" added" % str(arg))

	def update(self, dt):
		print("entity updated: %s" % self)
		for c in self.components:
			print("\tcomponent: %s" % c)
			c.update(dt)

	def draw(self, target):
		print("entity drawn: %s" % self)
		for c in self.components:
			print("\tcomponent: %s" % c)
			c.draw(target)

	def getcomponents(self, type):
		return [ c for c in self.components if isinstance(c, component)]

	def getcomponent(self, type):
		return self.getcomponents(type)[0]

	def __del__(self):
		for component in self.components:
			component.__del__()

	def addcomponent(self, component):
		component.parent = self
		self.components.append(component)
