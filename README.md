PINO - Simple media center interface for the Raspberry Pi
=========================================================

Configuration
-------------

Make a settings.py in the same directory as pino.py. The following exported values are used:

  paths = [('path', 'Label'), ...]
    A list of tuples describing the root-level of the menu.
    Defaults to current working directory.
    
    If your paths or labels contains non-ascii characters, you'll need to have
      # -*- coding: utf8 -*-
    at the top of your file.

  fullscreen = False
    Set this to False to disable fullscreen.
    Defaults to True.

  width, height = 1920, 1080
    Set these to your setups native screen resolution.
    Default to 1920, 1080.

The settings is a simple python script, so you can do whatever magic trickery you want ;)
