import multiprocessing

class coap_queue (object):
        cp_queue = None
        _lock = None

        def __init__ (self):
                global cp_queue
                global _lock
                cp_queue = multiprocessing.Queue() 
                _lock = multiprocessing.Lock()

        def put (self, data):
                '''host_queue.put(data, block=True, timeout=None)'''
                cp_queue.put(data)

        def get (self):
                if self.is_empty() is True:
                        print ("Empty!!!")
                        return False
                else:
                        print ("Read DATA from COAP Queue = ")
                        return cp_queue.get()

        def get_nowait (self):
                return cp_queue.get_nowait()

        def get_lock (self):
                _lock.acquire()
        
        def release_lock (self):
                _lock.release()

        def close_queue (self):
                cp_queue.close()

        def is_empty (self):
                if cp_queue.empty():
                        return True
                else:
                        return False
