import multiprocessing

class outbound_FILTER_queue_low_latency (object):
   	ser_filter_queue = None
	_lock = None

	def __init__ (self):
        	global ser_filter_queue
		global _lock
        	ser_filter_queue = multiprocessing.Queue() 
		_lock = multiprocessing.Lock()

	def put (self, data):
		'''host_queue.put(data, block=True, timeout=None)'''
		ser_filter_queue.put(data)

	def get (self):
		if self.is_empty() is True:
			return False
		else:
			return ser_filter_queue.get()

	def get_nowait (self):
		return ser_filter_queue.get_nowait()

	def get_lock (self):
		_lock.acquire()
	
	def release_lock (self):
		_lock.release()

	def close_queue (self):
		ser_filter_queue.close()

	def is_empty (self):
		if ser_filter_queue.empty():
			return True
		else:
			return False

