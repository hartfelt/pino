class Player(object):
	def __init__(self, file, done_callback):
		self.file = file
		self.done_callback = done_callback
	
	def play(self):
		print('playing', self.file)
		self.done_callback()
