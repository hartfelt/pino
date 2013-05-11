from drivers import BasePlayer
from utils import settings

import pexpect
from threading import Thread
import time

class Player(BasePlayer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._process = pexpect.spawn('/usr/bin/mplayer', [
			'-fs',
			'-msglevel', 'all=0:STATUSLINE=5',
			self.file
		])
		self.state = 'playing'
		self.toggle_pause()
		self.position = 0.0
		
		self._position_thread = Thread(target=self._get_position)
		self._position_thread.start()
		time.sleep(settings.preplay_delay)
	
	def _get_position(self):
		while True:
			i = self._process.expect([
				'A: *(\d+\.\d) ',
				pexpect.EOF,
				pexpect.TIMEOUT
			])
			if i == 0:
				self.position = float(self._process.match.groups()[0])
			if i == 1:
				self.state = 'stopped'
				self.done_callback()
				break
			# Ignore timeouts
	
	def toggle_pause(self):
		self._process.send('p')
		if self.state == 'playing':
			self.state = 'paused'
		elif self.state == 'paused':
			self.state = 'playing'
		# What this does when the movie is not playing is... undefined
	
	def play(self):
		if self.state == 'paused':
			self.toggle_pause()
		#self.done_callback()
	
	def stop(self):
		self._process.send('q')
		self._process.expect(pexpect.EOF)
	
	def seek(self, offset):
		offset = int(round(offset / 10))
		while offset >= 6:
			self._process.send('\x1b[A') # up
			offset -= 6
		while offset >= 1:
			self._process.send('\x1b[C') # right
			offset -= 1
		while offset <= -6:
			self._process.send('\x1b[B') # down
			offset += 6
		while offset <= -1:
			self._process.send('\x1b[D') # left
			offset += 1
