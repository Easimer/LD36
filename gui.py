from emf import VMF
from entity import entity
import engine
from eventdemux import eventdemux

class gui(entity):

	elements = []
	font = None
	__unregisterme__ = False

	def __init__(self, deffilename):
		definition = None
		e = engine.engine.getengine()

		with open(deffilename) as file:
			definition = VMF(file).lBlocks
		root = [block for block in definition if block["__classname__"] == "root"][0]
		if not root:
			print("gui: no root found in resfile %s" % deffilename)
			return
		# set and load default font
		if "defaultfont" in root:
			e.resources.precache(e.resources.FONT, root["defaultfont"])
			self.font = e.resources.load(e.resources.FONT, root["defaultfont"])
		# init subelements
		for subblock in root["__subblocks__"]:
			if subblock["__classname__"] == "window":
				w = gui_window(self, subblock["title"], subblock["position"], subblock["size"], subblock["__subblocks__"])
				if "bgcolor" in subblock:
					w.setbgcolor(subblock["bgcolor"])
				self.elements.append(w)
		evdm = e.eventdemux
		evdm.register(eventdemux.MOUSEMOTION, self, gui.mouseevent)
		evdm.register(eventdemux.MOUSEBUTTONUP, self, gui.mouseevent)
		evdm.register(eventdemux.MOUSEBUTTONDOWN, self, gui.mouseevent)

	def draw(self, target):
		for element in self.elements:
			element.draw(target)

	def mouseevent(self, ev):
		for element in self.elements:
			element.mouseevent(ev)

	def __del__(self):
		self.__unregisterme__ = True



class gui_window(gui):
	parent = None
	root = None
	title = ""
	titlesurf = None
	bgcolor = (64, 64, 64)
	barbgcolor = (48, 48, 48)

	def __init__(self, parent, title, position, size, subelems):
		self.parent = parent
		self.title = title
		self.position = position
		self.size = size
		self.titlesurf = self.parent.font.render(self.title, False, (212, 212, 212))
		print("window: title: %s pos: %s size: %s" % (title, position, size))
		self.elements = []
		for elem in subelems:
			if elem["__classname__"] == "label":
				l = gui_label(self, elem["text"], elem["position"])
				if "color" in elem:
					l.color = elem["color"]
				self.elements.append(l)
			if elem["__classname__"] == "button":
				b = gui_button(self, elem["text"], elem["position"], elem["size"], elem["onclick"])
				if "bgcolor" in elem:
					b.color = elem["bgcolor"]
				self.elements.append(b)

	def setbgcolor(self, color):
		if len(color) not in [3, 4]:
			return
		self.bgcolor = color
		self.barbgcolor = [(val - 16) for val in color]

	def draw(self, target):
		s = target.getsurf(self.size[0], self.size[1])
		s.fill(self.bgcolor)
		if self.title or len(self.title) > 0:
			s.fill(self.barbgcolor, target.getrect(0, 0, self.size[0], 32))
			s.blit(self.titlesurf, (8, 8))
		target.drawsurfgui(s, self.position[0], self.position[1])
		for elem in self.elements:
			elem.draw(target)

	def mouseevent(self, ev):
		if not engine.ptinrect(ev.pos, (self.position + self.size)):
			return
		for element in self.elements:
			realpos = [element.position[0] + self.position[0], element.position[1] + self.position[1]]
			if engine.ptinrect(ev.pos, (realpos + element.size), True):
				element.mouseevent(ev)

	def close(self):
		self.elements = []

class gui_label(gui):
	surf = None
	def __init__(self, parent, text, position, color = (255, 255, 255)):
		self.parent = parent
		self.text = text
		self.position = position
		self.color = color
		self.surf = self.parent.parent.font.render(self.text, False, self.color)
		print("\tlabel: text: %s pos: %s color: %s" % (self.text, self.position, self.color))

	def draw(self, target):
		target.drawsurfgui(self.surf, self.parent.position[0] + self.position[0], self.parent.position[1] + self.position[1] + 32)

class gui_button(gui):
	surf = None
	surf_clicked = None

	clicked = False

	def __init__(self, parent, text, position, size, onclick, color = (212, 212, 212)):
		self.parent = parent
		self.text = text
		self.position = position
		self.size = size
		self.setbgcolor(color)
		if onclick in gui_action:
			self.onclick = gui_action[onclick]
		else:
			print("button(%s): GUI action '%s' not found. the button will do nothing." % (str(self) if not hasattr(self, 'id') else self.id, onclick))

		e = engine.engine.getengine()
		self.surf = e.renderer.getsurf(*self.size)
		self.surf.fill(self.bgcolor)
		self.surf.blit(self.parent.parent.font.render(self.text, False, (255, 255, 255)), (8, 8))

		self.surf_clicked = e.renderer.getsurf(*self.size)
		self.surf_clicked.fill(self.bgcolor_clicked)
		self.surf_clicked.blit(self.parent.parent.font.render(self.text, False, (255, 255, 255)), (8, 8))

		print("\tbutton: text: %s pos: %s color: %s action: %s" % (self.text, self.position, self.bgcolor, onclick))
	def setbgcolor(self, color):
		if len(color) not in [3, 4]:
			return
		self.bgcolor = color
		self.bgcolor_clicked = [(val - 16) for val in color]

	def mouseevent(self, ev):
		if ev.type == eventdemux.MOUSEBUTTONUP:
			if ev.button == 1:
				self.onclick(self)

	def draw(self, target):
		if self.clicked:
			target.drawsurfgui(self.surf_clicked, self.parent.position[0] + self.position[0], self.parent.position[1] + self.position[1])
		else:
			target.drawsurfgui(self.surf, self.parent.position[0] + self.position[0], self.parent.position[1] + self.position[1])

# define your gui actions right down here fam

def print_meme(self):
	print("meme")

def mainmenu_start(self):
	pass

gui_action = {
	"print_meme" : print_meme,
	"mainmenu_start" : mainmenu_start,
}