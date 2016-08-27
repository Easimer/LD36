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
		entities_rw.append(prefab)
		return prefab

	def create(self, name, *args): # create an entity with components specified in *args and add it to the system
		e = entity(name, args)
		entities_rw.append(e)

	def update(self, dt):
		ro_lock = True
		for entity in self.entities_ro:
			entity.update(dt)
		ro_lock = False

	def draw(self, target):
		for entity in self.entities_rw:
			entity.draw(target)

	def sync(self):
		if ro_lock:
			return
		entities_ro = copy.deepcopy(entities_rw)

	def clear(self):
		if ro_lock:
			return
		entities_ro = []

	def entbyname(self, name):
		finds = []
		for ent in entities_rw:
			if ent.name == name:
				finds.append(ent)
		if len(finds) == 1:
			return finds[0]
		else:
			return finds

	def removebyname(self, name):
		for ent in entities_rw:
			if ent.name == name:
				entities_rw.remove(ent)

	def removebyobj(self, obj):
		entities_rw.remove(ent)

