from component import component
import engine as e

class keyboardinput(component):
	def __init__(self):
		evdm = e.engine.getengine().eventdemux
		evdm.register(eventdemux.KEYDOWN, self, keyboardinput.keyhandler)
		evdm.register(eventdemux.KEYUP, self, keyboardinput.keyhandler)


	def keyhandler(self, ev):


	def update(self, parent, dt):
		if parent.input:
			parent.input()
	def draw(self, parent, target):
		pass

	def __del__(self):
		self.__unregisterme__ = True