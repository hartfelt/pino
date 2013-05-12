from utils import settings

_watched = []
try:
	with open(settings.database, 'r') as file:
		_watched = [l.strip('\n') for l in file.readlines()]
except IOError:
	pass

def watch_file(item):
	global _watched
	if not item in _watched:
		_watched.append(item)
		with open(settings.database, 'a') as file:
			file.write(item)
			file.write('\n')

def is_watched(item):
	return item in _watched
