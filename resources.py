import os

import pygame
import emf

class resources:
	IMAGE	= 0 # image file
	SOUND	= 1 # sound file
	EMF		= 2 # tile map file
	FONT	= 3 # font file
	res = []
	def precache(self, restype, path):
		for resource in self.res:
			if resource["id"] == path:
				return
		resentry = {
			"id" : path,
			"type" : restype,
			"res" : None
		}
		path = os.path.join("assets/", path)
		if restype == resources.IMAGE:
			try:
				resentry["res"] = pygame.image.load(path)
				self.res.append(resentry)
			except Exception as e:
				print("resources: cannot precache image '%s': %s" % (path, str(e)))
		elif restype == resources.SOUND:
			pass
		elif restype == resources.EMF:
			try:
				with open(path, 'rb') as file:
					resentry["res"] = emf.VMF(path)
			except Exception as e:
				print("resources: cannot precache map file '%s': %s" % (path, str(e)))
		elif restype == resources.FONT:
			try:
				resentry["res"] = pygame.font.Font(path, 16)
				self.res.append(resentry)
			except Exception as e:
				print("resources: cannot precache font file '%s': %s" % (path, str(e)))


	def load(self, restype, path, late = False):
		for resource in self.res:
			if resource["id"] == path:
				return resource["res"]
		# late precache and try again
		if late: # prevent infinite loop
			return None
		self.precache(restype, path)
		return self.load(restype, path, True)

		