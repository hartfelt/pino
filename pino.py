#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os, os.path
import sys
import pygame
import utils.settings as settings

if settings.driver == 'mplayer':
	from drivers.mplayer import Player
elif settings.driver == 'omxplayer':
	from drivers.omxplayer import Player
else:
	raise ImportError

pygame.display.init()
pygame.font.init()
pygame.key.set_repeat(200, 100)

mods = pygame.DOUBLEBUF
if settings.fullscreen:
	mods = mods and pygame.FULLSCREEN
screen = pygame.display.set_mode((settings.width, settings.height), mods, 32)
width, height = screen.get_size()

scale = min(width/1920.0, height/1080.0)
aw, ah = 1920*scale, 1080*scale
dx, dy = (width-aw)/2, (height-ah)/2

font = pygame.font.Font('media/sans.ttf', int(round(30 * scale)))

COLOR = {
	'white': pygame.color.Color(255,255,255),
	'black': pygame.color.Color(0,0,0),
	'light': pygame.color.Color(200,200,200),
	'dark': pygame.color.Color(160,160,160),
}

# Helpers to scale stuff to fit on the conceptual 1920×1080-screen
X = lambda x: int(x * scale + dx)
Y = lambda y: int(y * scale + dy)
W = H = lambda l: int(l * scale)
def XY(x,y): return X(x), Y(y)
def WH(w,h): return W(w), H(h)

class Pino(object):
	def __init__(self):
		self.set_background('media/bg.png')
		self.menu_key_map = {
			pygame.K_RETURN: self.select,
			pygame.K_UP: self.up,
			pygame.K_DOWN: self.down,
			pygame.K_RIGHT: self.select, # right
			pygame.K_LEFT: self.back, # back
			pygame.K_ESCAPE: sys.exit
		}
		self.player_key_map = {
			pygame.K_ESCAPE: lambda: self.player.stop(),
			pygame.K_SPACE: lambda: self.player.toggle_pause(),
		}
		self.notifies = {}
		
		self.ROOT = [('d', path, label) for path, label in settings.paths]
			#('d', 'new', 'Newly added files'),
			#('a', 'update', 'Update database'),
		
		self.dir_path = []
		self.dir_listing = self.ROOT
		self.dir_scroll = 0
		self.dir_selected = 0
		self.player = None
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				elif event.type == pygame.KEYDOWN:
					c = event.key
					if self.player:
						if c in self.player_key_map.keys():
							player_key_map[c]()
					else:
						if c in self.menu_key_map.keys():
							self.menu_key_map[c]()
						else:
							self.notify('Unhandled key: {}'.format(c), duration=1000)
			
			# Draw the screen
			screen.blit(self.background, (0,0))
			self.draw_text('Pino', COLOR['white'], XY(20,20))
			self.draw_trans_rect(
				COLOR['black'], 128,
				XY(20, 60), WH(1200, 1000))
			self.draw_dir()
			self.draw_notifies()
			
			pygame.display.flip()
	
	def draw_trans_rect(self, color, alpha, pos, size):
		s = pygame.Surface(size)
		s.set_alpha(alpha)
		s.fill(color)
		screen.blit(s, pos)
	
	def draw_text(self, text, color, pos, max_length=None):
		if max_length and font.size(text)[0] > max_length:
			while font.size(text + '...')[0] > max_length:
				text = text[:-1]
			screen.blit(font.render(text + '...', True, color), pos)
		else:
			screen.blit(font.render(text, True, color), pos)
	
	def set_background(self, filename):
		self.background = pygame.transform.smoothscale(
			pygame.image.load(filename).convert(),
			(width,height))
		
	def notify(self, message, duration=4000, color=COLOR['black']):
		x = W(1920) - font.size(message)[0] - W(30)
		# Find suitable place for notification.
		y = 10
		while True:
			if not y in self.notifies.keys():
				break
			y += 60
		self.notifies[y] = (message, color, pygame.time.get_ticks()+duration, x)
	
	def draw_notifies(self):
		now = pygame.time.get_ticks()
		for y, (message, color, timeout, x) in self.notifies.items():
			if timeout < now:
				del self.notifies[y]
			else:
				self.draw_trans_rect(color, 128, (x, Y(y)), (W(1910)-x, H(50)))
				self.draw_text(message, COLOR['white'], (x+W(10), Y(y+5)))
	
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
		these = self.dir_listing[self.dir_scroll:][:20]
		for index, (type, target, text) in enumerate(these):
			selected = (index+self.dir_scroll == self.dir_selected)
			if type == 'd':
				self.draw_item('dir', text, selected, index)
			elif type == 'f':
				self.draw_item(' ', text, selected, index)
			else:
				self.notify('Unknown type: ' + type, color='AA0000')
		# Do we need a scroll-bar?
		dir_len = len(self.dir_listing)
		if dir_len > 20:
			# We do..
			pages = math.ceil(dir_len/20.0)
			top = (self.dir_selected/float(dir_len-1))
			self.draw_trans_rect(
				COLOR['white'], 200,
				XY(1225, 60 + (1000-(1000/pages))*top),
				WH(10, 1000/pages))
	
	def draw_item(self, icon, text, selected, y):
		if selected:
			self.draw_trans_rect(
				COLOR['black'], 80,
				(X(20), Y(y*50 + 60)),
				WH(1200, 50))
		self.draw_text(
			icon,
			COLOR[('light' if selected else 'dark')],
			(X(30), Y(y*50 + 69)))
		self.draw_text(
			text,
			COLOR[('white' if selected else 'light')],
			(X(80), Y(y*50 + 69)),
			W(1120))
	
	def play(self, item):
		self.player = Player(item, done_callback=self.play_done)
		self.player.play()
	
	def play_done(self):
		self.player = None
		self.notify('Playback of file is done')
	
	def up(self):
		self.dir_selected = (self.dir_selected - 1) % len(self.dir_listing)
		self.dir_scroll = (self.dir_selected // 20) * 20
		self.draw_dir()
	
	def down(self):
		self.dir_selected = (self.dir_selected + 1) % len(self.dir_listing)
		self.dir_scroll = (self.dir_selected // 20) * 20
		self.draw_dir()
	
	def back(self):
		self.change_dir('..')
	
	def select(self):
		# Find out what is selected
		type, path, _ = self.dir_listing[self.dir_selected]
		if type == 'd':
			self.change_dir(path)
		elif type == 'f':
			self.play(path)
	
Pino().run()
