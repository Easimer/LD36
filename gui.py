from emf import VMF
from entity import entity
import engine
from eventdemux import eventdemux

class gui(entity):
	def __init__(self):
		self.elements = []
		self.font = None
		self.__unregisterme__ = False
		self.visible = True
		self.id = None
		self.position = [0, 0]
		self.size = [0, 0]

	def update(self, dt):
		pass

	def draw(self, target):
		pass

	def mouseevent(self, ev):
		pass

	def setbgcolor(self, color):
		pass

	
class gui_root(gui):
	def __init__(self, deffilename):
		super().__init__()
		e = engine.engine.getengine()
		definition = None

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
		evdm.register(eventdemux.MOUSEMOTION, self, gui_root.mouseevent)
		evdm.register(eventdemux.MOUSEBUTTONUP, self, gui_root.mouseevent)
		evdm.register(eventdemux.MOUSEBUTTONDOWN, self, gui_root.mouseevent)
	def draw(self, target):
		if not self.visible:
			return
		for element in self.elements:
			element.draw(target)

	def mouseevent(self, ev):
		for element in self.elements:
			element.mouseevent(ev)

	def __del__(self):
		self.__unregisterme__ = True

	def setbgcolor(self, color):
		pass

	def findelementbyid(self, name):
		for elem in self.elements:
			if elem.id == name:
				return elem
			for subelem in elem.elements:
				if subelem.id == name:
					return subelem
		return None



class gui_window(gui):
	parent = None
	root = None
	title = ""
	titlesurf = None
	bgcolor = (64, 64, 64)
	barbgcolor = (48, 48, 48)

	def __init__(self, parent, title, position, size, subelems):
		super().__init__()
		self.parent = parent
		self.title = title
		self.position = position
		self.size = size
		self.titlesurf = self.parent.font.render(self.title, False, (212, 212, 212))
		print("window: title: %s pos: %s size: %s" % (title, position, size))
		self.elements = []
		for elem in subelems:
			e = None
			if elem["__classname__"] == "label":
				e = gui_label(self, elem["text"], elem["position"])
			elif elem["__classname__"] == "button":
				e = gui_button(self, elem["text"], elem["position"], elem["size"], elem["onclick"])
			elif elem["__classname__"] == "image":
				e = gui_image(self, elem["path"], elem["position"])
			else:
				continue

			for prop in elem:
				if not prop.startswith("__") and not prop in ["visible", "bgcolor", "onclick"]:
					setattr(e, prop, elem[prop])
			if "visible" in elem:
				e.visible = elem["visible"].lower() in ["true", "1", "yes"]
			if "bgcolor" in elem:
				e.setbgcolor(elem["bgcolor"])

			self.elements.append(e)

	def setbgcolor(self, color):
		if len(color) not in [3, 4]:
			return
		self.bgcolor = color
		self.barbgcolor = [(val - 16) for val in color]

	def draw(self, target):
		if not self.visible:
			return
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
				#print("mouseevent %s hit element %s at %s" % (ev, element, ev.pos))
				element.mouseevent(ev)

	def close(self):
		self.elements = []

class gui_label(gui):
	surf = None
	font = None
	font_size = 16
	def __init__(self, parent, text, position, color = (255, 255, 255)):
		super().__init__()
		self.parent = parent
		self.text = text
		self.position = position
		self.color = color
		self.gensurf()
		print("\tlabel: text: %s pos: %s color: %s" % (self.text, self.position, self.color))

	def draw(self, target):
		if isinstance(self.font, str):
			self.gensurf()
		if not self.visible:
			return
		target.drawsurfgui(self.surf, self.parent.position[0] + self.position[0], self.parent.position[1] + self.position[1])

	def gensurf(self):
		if not self.font:
			self.surf = self.parent.parent.font.render(self.text, False, self.color)
		else:
			if isinstance(self.font, str):
				e = engine.engine.getengine()
				e.resources.precache(e.resources.FONT, self.font, int(self.font_size))
				self.font = e.resources.load(e.resources.FONT, self.font)
				print("custom font!")
			self.surf = self.font.render(self.text, False, self.color)

class gui_button(gui):
	surf = None
	surf_clicked = None

	clicked = False
	onclick = None

	def __init__(self, parent, text, position, size, onclick, color = (212, 212, 212)):
		super().__init__()
		self.parent = parent
		self.text = text
		self.position = position
		self.size = size
		self.setbgcolor(color)
		if onclick == "null":
			self.onclick = None
		else:
			if onclick in gui_action:
				self.onclick = gui_action[onclick]
			else:
				print("button(%s): GUI action '%s' not found. the button will do nothing." % (str(self) if not hasattr(self, 'id') else self.id, onclick))

		self.gensurfs()

		print("\tbutton: text: %s pos: %s color: %s action: %s" % (self.text, self.position, self.bgcolor, onclick))
	def setbgcolor(self, color):
		if len(color) not in [3, 4]:
			return
		self.bgcolor = color
		self.bgcolor_clicked = [(val - 16) for val in color]
		self.gensurfs()

	def gensurfs(self):
		e = engine.engine.getengine()

		textpos = [0, 0]
		textsize = self.parent.parent.font.size(self.text)
		textpos[0] = (self.size[0] - textsize[0]) / 2
		textpos[1] = (self.size[1] - textsize[1]) / 2

		self.surf = e.renderer.getsurf(*self.size)
		self.surf.fill(self.bgcolor)
		self.surf.blit(self.parent.parent.font.render(self.text, False, (255, 255, 255)), textpos)

		self.surf_clicked = e.renderer.getsurf(*self.size)
		self.surf_clicked.fill(self.bgcolor_clicked)
		self.surf_clicked.blit(self.parent.parent.font.render(self.text, False, (255, 255, 255)), textpos)

	def mouseevent(self, ev):
		if ev.type == eventdemux.MOUSEBUTTONUP:
			if ev.button == 1:
				if self.onclick:
					self.onclick(self)

	def draw(self, target):
		if not self.visible:
			return
		if self.clicked:
			target.drawsurfgui(self.surf_clicked, self.parent.position[0] + self.position[0], self.parent.position[1] + self.position[1])
		else:
			target.drawsurfgui(self.surf, self.parent.position[0] + self.position[0], self.parent.position[1] + self.position[1])

class gui_image(gui):
	surf = None

	def __init__(self, parent, path, position):
		super().__init__()
		e = engine.engine.getengine()
		e.resources.precache(e.resources.IMAGE, path)
		self.parent = parent
		self.position = position
		self.surf = e.resources.load(e.resources.IMAGE, path)
		self.size = [self.surf.get_width(), self.surf.get_height()]

	def mouseevent(self, ev):
		pass

	def draw(self, target):
		if not self.visible:
			return
		target.drawsurfgui(self.surf, self.parent.position[0] + self.position[0], self.parent.position[1] + self.position[1])

# define your gui actions right down here fam

def mainmenu_start(self):
	e = engine.engine.getengine()
	e.gamemgr.switchstate(e.gamemgr.STATE_GAME)

def buypart(self):
	e = engine.engine.getengine()
	e.gamemgr.buypart(self.part)

gui_action = {
	"mainmenu_start" : mainmenu_start,
	"buypart" : buypart,
}