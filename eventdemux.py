import pygame

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

class eventdemux:
	hregister = []
	eventtype = None

	def __init__(self):
		for i in range(14):
			self.hregister.append(list())
		self.eventtype = {
			QUIT : pygame.QUIT,
			ACTIVE : pygame.ACTIVEEVENT,
			KEYDOWN : pygame.KEYDOWN,
			KEYUP : pygame.KEYUP,
			MOUSEMOTION : pygame.MOUSEMOTION,
			MOUSEBUTTONUP : pygame.MOUSEBUTTONUP,
			MOUSEBUTTONDOWN : pygame.MOUSEBUTTONDOWN,
			JOYAXISMOTION : pygame.JOYAXISMOTION,
			JOYBALLMOTION : pygame.JOYBALLMOTION,
			JOYHATMOTION : pygame.JOYHATMOTION,
			JOYBUTTONUP : pygame.JOYBUTTONUP,
			JOYBUTTONDOWN : pygame.JOYBUTTONDOWN,
			VIDEORESIZE : pygame.VIDEORESIZE,
			VIDEOEXPOSE : pygame.VIDEOEXPOSE,
		}
		print("pygame event queue demux init")

	def update(self):
		for event in pygame.event.get():
			try:
				for handler in self.hregister[self.transevtype(event.type)]:
					if handler["obj"]:
						if handler["f"]:
							handler["f"](handler["obj"], event)
					else:
						if handler["f"]:
							handler["f"](event)
			except IndexError:
				print("eventdemux.pygame: event %s (internal ID: %s) not handled" % (event.type, self.transevtype(event.type)))
	def transevtype(self, eventtype): # evdemux event type -> custom event type
		for k,v in self.eventtype.items():
			if v == eventtype:
				return k

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