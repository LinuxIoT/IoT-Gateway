import serial
import os
import logging
import logging.handlers
from sysconfigx import *
from serial_config import *

class serial_get():
        max_len=0
        min_len=0
        
	def __init__(self,ser):
		self.parse = Parser_Functions()
		self.parse.parser_init()
		self.parse.ConfigSectionMap()
		self.ser = ser

	def serial_write(self, _cmd):
		self.ser.write(_cmd)
		print "wrote: " + _cmd

	def serial_readline(self):
                
		_port_data = None
		_port_data = self.ser.readline().strip()
		if _port_data is None:
			return False
		elif _port_data is "":
			return False
		else:
			#_logger.debug(_port_data)
                        print _port_data
			return _port_data
				

	def get_serial_conf(self):
		print self.ser.getSettingsDict()

	def flush_buffer(self):
		self.ser.flush()


if __name__ == '__main__':
        get = serial_get()

