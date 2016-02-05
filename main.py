#!/usr/bin/python

__author__ = "Weqaar Janjua"
__copyright__ = "Copyright (C) 2016 Linux IoT"
__revision__ = "$Id$"
__version__ = "5.7"

import signal
import threading
import os
import sys
from time import *
import psutil
import subprocess
import gc
# Proprietary Code
from FILTER_queue_singleton_low_latency import *
from FILTER_queue_singleton_high_latency import *
from CFAR_queue_singleton import *
from CFAR import *
from serial_FILTER import *
from sysconfigx import *
from ZMQ import *
from IoTGatewayHttpServer import *


#Please modify the directory path (_firmware_dir) for the variable below: 
#_firmware_dir = '/opt/IoT-Gateway'
_firmware_dir = '.'
_thread_pool = []


class sysinit():
	def __init__(self):
		global sys_obj
		pass

	def run(self):
		sys_obj = Parser_Functions()
		sys_obj.parser_init()
		sys_obj.conf_map = sys_obj.ConfigSectionMap()
		self.verify_os_linux()
		self.verify_run_as_root()
		self.set_working_dir()
		self.set_process_priority_RT()

	def verify_os_linux(self):
		if "linux" in sys.platform:
			pass
		else:
			print "Firmware must run on Linux OS, other OS i.e. Windows are not supported, exiting!\n"
			exit (0)
		 
	def verify_run_as_root(self):
		if os.geteuid() != 0:
			print "Process must run as user root, exiting!\n"
			exit (0)
		 

	def set_working_dir(self):
		try:
			print "Switching to working directory: " + _firmware_dir + "\n"
			os.chdir(_firmware_dir)
		except OSError:
			print "ERROR Switching to working directory: " + _firmware_dir + " Exiting.\n"
			exit(0)

	def set_process_priority_RT(self):
		_pid = os.getpid()
		print "Process ID: " + str(_pid) + "\n"
		_process = psutil.Process(_pid)
		print "Current Process Priority: " + str(_process.nice()) + "\n"
		_process.nice(-20)
		print "New Process Priority: " + str(_process.nice()) + "\n"
		print "RT PRIO for " + subprocess.check_output(['chrt', '-p', str(_pid)]) + "\n"
		subprocess.call(['chrt', '-f', '-p', '99', str(_pid)])
		print "New RT PRIO for " + subprocess.check_output(['chrt', '-p', str(_pid)]) + "\n"


class serial_IO_FILTER(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		global _serial_FILTER

	def run(self):
		_serial_FILTER = Serial_Functions_FILTER()
		_serial_FILTER.serial_init_FILTER()
		_serial_FILTER.flush_buffer()
        	while True:
            		sleep(0.01)
			_ser_data = _serial_FILTER.serial_readline()
			if _ser_data is False:
				pass
			elif _ser_data == "NULL":
				pass
			else:
				CFAR_queue.get_lock()
				CFAR_queue.put(_ser_data)
				print str(_ser_data)
				CFAR_queue.release_lock()
				_serial_FILTER.flush_buffer()


class CFAR_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		_CFAR = CFAR_Functions()
		while True:
			sleep(0.01)
			_CFAR.process_data()


class ZMQ_Low_Latency_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		_ZMQ = ZMQ_Functions()
		_ZMQ.init_socket_low_latency()
		while True:
			sleep(0.01)
			_ZMQ.process_data_low_latency()


class ZMQ_High_Latency_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		_ZMQ = ZMQ_Functions()
		_ZMQ.init_socket_high_latency()
		while True:
			sleep(0.01)
			_ZMQ.process_data_high_latency()


class IoT_Gateway_Http_Server_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		_HTTP_SERVER = IoT_Gateway_http_server()
		_HTTP_SERVER.start_server()


def main():
	_print_header()

	sysinit_obj = sysinit()
	sysinit_obj.run()

	_config_parse = Parser_Functions()
     	_config_parse.parser_init()
     	_config_parse.ConfigSectionMap()
	'''example:
        _section = 'FIRMWARE'
        _firmware_dir = _config_parse.getSectionOption(_section, 'firmware_directory')
	'''
	print "Garbage Collector Enabled: " + str(gc.isenabled()) + "\n"

    	# Initialize local queues
	global FILTER_queue_low_latency
	FILTER_queue_low_latency = outbound_FILTER_queue_low_latency()
	
	global FILTER_queue_high_latency
	FILTER_queue_high_latency = outbound_FILTER_queue_high_latency()
	
	global CFAR_queue
	CFAR_queue = outbound_CFAR_queue()

    	# Spawn Threads
	t0 = serial_IO_FILTER()
	t0.start()
	_thread_pool.append(t0)

	t1 = CFAR_Thread()
	t1.start()
	_thread_pool.append(t1)

	t2 = ZMQ_Low_Latency_Thread()
	t2.start()
	_thread_pool.append(t2)

	t3 = ZMQ_High_Latency_Thread()
	t3.start()
	_thread_pool.append(t3)

	t4 = IoT_Gateway_Http_Server_Thread()
	t4.start()
	_thread_pool.append(t4)


def _print_header():
	_marker = '-------------------------------------------'
        _n = '\n'
	print _n + _marker
	print "Process name:" + __file__ + _n
	print "Author: " + __author__ + _n 
	print "Copyright: " + __copyright__ + _n
	print "Version: " + __version__ + _n
	print _marker + _n
	return 

if __name__ == '__main__':
	main()

