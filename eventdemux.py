import pygame

class eventdemux:
	QUIT = 0
	ACTIVE = 1
	KEYDOWN = 2
	KEYUP = 3
	MOUSEMOTION = 4
	MOUSEBUTTONUP = 5
	MOUSEBUTTONDOWN = 6
	JOYAXISMOTION = 7
	JOYBALLMOTION = 8
	JOYHATMOTION = 9
	JOYBUTTONUP = 10
	JOYBUTTONDOWN = 11
	VIDEORESIZE = 12
	VIDEOEXPOSE = 13
	hregister = []
	eventtype = None

	def __init__(self):
		for i in range(256):
			self.hregister.append(list())
		print("pygame event queue demux init")

	def update(self):
		for event in pygame.event.get():
			try:
				for handler in self.hregister[event.type]:
					if handler["obj"]:
						if handler["f"]:
							handler["f"](handler["obj"], event)
					else:
						if handler["f"]:
							handler["f"](event)
			except IndexError:
				print("eventdemux.pygame: event %s not handled" % event.type)

	# register event handler, with an optional object that can be passed to the handler function
	# returns a handler ID that can be used to remove the handler
	def register(self, evtype, obj, f):
		# get free handler ID
		freeid = 0
		for handlers in self.hregister[evtype]:
			for handler in handlers:
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

	def unregister(self, hid):
		# find handler(s) with ID 'hid', remove it
		handlers = []
		for reg in self.hregister:
			for handler in reg:
				if handler["id"] == hid:
					handlers.remove(handler)