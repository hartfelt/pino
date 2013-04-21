#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: options
option = {
	'paths': [
		'/home/bjuhn/lain',
	],
}

from libavg import avg, AVGApp, ui

# Singleton player-object for easy reference.
player = avg.Player.get()

# Actual screen size
width, height = map(lambda x:int(x/2), player.getScreenResolution())

scale = min(width/1920.0, height/1080.0)
aw, ah = 1920*scale, 1080*scale
dx, dy = (width-aw)/2, (height-ah)/2

player.setWindowPos(0, 0)
player.setResolution(True, width, height, 32)
player.setWindowFrame(False)
font='Nimbus Roman No9 L'

# Helpers to scale stuff to fit on the conceptual 1920×1080-screen
F = lambda s: s * 30 * scale
X = lambda x: x * scale + dx
Y = lambda y: y * scale + dy
W = H = lambda l: l * scale
def XY(x,y): return X(x), Y(y)
def WH(w,h): return W(w), H(h)

class Pino(AVGApp):
	def init(self):
		self.background = avg.ImageNode(parent=self._parentNode,
			pos=(0,0), size=(width,height), href='media/bg.png')
		
		avg.WordsNode(parent=self._parentNode,
			pos=XY(20,20), text=u'<i>Pino</i>', fontsize=F(1), font=font)
		
		self.key_map = {
			13: self.select,
			273: self.up,
			274: self.down,
			275: self.right,
			276: self.left,
		}
		self.notifies = []
	
	def notify(self, message, duration=4000):
		words = avg.WordsNode(
			text=message, fontsize=F(1), font=font, color='ffffff')
		words_width = words.getMediaSize()[0] + W(40)
		
		# Find suitable place for notification.
		y = 0
		while True:
			if not y in self.notifies:
				break
			y += 60
		self.notifies.append(y)
		
		box = avg.DivNode(parent=self._parentNode,
			pos=(X(1910)-words_width, Y(y)), size=WH(words_width, 50),
			opacity=0)
		avg.RectNode(parent=box,
			pos=(0,0), size=(words_width, H(50)), fillcolor='111111',
			fillopacity=.8, strokewidth=0)
		box.appendChild(words)
		words.pos = WH(20,5)
		
		avg.LinearAnim(box, 'opacity', 300, 0, 1).start()
		stop = (lambda: (self._parentNode.removeChild(box), self.notifies.remove(y)))
		player.setTimeout(duration, avg.LinearAnim(
			box, 'opacity', 300, 1.0, 0.0
		).start)
		player.setTimeout(duration+300, stop)
	
	def dir(self, path):
		pass
	
	def onKeyDown(self, event):
		c = event.keycode
		if c in self.key_map.keys():
			self.key_map[c](event)
			return True
		
		self.notify('Unhandled key: {}'.format(c), duration=1000)
		return False
	
	def up(self, event):
		self.notify(u'^')
	
	def down(self, event):
		self.notify(u'v')
	
	def left(self, event):
		self.notify(u'&lt;')
	
	def right(self, event):
		self.notify(u'>')
	
	def select(self, event):
		self.notify(u'¬')

Pino.start(resolution=(width, height))
