import pygame
import uuid

class resources:
	IMAGE	= 0 # image file
	SOUND	= 1 # sound file
	EMF		= 2 # tile map file
	res = []
	def precache(self, restype, path):
		resentry = {
			"id" : path,
			"type" : restype,
			"res" : None
		}
		if restype == self.IMAGE:
			try:
				resentry["res"] = pygame.image.load(os.path.join("assets/", path))
				self.res.append(resentry)
			except Exception as e:
				print("resources: cannot precache resource: %s" % str(e))
		elif restype == self.SOUND:
			pass
		elif restype == self.EMF: # TODO: raise EMF lib from repo
			pass

	def load(self, restype, path):
		pass