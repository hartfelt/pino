import time
from threading import Timer

def setTimeout(delay, fun, *args, **kwargs):
	Timer(delay, lambda: fun(*args, **kwargs)).start()
