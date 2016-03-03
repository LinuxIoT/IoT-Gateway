from ZMQ import *
import threading
from time import *


class ZMQ_HL(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		_ZMQ = ZMQ_Functions()
		_ZMQ.init_socket_high_latency()
		while True:
			sleep(1)
			print "IN ZMQ HIGH"
			_ZMQ.process_data_high_latency()
