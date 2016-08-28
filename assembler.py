# Assembler (LD36) code

import os
import os.path

from entity import entity
from component import component
from atypes import transform, sprite2d, vector
from emf import VMF
import engine

partdefs = {}

def assembler_init():
	partfiles = [f for f in os.listdir("assets/parts/") if os.path.isfile(os.path.join("assets/parts/", f))]
	for file in partfiles:
		data = None
		with open(os.path.join("assets/parts", file)) as hfile:
			data = VMF(hfile).lBlocks
		if not data:
			continue
		for part in data:
			if not part["__classname__"] == "part":
				continue
			pdef = {}
			for k,v in part.items():
				if k == "name":
					partdefs[v] = pdef
				elif k.startswith("level"):
					pdef[k] = v in ["true", "yes", "1"]
				else:
					pdef[k] = v
	print(partdefs)

class part_cpoint(component):
	def __init__(self):
		self.position = None
		self.child = None


class part(component):
	parent = None
	sprite = None
	cpoint = None
	def __init__(self, pdef):
		if "texture" in pdef:
			print("texture set")
			self.sprite = sprite2d(pdef["texture"])
			self.sprite.parent = self
		self.cooldown = 0
		self.cooldownmax = 0
		self.radarcooldown = 0
		self.projectile = None
		self.currenttarget = None
		if "cooldown" in pdef:
			self.cooldown = 0
			self.cooldownmax = int(pdef["cooldown"])
		self.cpoints = []
		for subblock in pdef["__subblocks__"]:
			if subblock["__classname__"] == "cpoint":
				cpoint = part_cpoint()
				position = subblock["position"]
				print("add cpoint '%s'to part '%s'" % (position, self))
				cpoint.position = transform(position[0], position[1])
				print(cpoint.position.position)
				self.cpoints.append(cpoint)
			elif subblock["__classname__"] == "projectile":
				self.projectile = subblock

	def position(self):
		if self.vparent:
			#print("getting position of %s, with a parent %s" % (self, self.parent))
			if isinstance(self.vparent, entity): # if my parent is not a part, but an entity
				x = 0
				y = 0
				for comp in self.vparent.components: 
					if isinstance(comp, transform): # find it's transform
						x = comp.position[0]
						y = comp.position[0]
					elif isinstance(comp, sprite2d): # and it's sprite
						x -= comp.sprite.get_width() / 2
						y -= comp.sprite.get_height() / 2
				return (x, y)
			elif isinstance(self.vparent, part): # but if my parent is another part
				ppart = self.vparent # parent part
				ppos = ppart.position() # parent's position
				cpoint = self.cpoint.position.position # my connection point
				pos = (0, 0)
				if self.vparent and self.vparent.sprite:
					spr = self.vparent.sprite.sprite
					try:
						pos = (ppos[0] + cpoint[0] - spr.get_width() / 2, ppos[1] + cpoint[1] - spr.get_height() / 2)
					except Exception:
						pass
				else:
					pos = (ppos[0] + cpoint[0], ppos[1] + cpoint[1])
				return pos

	def remove(self):
		if self.cpoint:
			self.cpoint.child = None
			self.cpoint = None

	def draw(self, target):
		if self.sprite:
			p = self.position()
			target.drawsurf(self.sprite.sprite, p[0], p[1])

	def projimpact(self, target):
		print("IMPACT: " + str(target))

	def searchtarget(self):
		e = engine.engine.getengine()
		for ent in e.entities.entities_rw:
			for comp in ent.components:
				if isinstance(comp, enemy):
					self.currenttarget = ent
					return

	def update(self, dt):
		if self.cooldownmax != 0:
			self.cooldown -= dt
			self.radarcooldown -= dt
		else:
			return
		if self.radarcooldown <= 0:
			if not self.currenttarget:
				self.searchtarget()
			self.radarcooldown = 1
		if self.cooldown <= 0 and self.currenttarget:
			self.cooldown = self.cooldownmax
			if self.projectile:
				e = engine.engine.getengine().entities
				enemypos = None
				for comp in self.currenttarget.components:
					if isinstance(comp, transform):
						enemypos = comp.position
						break
				if enemypos:
					p = create_projectile(self.projectile["texture"], self.position(), (enemypos[0], enemypos[1]), float(self.projectile["speed"]), self.projimpact, self.currenttarget)


def create_machine_root():
	if "root" not in partdefs:
		raise Exception("root element not defined")
	e = entity("root")
	t = transform()
	p = part(partdefs["root"])
	p.vparent = e
	e.addcomponent(t)
	e.addcomponent(p)
	return e

def add_part(name, ent, parent):
	if not ent: # if the entity is None
		return
	if name not in partdefs: # if the part is not defined
		return
	p = part(partdefs[name]) # create part
	print("add_part '%s' '%s' '%s'" % (name, ent, parent))
	if parent: # if parent is specified
		p.vparent = parent
		print("\tvparent: " + str(p.vparent))
		for cpoint in parent.cpoints:
			if cpoint.child:
				print("\thas child, cont")
				continue
			print("\tcpoint: " + str(cpoint))
			p.cpoint = cpoint
			cpoint.child = p
			break
	else: # otherwise
		p.vparent = ent # the entity will be it's parent
		p.cpoint = None
	ent.addcomponent(p)
	return p

def add_part_nextcpoint(name, ent): # create part and connect it to the first free cpoint
	if not ent:
		return
	if isinstance(ent, entity):
		entfree = True
		for comp in ent.components:
			if isinstance(comp, part):
				for cpoint in comp.cpoints:
					if not cpoint.child:
						return add_part(name, ent, comp)
				if comp.vparent == ent:
					entfree = False
		# no point with 
		if entfree:
			return add_part(name, ent, None)

class projectile(component):
	def __init__(self, vfrom, vto, speed, onarrival = None, obj = None):
		self.onarrival = onarrival
		self.obj = obj
		self.vfrom = vfrom
		self.vto = vto
		self.vector = (vto - vfrom).normalize() * vector(speed, speed, speed)
		self.pathlength = (vto - vfrom).length

	def setvector(self, vfrom, vto, speed):
		self.vfrom = vfrom
		self.vto = vto
		self.vector = (vto - vfrom).normalize() * vector(speed, speed, speed)
		self.pathlength = (vto - vfrom).length


	def update(self, dt):
		if not hasattr(self, 'position'):
			for comp in self.parent.components:
				if isinstance(comp, transform):
					self.position = transform
		vdt = vector(dt, dt, dt)
		self.position.position += (self.vector * vdt)
		if (self.position.position - self.vfrom).length() > self.pathlength:
			if self.onarrival:
				self.onarrival(self, self.obj)
			e = engine.engine.getengine()
			self.parent.components = [] # kill myself...
			e.entities.removebyobj(self.parent) # ...but first murder my parent


def create_projectile(image, vfrom, vto, speed, onarrival = None, obj = None):
	t = transform(*vto)
	p = projectile(vector(*vfrom), vector(*vto), speed, onarrival, obj)
	s = sprite2d(image)
	e = entity("projectile", t, p)
	return e


class enemy(component):
	def __init__(self, health = 100, wave = 1):
		self.maxhealth = health
		self.health = health
		self.wave = wave

	def update(self, dt):
		pass

def create_enemy(pos, image, health = 100, wave = 1):
	ec = enemy(health, wave)
	s = sprite2d(image)
	t = transform(pos[0], pos[1])
	e = entity("enemy", ec, s, t)
	return e