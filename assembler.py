# Assembler (LD36) entity factories

from entity import entity
from component import component
from atypes import transform, sprite2d

# a point where parts can connect
class part_cpoint(component):
	position = transform()
	child = None

	def setchild(self, child):
		self.child = child

class part(component):
	def __init__(self, image, *args):
		self.sprite = sprite2d(image)
		self.cpoints = []
		for arg in args:
			cpoint = part_cpoint()
			cpoint.position = transform(arg[0], arg[1])
			self.cpoints.append(cpoint)

	def setparent(self, parent):
		self.parent = parent
		self.sprite.parent = self.parent

	def draw(self, target):
		self.sprite.draw(target)

def create_machine(name):
	e = entity(name)
	t = transform()
	p = part("textures/4body.png")
	p.setparent(e)
	e.addcomponent(t)
	e.addcomponent(p)
	return e