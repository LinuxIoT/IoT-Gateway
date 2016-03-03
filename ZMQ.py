import zmq
import time
import sys
import os
import random
import multiprocessing
import logging
import logging.handlers
from sysconfigx import *
from CC_queue_HL import *
from CC_queue_LL import *

class ZMQ_Functions():

	def __init__(self):
		global FILTER_queue_low_latency
		global FILTER_queue_high_latency
		FILTER_queue_low_latency = CC_OUT_LL()
		FILTER_queue_high_latency = CC_OUT_HL()

		global _data
		global _publisher_port_low_latency
		global _publisher_port_high_latency

		_data = None

		self.parse = Parser_Functions()
		self.parse.parser_init()
		self.parse.ConfigSectionMap()

		#global _context
		_section = 'ZMQ'
		_publisher_port_low_latency = int(self.parse.getSectionOption(_section, 'pport_low_latency'))
		_publisher_port_high_latency = int(self.parse.getSectionOption(_section, 'pport_high_latency'))
		#_context = zmq.Context()
	
		#Initialize Logger
		global _logger
		_section = 'SYSLOG'
		_syslog_dir = self.parse.getSectionOption(_section, 'syslogdir')
		_syslog_file = self.parse.getSectionOption(_section, 'syslogfile')
		_log_level = int(self.parse.getSectionOption(_section, 'loglevel'))
		_log_title = self.parse.getSectionOption(_section, 'logtitle')
		try:
    			os.stat(_syslog_dir)
		except:
    			os.mkdir(_syslog_dir)
		try:
    			os.remove(_syslog_dir + "/" + _syslog_file)
		except OSError:
    			pass
		_logger = logging.getLogger(_log_title)
		_logger.setLevel(_log_level)
		_log_file = logging.FileHandler(_syslog_dir + "/" + _syslog_file)
		_log_file.setLevel(_log_level)
		_log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - ' + self.__class__.__name__ + " : " + '%(message)s')
		_log_file.setFormatter(_log_formatter)
		_logger.addHandler(_log_file)

	#Low Latency (PUB/SUB)
	def init_socket_low_latency(self):
		global _zmq_socket_low_latency
		_context = zmq.Context()
		_zmq_socket_low_latency = _context.socket(zmq.PUB)
		_zmq_socket_low_latency.bind("tcp://*:%s" % _publisher_port_low_latency)
		
	def process_data_low_latency(self):
		if(FILTER_queue_low_latency.is_empty() is True):
                        print "LL EMPTY!!!"
			pass
		else: 
			FILTER_queue_low_latency.get_lock()
			_data_low_latency = FILTER_queue_low_latency.get()
			FILTER_queue_low_latency.release_lock()
			_zmq_socket_low_latency.send(_data_low_latency)
			_logger.debug(_data_low_latency)
			print 'ZMQ: Low Latency Data is: ' + str(_data_low_latency) + '\n'


	#High Latency (PUSH/PULL)
	def init_socket_high_latency(self):
		global _zmq_socket_high_latency
		_context = zmq.Context()
		_zmq_socket_high_latency = _context.socket(zmq.PUSH)
		_zmq_socket_high_latency.bind("tcp://*:%s" % _publisher_port_high_latency)

	def process_data_high_latency(self):
		#print "PPPPPPPPPPPPPPPP:" + str(FILTER_queue_high_latency.get())
		if(FILTER_queue_high_latency.is_empty() is True):
                        print "HL EMPTY!!!"
			#pass
		else: 	
			FILTER_queue_high_latency.get_lock()
			_data_high_latency = FILTER_queue_high_latency.get()
			FILTER_queue_high_latency.release_lock()
			_zmq_socket_high_latency.send(_data_high_latency)
			_logger.debug(_data_high_latency)
			print 'ZMQ: High Latency Data is: ' + str(_data_high_latency) + '\n'

#EOF
