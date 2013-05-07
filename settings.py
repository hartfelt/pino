#!/usr/bin/env python3

import configparser
import os

# Default values.
class _CaseSensitiveParser(configparser.SafeConfigParser):
	def optionxform(self, option):
		return str(option)
		
_config = _CaseSensitiveParser()
_config.read_dict({
	'paths': {},
	'pino': {
		'width': '1920',
		'height': '1080',
		'fullscreen': 'yes',
		'driver': 'mplayer',
	}
})

# Read conf files.
_config.read([
	'/etc/pinorc',
	os.path.expanduser('~/.pinorc')
])

# Export the values we care about
paths = [(d, l) for (l, d) in _config.items('paths')]
if not paths:
	paths = [('/', 'Please configure pino first')]
width = int(_config['pino']['width'])
height = int(_config['pino']['height'])
fullscreen = _config['pino'].getboolean('fullscreen')
driver = _config['pino']['driver']
