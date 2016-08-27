import pygame
import uuid
import emf

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
				print("resources: cannot precache image '%s': %s" % (path, str(e)))
		elif restype == self.SOUND:
			pass
		elif restype == self.EMF:
			try:
				with open(path, 'rb') as file:
					resentry["res"] = emf.VMF(file)
			except Exception as e:
				print("resources: cannot precache map file '%s': %s" % (path, str(e)))

	def load(self, restype, path, late = False):
		for resource in self.res:
			if resource["id"] == path:
				return resource["res"]
		# late precache and try again
		if late: # prevent infinite loop
			return None
		self.precache(restype, path)
		self.load(restype, path, True)

		