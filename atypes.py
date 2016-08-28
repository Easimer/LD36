import engine
from component import component
from entity import entity

class vector:

	def __init__(self, x = 0, y = 0, z = 0):
		self.pos = [0, 0, 0]
		self.pos[0] = int(x)
		self.pos[1] = int(y)
		self.pos[2] = int(z)

	def __len__(self):
		return 3

	@property
	def x(self):
		return self.pos[0]

	@property
	def y(self):
		return self.pos[1]

	@property
	def z(self):
		return self.pos[2]

	def __getitem__(self, key):
		if key > 2:
			raise IndexError()
		return self.pos[key]

	def __repr__(self):
		return "Vector(%s)" % self.pos

	def __eq__(self, other):
		if not isinstance(other, vector):
			return False
		for c in zip(self.pos, other.pos):
			if c[0] != c[1]:
				return False
		return True

	def __ne__(self, other):
		if not isinstance(other, vector):
			return False
		for c in zip(self.pos, other.pos):
			if c[0] == c[1]:
				return False
		return True

	def __nonzero__(self):
		for c in self.pos:
			if bool(c):
				return True
		return False

	def __add__(self, other):
		return vector(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other):
		return vector(self.x - other.x, self.y - other.y, self.z - other.z)

	def __rsub__(self, other):
		return vector(other.x - self.x, other.y - self.y, other.z - self.z)

	def __mul__(self, other):
		return vector(self.x * other.x, self.y * other.y, self.z * other.z)

	def __div__(self, other):
		return vector(self.x / other.x, self.y / other.y, self.z / other.z)

	@property
	def length(self):
		return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** (1/2)

	def normalize(self):
		length = self.length
		return vector(self.x / length, self.y / length, self.z / length)


class rotation(vector):

	def rotate(self, x, y, z):
		return rotation(x, y, z) + self

	def __repr__(self):
		return "Rotation(%s, %s, %s)" % tuple(self.pos)

class transform(component):
	def __init__(self, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0):
		self.position = vector(x, y, z)
		self.rotation = rotation(rx, ry, rz)


class sprite2d(component):
	def __init__(self, path, offset = (0, 0, 0)):
		e = engine.engine.getengine()
		e.resources.precache(e.resources.IMAGE, path)
		self.sprite = e.resources.load(e.resources.IMAGE, path)
		self.offset = vector(*offset)
		self.parent = None


	def draw(self, target):
		if not self.parent or not self.sprite:
			return
		t = None
		if isinstance(self.parent, entity): # if my parent is an entity
			for comp in self.parent.components:
				if isinstance(comp, transform): # find it's transform
					t = comp
					target.drawsurf(self.sprite, t.position.x, t.position.y) # and that position will be my position too!
					return
		elif isinstance(self.parent, component): # but if my parent is a component
			try: # try if it has position attrib
				pos = self.parent.position()
				target.drawsurf(self.sprite, pos[0], pos[1]) # then that position will be my position too!
			except AttributeError:
				pass