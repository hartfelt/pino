#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: real options
options = {
	'paths': [
		(u'/home/bjuhn/lain', u'Lain'),
		(u'/home/bjuhn/incoming', u'Incoming'),
	],
	'player': ['/usr/bin/mplayer', '-fs'],
	'uiscale': 1.0,
}

import math
import os, os.path
import subprocess
from libavg import avg, AVGApp, ui

# Singleton player-object for easy reference.
player = avg.Player.get()

# Actual screen size
width, height = map(lambda x:int(x*options['uiscale']), player.getScreenResolution())

scale = min(width/1920.0, height/1080.0)
aw, ah = 1920*scale, 1080*scale
dx, dy = (width-aw)/2, (height-ah)/2

player.setWindowPos(0, 0)
player.setResolution(True, width, height, 32)
player.setWindowFrame(False)
font = 'Bitstream Vera Sans'

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
			pos=(0, 0), size=(width,height), href='media/bg.png')
		avg.WordsNode(parent=self._parentNode,
			pos=XY(20, 20), text=u'Pino', fontsize=F(1), font=font)
		
		avg.RectNode(parent=self._parentNode,
			pos=XY(20, 60), size=WH(1200, 1000), fillcolor='000000',
			fillopacity=.6, strokewidth=0)
		self.listing = avg.DivNode(parent=self._parentNode,
			pos=XY(20, 60), size=WH(1200, 1000), crop=True)
		self.scrollbar = avg.RectNode(parent=self._parentNode,
			pos=XY(1225, 60), size=WH(10, 1000), fillcolor='ffffff',
			fillopacity=0, strokewidth=0)
		
		self.key_map = {
			13: self.select,
			273: self.up,
			274: self.down,
			275: self.select, # right
			276: self.back, # back
		}
		self.notifies = []
		
		self.ROOT = [('d', path, label) for path, label in options['paths']]
			#('d', 'new', u'Newly added files'),
			#('a', 'update', u'Update database'),
		
		self.dir_path = []
		self.dir_listing = self.ROOT
		self.dir_scroll = 0
		self.dir_selected = 0
		#self.dir_selected_action = lambda: None
		
		self.draw_dir()
	
	def notify(self, message, duration=4000, color='000000'):
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
			pos=(0,0), size=(words_width, H(50)), fillcolor=color,
			fillopacity=.6, strokewidth=0)
		box.appendChild(words)
		words.pos = WH(20,5)
		
		avg.LinearAnim(box, 'opacity', 300, 0, 1).start()
		stop = (lambda: (self._parentNode.removeChild(box), self.notifies.remove(y)))
		player.setTimeout(duration, avg.LinearAnim(
			box, 'opacity', 300, 1.0, 0.0
		).start)
		player.setTimeout(duration+300, stop)
	
	def change_dir(self, to):
		if to == '..':
			if self.dir_path:
				_, sel, scr = self.dir_path.pop()
				self.dir_selected = sel
				self.dir_scroll = scr
				if self.dir_path == []:
					self.dir_listing = self.ROOT
		else:
			self.dir_path.append((to, self.dir_selected, self.dir_scroll))
			self.dir_selected = 0
			self.dir_scroll = 0
		
		# OK, we have changed somewhere... find out what is here.
		if self.dir_path:
			cwd = self.dir_path[-1][0]
			self.dir_listing = []
			for item in sorted(os.listdir(cwd)):
				if item[0] == '.': continue # skip hidden files
				absitem = os.path.join(cwd, item)
				if os.path.isdir(absitem):
					self.dir_listing.append(('d', absitem, item))
				else:
					self.dir_listing.append(('f', absitem, item))
			if not self.dir_listing:
				self.dir_listing = [('d', '..', '(empty)')]
		
		self.draw_dir()
	
	def draw_dir(self):
		while self.listing.getNumChildren():
			self.listing.removeChild(0)
		
		these = self.dir_listing[self.dir_scroll:self.dir_scroll + 20]
		for index, (type, target, text) in enumerate(these):
			selected = (index+self.dir_scroll == self.dir_selected)
			y = index*50
			if type == 'd':
				self.draw_item('dir', text, selected, y)
			elif type == 'f':
				self.draw_item(' ', text, selected, y)
			else:
				self.notify('Unknown type: ' + type, color='AA0000')
		# Do we need a scroll-bar?
		dir_len = len(self.dir_listing)
		if dir_len > 20:
			# We do..
			pages = math.ceil(dir_len/20.0)
			top = (self.dir_selected/float(dir_len-1))
			self.scrollbar.pos = (self.scrollbar.pos[0], Y(60 + (1000-(1000/pages))*top))
			self.scrollbar.size = (self.scrollbar.size[0], H(1000/pages))
			self.scrollbar.fillopacity = .8
		else:
			# we don't
			self.scrollbar.fillopacity = 0
	
	def draw_item(self, icon, text, selected, y):
		box = avg.DivNode(pos=(X(0), Y(y)), size=WH(1200, 50), opacity=1)
		if selected:
			avg.RectNode(parent=box,
				pos=WH(0,0), size=WH(1200,50), fillcolor='000000',
				fillopacity=.3, strokewidth=0)
		avg.WordsNode(parent=box,
			pos=WH(15,9), size=WH(38,40), text=icon, fontsize=F(1), font=font,
			color=('aaaaaa' if selected else '888888'))
		
		words = avg.WordsNode(
			text=text, fontsize=F(1), font=font,
			color=('ffffff' if selected else 'aaaaaa'), rawtextmode=True)
		while words.getMediaSize()[0] > W(1120):
			text = text[:-1]
			words.text = text + '...'
		words.pos = WH(70,9)
		box.appendChild(words)
		self.listing.appendChild(box)
	
	def play(self, item):
		subprocess.call(options['player'] + [item])
	
	def onKeyDown(self, event):
		c = event.keycode
		if c in self.key_map.keys():
			self.key_map[c](event)
			return True
		
		self.notify('Unhandled key: {}'.format(c), duration=1000)
		return False
	
	def up(self, event):
		self.dir_selected = (self.dir_selected - 1) % len(self.dir_listing)
		self.dir_scroll = (self.dir_selected / 20) * 20
		self.draw_dir()
	
	def down(self, event):
		self.dir_selected = (self.dir_selected + 1) % len(self.dir_listing)
		self.dir_scroll = (self.dir_selected / 20) * 20
		self.draw_dir()
	
	def back(self, event):
		self.change_dir('..')
	
	def select(self, event):
		# Find out what is selected
		type, path, _ = self.dir_listing[self.dir_selected]
		if type == 'd':
			self.change_dir(path)
		elif type == 'f':
			self.play(path)
	
Pino.start(resolution=(width, height))
