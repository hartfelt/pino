PINO - Simple media center interface
====================================

Requirements
------------
Python 3.2 (or newer)

Python modules:
- pygame (a version that works with python3. I've only had success building
  it from source)
- pexpect-u (available on pypi)

An program that'll play your movies. Currently supported:
- omxplayer if you're running pino on a raspberry pi
- mplayer (preferrably mplayer2) if you're running on anything else

Installation
------------
Until I figure out how to distribute images in python packages, don't...

Usage
-----
Start pino with './pino' (for now...)

The following keys work in the menu:
- Up/Down: navigate the menu.
- Left: Up a dir.
- Right/Enter: Select dir or play file.
- Escape: Quit pino.

The following keys work when playing files:
- Space: Toggle pause.
- Q/Escape: Stop playback, return to menu.
- Left/Right: Seek 30sec back/forward.
- Up/Down: Seek 10min back/forward.

Note that if you use the mplayer driver, the mplayer window will likely take
focus and intercept the key stokes. (But fear not, the keybindings are the
same, except for shorter seeks)

Configuration
-------------
Copy the supplied pinorc to ~/.pinorc, and modify to fit your needs.
The `[paths]` section defines the root menu in pino. Define as many directories
as you want. The format is `key = value`, one on each line. The key is displayed
in the menu, the value is the absolute path to a directory.
