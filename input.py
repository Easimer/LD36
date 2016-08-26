from component import component

class keyboardinput(component):
	def __init__(self):


	def update(self, parent, dt):
		if parent.input:
			parent.input()
	def draw(self, parent, target):
		pass