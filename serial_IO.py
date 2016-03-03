from serial_frame import serial_get
from serial_raw_queue import serial_queue
import threading
from time import *


class serial_data(threading.Thread):
	def __init__(self,ser):
		threading.Thread.__init__(self)
		self.ser = ser
		global _serial_data

	def run(self):
                s = serial_get(self.ser)
                queue = serial_queue()
                
        	while True:
            		sleep(1)
			_ser_data = s.serial_readline()
			if _ser_data is False:
				pass
			elif _ser_data == "NULL":
				pass
			else:
				queue.get_lock()
				queue.put(_ser_data)
				print "Write RAW Data to Queue by Serial port = "
				print str(_ser_data)
				queue.release_lock()
				s.flush_buffer()
                        
                        
