import pygame
import uuid

IMAGE	= 0 # image file
SOUND	= 1 # sound file
EMF		= 2 # tile map file

class resources:

	res = []
	def precache(self, restype, path):
		resentry = {
			"id" : path,
			"type" : restype,
			"res" : None
		}
		if restype == IMAGE:
			try:
				resentry["res"] = pygame.image.load(os.path.join("assets/", path))
				self.res.append(resentry)
			except Exception as e:
				print("resources: cannot precache resource: %s" % str(e))
		elif restype == SOUND:
			pass
		elif restype == EMF: # TODO: raise EMF lib from repo
			pass

	def load(self, restype, path):
		pass