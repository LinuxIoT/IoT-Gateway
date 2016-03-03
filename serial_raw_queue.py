import multiprocessing

class serial_queue (object):
   	ser_queue = None
	_lock = None

	def __init__ (self):
        	global ser_queue
		global _lock
        	ser_queue = multiprocessing.Queue() 
		_lock = multiprocessing.Lock()

	def put (self, data):
		'''host_queue.put(data, block=True, timeout=None)'''
		ser_queue.put(data)

	def get (self):
		if self.is_empty() is True:
                        print "Empty!!!"
			return False
		else:
                        print "Read DATA from Serial Queue = "
			return ser_queue.get()

	def get_nowait (self):
		return ser_queue.get_nowait()

	def get_lock (self):
		_lock.acquire()
	
	def release_lock (self):
		_lock.release()

	def close_queue (self):
		ser_queue.close()

	def is_empty (self):
		if ser_queue.empty():
			return True
		else:
			return False
