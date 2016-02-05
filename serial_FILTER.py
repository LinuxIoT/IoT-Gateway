import serial
import os
import logging
import logging.handlers
from sysconfigx import *

class Serial_Functions_FILTER():

	def __init__(self):
		self.parse = Parser_Functions()
		self.parse.parser_init()
		self.parse.ConfigSectionMap()

	def serial_init_FILTER(self):
		_section = 'SERIAL'
		_device = self.parse.getSectionOption(_section, 'device')
		_baudrate = int(self.parse.getSectionOption(_section, 'baudrate'))
		_parity = self.parse.getSectionOption(_section, 'parity')
		_stopbits = int(self.parse.getSectionOption(_section, 'stopbits'))
		_bytesize = int(self.parse.getSectionOption(_section, 'bytesize'))
		_timeout = float(self.parse.getSectionOption(_section, 'timeout'))
		_inter_byte_delay = float(self.parse.getSectionOption(_section, 'inter_byte_delay'))
		try:
			self.ser = serial.Serial (port = _device, baudrate = _baudrate, timeout = _timeout, \
			   			  interCharTimeout = _inter_byte_delay, parity = _parity, \
						  stopbits = _stopbits, bytesize = _bytesize)
		except serial.SerialException:
			print "Serial Port Exception: " + _device + "\n"
            		return False
		self.ser.flush()
		#Initialize Logger
		_section = 'SYSLOG'
		_syslog_dir = self.parse.getSectionOption(_section, 'syslogdir')
		_syslog_file_serial = self.parse.getSectionOption(_section, 'syslogfileserial')
		_log_level = int(self.parse.getSectionOption(_section, 'loglevel'))
		_log_title = self.parse.getSectionOption(_section, 'logtitle')
		try:
    			os.stat(_syslog_dir)
		except:
    			os.mkdir(_syslog_dir)
		try:
    			os.remove(_syslog_dir + "/" + _syslog_file_serial)
		except OSError:
    			pass
		global _logger
		_logger = logging.getLogger(_log_title)
		_logger.setLevel(_log_level)
		_log_file = logging.FileHandler(_syslog_dir + "/" + _syslog_file_serial)
		_log_file.setLevel(_log_level)
		_log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - ' + self.__class__.__name__ + " : " + '%(message)s')
		_log_file.setFormatter(_log_formatter)
		_logger.addHandler(_log_file)
		#Initialize FRAME
		_section = 'FRAME'
		global _frame_netid_len
		global _frame_devid_len
		global _frame_devtype_len
		global _frame_macid_len
		global _frame_tom_len
		global _frame_prio_len
		global _frame_seqnum_len
		global _frame_pdu_len
		global _frame_fields_num
		global _frame_min_len
		global _frame_max_len
		_frame_netid_len = int(self.parse.getSectionOption(_section, 'netid'))
		_frame_devid_len = int(self.parse.getSectionOption(_section, 'devid'))
		_frame_devtype_len = int(self.parse.getSectionOption(_section, 'devtype'))
		_frame_macid_len = int(self.parse.getSectionOption(_section, 'macid'))
		_frame_tom_len = int(self.parse.getSectionOption(_section, 'tom'))
		_frame_prio_len = int(self.parse.getSectionOption(_section, 'prio'))
		_frame_seqnum_len = int(self.parse.getSectionOption(_section, 'seqnum'))
		_frame_pdu_len = int(self.parse.getSectionOption(_section, 'pdu'))
		_frame_fields_num = int(self.parse.getSectionOption(_section, 'framefields'))
		_frame_min_len = _frame_netid_len + _frame_devid_len + _frame_devtype_len + \
				 _frame_tom_len + _frame_prio_len + _frame_seqnum_len
		_frame_max_len = _frame_min_len + _frame_pdu_len

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
			_logger.debug(_port_data)
			_validation_status, _reconstructed_frame = self.validate_frame(_port_data)
			if _validation_status is True:
				print "Frame is Valid!\n"
				return _reconstructed_frame
			else:
				print "ERROR -> Frame is InValid!\n"
				return False

	def validate_frame(self, _frame):
		global _mac_id
		_reconstructed_frame = "NULL"
		if _frame is None:
			return [False, _reconstructed_frame]
		elif _frame is "":
			return [False, _reconstructed_frame]
		elif _frame.startswith('OK'):
			return [False, _reconstructed_frame]
		elif len(_frame) < _frame_min_len:
			print "len(_frame) < _frame_min_len\n"
			return [False, _reconstructed_frame]
		elif len(_frame) > _frame_max_len:
			print "len(_frame) > _frame_max_len\n"
			return [False, _reconstructed_frame]
		elif _frame.startswith("+DATA:") and ("BYTES" in _frame):
			print "_frame.startswith(+DATA:)\n"
			try:
				_mac_id=_frame.split(" ")[4]
				print "MAC: " + _mac_id + "\n"
			except IndexError:
				print "Invalid Frame, Unable to parse MAC: List index out of range" + "\n"
				return [False, _reconstructed_frame]
			return [True, _reconstructed_frame]
		#elif _mac_id is None:
		#	print "MAC ID: is NULL\n"
		#	return [False, _reconstructed_frame]
		else:	
			print "FRAME: " + str(_frame) + "\n"
			_expanded_frame=['NETID', 'DEVID', 'DEVTYPE', 'MACID', 'TOM', \
					 'PRIO', 'SEQNUM', 'PDU']
			try:	
				_expanded_frame[0] = _frame[1:3]
				_expanded_frame[1] = _frame[3:5]
				_expanded_frame[2] = _frame[5]
			except IndexError:
                        	print "error parsing, index out of range!\n"
				return [False, _reconstructed_frame]
			try:
				_mac_id
			except NameError:
				return [False, _reconstructed_frame]
			try:
				_expanded_frame[3] = str(_mac_id)
				_expanded_frame[4] = _frame[6]
				_expanded_frame[5] = _frame[7]
				_expanded_frame[6] = _frame[8:10]
				_expanded_frame[7] = _frame[10:]
			except IndexError:
				print "Invalid Frame, Unable to parse MAC: List index out of range" + "\n"
				return [False, _reconstructed_frame]
			if len(_expanded_frame) < _frame_fields_num:
				return [False, _reconstructed_frame]
			elif len(_expanded_frame) > _frame_fields_num:
				return [False, _reconstructed_frame]
			#Verify NETID Field Width
			elif len(_expanded_frame[0]) > _frame_netid_len:
				return [False, _reconstructed_frame]
			elif len(_expanded_frame[0]) < _frame_netid_len:
				return [False, _reconstructed_frame]
			#Verify DEVID Field Width
			elif len(_expanded_frame[1]) > _frame_devid_len:
				return [False, _reconstructed_frame]
			elif len(_expanded_frame[1]) < _frame_devid_len:
				return [False, _reconstructed_frame]
			#Verify DEVTYPE Field Width
			elif len(_expanded_frame[2]) > _frame_devtype_len:
				return [False, _reconstructed_frame]
			elif len(_expanded_frame[2]) < _frame_devtype_len:
				return [False, _reconstructed_frame]
			#Verify MACID Field Width
			elif len(_expanded_frame[3]) > _frame_macid_len:
				return [False, _reconstructed_frame]
			elif len(_expanded_frame[3]) < _frame_macid_len:
				return [False, _reconstructed_frame]
			#Verify TOM Field Width
			elif len(_expanded_frame[4]) > _frame_tom_len:
				return [False, _reconstructed_frame]
			elif len(_expanded_frame[4]) < _frame_tom_len:
				return [False, _reconstructed_frame]
			#Verify PRIO Field Width
			elif len(_expanded_frame[5]) > _frame_prio_len:
				return [False, _reconstructed_frame]
			elif len(_expanded_frame[5]) < _frame_prio_len:
				return [False, _reconstructed_frame]
			#Verify SEQNUM Field Width
			elif len(_expanded_frame[6]) > _frame_seqnum_len:
				return [False, _reconstructed_frame]
			elif len(_expanded_frame[6]) < _frame_seqnum_len:
				return [False, _reconstructed_frame]
			#Verify PDU Field Width
			elif len(_expanded_frame[7]) > _frame_pdu_len:
				return [False, _reconstructed_frame]
			else:		
				_reconstructed_frame = {'NETID'		: _expanded_frame[0], \
							'DEVID'		: _expanded_frame[1], \
							'DEVTYPE'	: _expanded_frame[2], \
							'MACID'		: _expanded_frame[3], \
							'TOM'		: _expanded_frame[4], \
							'PRIO'		: _expanded_frame[5], \
							'SEQNUM'	: _expanded_frame[6], \
							'PDU'		: _expanded_frame[7]}
				print "Reconstructed FRAME is: " + str(_reconstructed_frame) + "\n"
				return [True, _reconstructed_frame]


	def get_serial_conf(self):
		print self.ser.getSettingsDict()

	def flush_buffer(self):
		self.ser.flush()

