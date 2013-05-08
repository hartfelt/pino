from distutils.core import setup

setup(
	name='pino',
	version='0.0.1',
	description='Simple media center interface for the Raspberry Pi',
	author='Bjørn Hartfelt',
	author_email='b.hartfelt@gmail.com',
	url='http://hartfelt.de/pino',
	packages=['drivers', 'utils'],
	scripts=['pino.py'],
	data_files=[
		('/etc', ['pinorc']),
		('media', ['media/bg.png', 'media/sans.ttf']),
	],
)