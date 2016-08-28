import copy
from entity import entity

class entities:
	"""
	entities_rw is the read-write entity list. this is the list the entities can access and modify.
	entities_ro is the read-only entity list. when the entities' think function is running, we cannot modify the list
	(that would result in an exception), so we have to double buffer. when the think-draw sequence is over, the RW list is
	copied into the RO.
	i think the constant copying will impact performance, but I don't know if there is a way to overlay an empty, read-write list
	over the RO list, then overwrite the RO with the overlay list.

	entities_ro --copy--> entities_rw
	think(entities_ro) [access: entities_rw]
	draw(entities_rw)
	entities_rw --copy--> entities_ro
	"""
	entities_rw = []
	entities_ro = []

	ro_lock = False

	def add(self, prefab): # add an already initialized and constructed entity to the system
		self.entities_rw.append(prefab)
		return prefab

	def create(self, name, *args): # create an entity with components specified in *args and add it to the system
		e = entity(name, args)
		self.entities_rw.append(e)

	def update(self, dt):
		self.ro_lock = True
		for entity in self.entities_ro:
			entity.update(dt)
		self.ro_lock = False

	def draw(self, target):
		for entity in self.entities_rw:
			entity.draw(target)

	def sync(self):
		if self.ro_lock:
			return
		self.entities_ro = copy.deepcopy(self.entities_rw)

	def clear(self):
		if self.ro_lock:
			return
		self.entities_ro = []

	def entbyname(self, name):
		finds = []
		for ent in self.entities_rw:
			if ent.name == name:
				finds.append(ent)
		if len(finds) == 1:
			return finds[0]
		else:
			return finds

	def removebyname(self, name):
		for ent in self.entities_rw:
			if ent.name == name:
				self.entities_rw.remove(ent)

	def removebyobj(self, obj):
		self.entities_rw.remove(ent)

	def dump(self):
		self.ro_lock = True
		for ent in self.entities_ro:
			print(ent)
			for k,v in ent.__dict__.items():
				print("\t%s : %s" % (k,v))
				if type(v) == list:
					for e in v:
						for k2, v2 in e.__dict__.items():
							print("\t\t%s : %s" % (k2,v2))
						print()
			print()