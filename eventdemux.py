import pygame

class eventdemux:
	QUIT = pygame.QUIT
	ACTIVE = pygame.ACTIVEEVENT
	KEYDOWN = pygame.KEYDOWN
	KEYUP = pygame.KEYUP
	MOUSEMOTION = pygame.MOUSEMOTION
	MOUSEBUTTONUP = pygame.MOUSEBUTTONUP
	MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
	JOYAXISMOTION = pygame.JOYAXISMOTION
	JOYBALLMOTION = pygame.JOYBALLMOTION
	JOYHATMOTION = pygame.JOYHATMOTION
	JOYBUTTONUP = pygame.JOYBUTTONUP
	JOYBUTTONDOWN = pygame.JOYBUTTONDOWN
	VIDEORESIZE = pygame.VIDEORESIZE
	VIDEOEXPOSE = pygame.VIDEOEXPOSE

	hregister = []
	eventtype = None

	def __init__(self):
		for i in range(128):
			self.hregister.append(list())
		print("pygame event queue demux init")

	def update(self):
		for event in pygame.event.get():
			#try:
				#print("event %s" % str(event))
				for handler in self.hregister[event.type]:
					if handler["obj"]:
						if handler["f"]:
							handler["f"](handler["obj"], event)
					else:
						if handler["f"]:
							handler["f"](event)
			#except IndexError:
			#	print("eventdemux.pygame: event %s not handled" % event.type)

	def checkhandlers(self):
		for handlers in self.hregister:
			for handler in handlers:
				if not handler["obj"]:
					continue
				if handler["obj"].__unregisterme__:
					self.unregister(handler["id"])

	# register event handler, with an optional object that can be passed to the handler function
	# returns a handler ID that can be used to remove the handler
	def register(self, evtype, obj, f):
		# get free handler ID
		freeid = 0
		for handler in self.hregister[evtype]:
			if handler["id"] == freeid:
				freeid += 1
		# create register entry
		handler = {
			"id" : freeid,
			"obj" : obj,
			"f" : f
		}
		# add handler
		self.hregister[evtype].append(handler)
		return handler["id"]

	def unregister(self, hid):
		# find handler(s) with ID 'hid', remove it
		for reg in self.hregister:
			for handler in reg:
				if handler["id"] == hid:
					reg.remove(handler)

	def deleteall(self):
		for reg in self.hregister:
			for handler in reg:
				for k in handler:
					handler[k] = None
			reg = []
		self.hregister = []