import os
import sys
import psutil
import subprocess
from sysconfigx import *


class sysinit():
        _firmware_dir='/home/ahmer'
	def __init__(self):
                
		global sys_obj
		pass

	def run(self):
		sys_obj = Parser_Functions()
		sys_obj.parser_init()
		sys_obj.conf_map = sys_obj.ConfigSectionMap()
		sysinit._firmware_dir = sys_obj.getSectionOption("FIRMWARE","FIRMWARE_DIRECTORY")
		print sysinit._firmware_dir
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
			print "Switching to working directory: " + sysinit._firmware_dir + "\n"
			os.chdir(sysinit._firmware_dir)
		except OSError:
			print "ERROR Switching to working directory: " + sysinit._firmware_dir + " Exiting.\n"
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


if __name__ == '__main__':
	sysinit_obj = sysinit()
	sysinit_obj.run()



