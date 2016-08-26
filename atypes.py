from component import component

class vector:
	pos = [0, 0, 0] # cartesian

	def __init__(self, x = 0, y = 0, z = 0):
		self.pos[0] = x
		self.pos[1] = y
		self.pos[2] = z

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
		return pos[key]

	def __repr__(self):
		return "Vector(%s, %s, %s)" % tuple(pos)

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


class rotation(vector):

	def rotate(self, x, y, z):
		return rotation(x, y, z) + self

	def __repr__(self):
		return "Rotation(%s, %s, %s)" % tuple(rot)

class transform(component):
	position = vector()
	rotation = rotation()

class sprite2d(component):
	sprite = None