class BasePlayer(object):
	def __init__(self, file, done_callback=(lambda: None)):
		self._file = file
		self._done_callback = done_callback
	
	def play(self):
		raise NotImplementedError
	
	def toggle_pause(self):
		raise NotImplementedError
	
	def stop(self):
		raise NotImplementedError
	
	def seek(self, offset):
		raise NotImplementedError
