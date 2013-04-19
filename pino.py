#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg, AVGApp

# Singleton player-object for easy reference.
player = avg.Player.get()

width, height = map(int, player.getScreenResolution())
player.setWindowPos(0, 0)
player.setResolution(True, width, height, 32)
player.setWindowFrame(False)

def fs(s):
	return min(width*9, height*16)*s/450

class Pino(AVGApp):
	def init(self):
		self.background = avg.ImageNode(
			pos=(0,0), size=(width, height), parent=self._parentNode,
			href='media/bg.png')
		avg.WordsNode(
			pos=(20,20), text=u'<i>Pino</i>', fontsize=fs(.8), parent=self._parentNode)
		self.test = avg.WordsNode(
			pos=(100,230), text=u'here', fontsize=fs(1), parent=self._parentNode)
		
		self.key_map = {
			273: self.up,
			274: self.down,
			275: self.right,
			276: self.left,
		}
	
	def onKeyDown(self, event):
		c = event.keycode
		if c in self.key_map.keys():
			self.key_map[c](event)
			return True
		
		print 'unhandled key', c
		return False
	
	def up(self, event):
		self.test.y -= 10
	
	def down(self, event):
		self.test.y += 10
	
	def left(self, event):
		self.test.x -= 10
	
	def right(self, event):
		self.test.x += 10

Pino.start(resolution=(width, height))
