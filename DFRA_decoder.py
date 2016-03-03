from DFRA_Methods import DFRA_Functions
import threading
from time import *

class DFRA(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		_DFRA =DFRA_Functions()
		while True:
			sleep(1)
			_DFRA.process_data()
