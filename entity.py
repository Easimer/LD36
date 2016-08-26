from component import component

class entity:
	name = ""
	components = []

	def __init__(self, name = "", *args):
		self.name = name
		print("creating entity with name \"%s\"" % name)
		for arg in args:
			self.components.append(arg)
			print("\tcomponent \"%s\" added" % str(arg))

	def update(self, dt):
		for c in self.components:
			c.update(dt)

	def draw(self, target):
		for c in self.components:
			c.draw(target)

	def getcomponent(self, type):
		return [ c for c in self.components if isinstance(c, component)]
