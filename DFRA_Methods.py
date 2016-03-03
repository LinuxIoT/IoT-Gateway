import multiprocessing
import json
from sysconfigx import *
from Dynamic_False_Reduction_Alarm_queue import *
from CC_queue_LL import *
from CC_queue_HL import *
from ringbuffer import *
import string
import time

class DFRA_Functions():

	def __init__(self):
		global LL_queue
		global HL_queue
		LL_queue = CC_OUT_LL()
		HL_queue = CC_OUT_HL()
	
		global DFRA_queue
		DFRA_queue = DFRA_out_queue()

		global alert_dict
		alert_dict = {'SRCID': 0.0}
	
		global sensor_dict
		sensor_dict = { 'NETID' : '', \
				'SRCID' : '', \
                                'DSTID' : '', \
                                'PHYTYPE' : '', \
 				'DEVTYPE' : '', \
				'TOM' : '', \
			        'PRIO' : '', \
				'SEQNUM' : '', \
                                'PDUL' : '', \
                                'PDUT' : '', \
                                'PDU' : '', \
				'ECC' : '' }

		global json_object
		json_object = None

		global _queue_pass
		_queue_pass = 0

		self.parse = Parser_Functions()
		self.parse.parser_init()
		self.parse.ConfigSectionMap()

		global _dfra_expiry
		_section = 'DFRA'
		_dfra_expiry = int(self.parse.getSectionOption(_section, 'dfra_expiration'))

		global _auth_key
		_section_auth = 'AUTH'
		_auth_key = str(self.parse.getSectionOption(_section_auth, 'auth_key'))

		global _ringbuf_size
		global _ringbuf_activation
		_section_filter = 'FILTER'
		_ringbuf_size = int(self.parse.getSectionOption(_section_filter, 'ringbuffer_size'))
		_ringbuf_activation = int(self.parse.getSectionOption(_section_filter, 'ringbuffer_activate'))

		global _ringbuff
		_ringbuff = RingBuffer(_ringbuf_size)


	def process_data(self):
		if(DFRA_queue.is_empty() is True):
			_queue_it = 0
		else:
			_data = DFRA_queue.get()
			if _ringbuf_activation == 1:
				if self.ringbuffer_verify(_data) is False:
					_queue_it = 0
					#pass
				else:
					_queue_it = self.create_sensor_data(_data)
			else:
				try:
					_queue_it = self.create_sensor_data(_data)
				except IndexError:
					print "Invalid Frame: " + str(_data) + "\n"
					_queue_it = 0
		if _queue_it == 1:
			_json = self.create_json()
			print "JSON Formated: " + _json + "\n"
			self.queue_out_data(_json)
		else:
			json_object = None


	def create_json(self):
		json_object = str(sensor_dict['NETID']) + ":" + str(sensor_dict['SRCID']) + ":" + \
		      	      str(sensor_dict['DEVTYPE']) + ":" + \
			      str(sensor_dict['TOM']) + ":" + str(sensor_dict['PDU'])
		return json_object


	def create_sensor_data(self, _data):
		sensor_dict['NETID'] = _data['NETID']
		sensor_dict['SRCID'] = _data['SRCID']
		sensor_dict['DSTID'] = _data['DSTID']
		sensor_dict['DEVTYPE'] = _data['DEVTYPE']
		sensor_dict['TOM'] = _data['TOM']
		sensor_dict['PRIO'] = _data['PRIO']
		sensor_dict['SEQNUM'] = _data['SEQNUM']
		sensor_dict['PDUL'] = _data['PDUL']
		sensor_dict['PDUT'] = _data['PDUT']
		sensor_dict['PDU'] = _data['PDU']
		sensor_dict['ECC'] = _data['ECC']
			
		# A = Alert
		if sensor_dict['TOM'] == 'A' or sensor_dict['TOM'] == 'a':
			_sensor_head_no = _data['PDU'].split(",")[0]   # -- To Check
			print "\nAlert Detected on device: " + sensor_dict['SRCID'] + "\n"

			#DFRA - START
			if sensor_dict['SRCID'] in alert_dict:
				_current_stamp = time.time()
				_elapsed = _current_stamp - float(alert_dict[sensor_dict['SRCID']])
				if _elapsed < _dfra_expiry:
					print "Elapsed < _dfra_expiry - is: " + str(_elapsed) + "\n"
					_queue_pass = 0
				else:
					alert_dict[sensor_dict['SRCID']] = _current_stamp 
					_queue_pass = 1
			else:
				_current_stamp = time.time()
				alert_dict[sensor_dict['SRCID']] = _current_stamp 
				_queue_pass = 1
			#DFRA - END

                # T = Time Synchronization
		elif sensor_dict['TOM'] == 'T' or sensor_dict['TOM'] == 't':
                        #print "Current time " + time.strftime("%X")
                        if len(_data['PDU']) != 8:
                                print "Time Sync ERROR!!! Time is INVALID!!!"
                                _queue_pass = 0
                        else:
                                time_str = _data['PDU'].split(':')
                                if int(time_str[0]) > 24:
                                       print "Hours are INVALID!!!"
                                       _queue_pass = 0
                                elif int(time_str[1]) > 60:
                                       print "Mins are INVALID!!!"
                                       _queue_pass = 0
                                elif int(time_str[2]) > 60:
                                       print "Secs are INVALID!!!"
                                       _queue_pass = 0
                                else:
                                
                                       print "Time is VALID!!!"
                                       print "Time = " + time_str[0] + ":" + time_str[1] + ":" + time_str[2]
                                       _queue_pass = 1

                
               
                # P = Power Source
		elif sensor_dict['TOM'] == 'P' or sensor_dict['TOM'] == 'p':
                        if len(sensor_dict['PDU']) != 1:
                                print "POWER Source is INVALID!!! != 1 Byte"
                                _queue_pass = 0
                        else:
                                if sensor_dict['PDU'] == 'B' or sensor_dict['PDU'] =='b':
                                       print "Power Source is Battery!!!"
                                       _queue_pass = 1
                                elif sensor_dict['PDU'] == 'M' or sensor_dict['PDU'] == 'm':
                                       print "Power Source is Main DC/AC!!!"
                                       _queue_pass = 1
                                else:
                                       print "Power Source is INVALID!!!"
                                       _queue_pass = 0         

                # B = Battery
		elif sensor_dict['TOM'] == 'B' or sensor_dict['TOM'] == 'b':
			#_battery = str(_data[10:])
			_battery = _data['PDU']
			sensor_dict['PDU'] = _battery
			print "battery = "
			print _battery
			_queue_pass = 1        


		# H = Heartbeat
		elif sensor_dict['TOM'] == 'H':
			#_heartbeat = str(_data[10:])
			_heartbeat = _data['PDU']
			if _heartbeat.isdigit():
				sensor_dict['PDU'] = _heartbeat
				_queue_pass = 1
				print sensor_dict['SRCID'] + " = alive"
			else:
				_queue_pass = 0

                # S = Status
		elif sensor_dict['TOM'] == 'S' or sensor_dict['TOM'] == 's':
			#_status = str(_data[10:])
			_status = _data['PDU']
			if _status.isdigit():
				print "STATUS is: " + _status + "\n"
				if _status == 'L' or _status == 'l':
					print "Device: " + sensor_dict['DEVID'] + \
					      " trying to lock GPS....\n"	
					_queue_pass = 1
					sensor_dict['PDU'] = _status
				elif _status == 'F' or _status == 'f':
					print "Device: " + sensor_dict['DEVID'] + " GPS lock failed!\n"
					_queue_pass = 1
					sensor_dict['PDU'] = _status
				elif _status == 'N' or _status == 'n':
					print "Device: " + sensor_dict['DEVID'] + " Turned ON!\n"
					_queue_pass = 1
					sensor_dict['PDU'] = _status
				elif _status == 'O' or _status == 'o':
					print "Device: " + sensor_dict['DEVID'] + " Turned OFF!\n"
					_queue_pass = 1
					sensor_dict['PDU'] = _status
				elif _status == 'D' or _status == 'd':
					print "Device: " + sensor_dict['DEVID'] + " Debug Mode!\n"
					_queue_pass = 1
					sensor_dict['PDU'] = _status
				elif _status == 'S' or _status == 's':
					print "Device: " + sensor_dict['DEVID'] + " Sleep Mode!\n"
					_queue_pass = 1
					sensor_dict['PDU'] = _status
				elif _status == 'W' or _status == 'w':
					print "Device: " + sensor_dict['DEVID'] + " Woke Up!\n"
					_queue_pass = 1
					sensor_dict['PDU'] = _status
				else:
					print "Device: " + sensor_dict['DEVID'] + \
					      " sent Invalid Status Message!\n"
					_queue_pass = 0
			else:
					print "Device: " + sensor_dict['DEVID'] + \
					      " sent Invalid Status Message: NAN!\n"
					_queue_pass = 0



		# G = GPS
		elif sensor_dict['TOM'] == 'G' or sensor_dict['TOM'] == 'G':
			_gps_str = _data['PDU'].split(',')
			if len(_gps_str[0]) < 1:
				print "Device: " + sensor_dict['DEVID'] + " GPS data invalid! len(_gps_str[0]) < '1'\n"
				_queue_pass = 0
			elif _gps_str[0] == "":
				print "Device: " + sensor_dict['DEVID'] + " GPS data invalid! elif _gps_str[0] is ""\n"
				_queue_pass = 0
			else:
				print "gps raw is: " + _data['PDU'] + "\n"
				_gps_formatted = self.kill_murphy(_gps_str)
				try:
					_lat = _gps_formatted[0]
					_lon = _gps_formatted[1]
					_alt = _gps_str[2]
				except IndexError:
					print "error parsing, index out of range!\n"
				sensor_dict['PDU'] = _lat + ',' + _lon + ',' + _alt
				_queue_pass = 1
				
	
		# R = Registration/Authentication
		elif sensor_dict['TOM'] == 'R':
			#_registration = str(_data[10:])
			_registration = _data['PDU']
			if ',' in _registration:
				try:
					_mac = _registration.split(',')[0]
					_key = _registration.split(',')[1]
				except IndexError:
					print "error parsing, index out of range!\n"
				if _key == _auth_key:
					sensor_dict['PDU'] = _registration
					_queue_pass = 1
				else:
					print "AUTHENTICATION FAILED FROM DEVICE: " + sensor_dict['DEVID'] + "\n"
					_queue_pass = 0
			else:
				_queue_pass = 0

			
		# Invalid Message		
		else:
			print "Invalid Data: Undefined [TOM] Field\n"
			_queue_pass = 0

		return _queue_pass

	        """
                # W = Wireless
		elif sensor_dict['TOM'] == 'W' or sensor_dict['TOM'] == 'w':
                        if sensor_dict['PDU'] == 'S' or sensor_dict['PDU'] = 's':
                               print "Wireless !!!"
                               _queue_pass = 1
                        elif sensor_dict['PDU'] == 'I' or sensor_dict['PDU'] = 'i':
                               print "Power Source is Main DC/AC!!!"
                               _queue_pass = 1
                        else:
                               print "Power Source is INVALID!!!"
                               _queue_pass = 0         
                """


	def kill_murphy(self, gps_coords):
		try:
			gps_coords[0] = str(self.toDecimalDegrees(gps_coords[0]))
			gps_coords[1] = str(self.toDecimalDegrees(gps_coords[1]))
		except IndexError:
			print "error parsing, index out of range!\n"
		return gps_coords

	def toDecimalDegrees(self, ddmm):
		splitat = string.find(ddmm, '.') - 2
		return self._float(ddmm[:splitat]) + self._float(ddmm[splitat:]) / 60.0

	def _float(self, s):
		if s:
			return float(s)
		else:
			return None

	def concatinate(self, data1 , data2):
		temp = data1 << 8
		final = temp | data2
		return final

	def queue_out_data(self, _jobject):
		#Update Low Latency Queue
		LL_queue.get_lock()
		LL_queue.put(_jobject)
		LL_queue.release_lock()
	
		#Update High Latency Queue
		HL_queue.get_lock()
		HL_queue.put(_jobject)
		HL_queue.release_lock()
			


	# Checks for duplicate messages transmitetd over RF
	# Returns: True if match not found, False if match found
	def ringbuffer_verify(self, _data_):
		_md5_hash = _ringbuff.md5_generate(_data_)
		if (_ringbuff.search(_md5_hash) == 0):
			_ringbuff.append(_md5_hash)
			return True
		else:
			return False
