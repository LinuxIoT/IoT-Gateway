import serial
import os
import logging
import logging.handlers
from sysconfigx import *

class ser_init():
        def __init__(self):
                self.parse = Parser_Functions()
                self.parse.parser_init()
                self.parse.ConfigSectionMap()

        def serial_init(self):
                _section = 'SERIAL'
                _device = self.parse.getSectionOption(_section, 'device')
                _baudrate = int(self.parse.getSectionOption(_section, 'baudrate'))
                _parity = self.parse.getSectionOption(_section, 'parity')
                _stopbits = int(self.parse.getSectionOption(_section, 'stopbits'))
                _bytesize = int(self.parse.getSectionOption(_section, 'bytesize'))
                _timeout = float(self.parse.getSectionOption(_section, 'timeout'))
                _inter_byte_delay = float(self.parse.getSectionOption(_section, 'inter_byte_delay'))
                
                try:
                        ser_init.ser = serial.Serial (port = _device, baudrate = _baudrate, timeout = _timeout, \
                                                  interCharTimeout = _inter_byte_delay, parity = _parity, \
                                                  stopbits = _stopbits, bytesize = _bytesize)
                        print ("Serial Port has been initiallized successfully!!!")
                except serial.SerialException:
                        print "Serial Port Exception: " + _device + "\n"
                        return False                    
                ser_init.ser.flush()
                
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

                _ser = ser_init.ser
                return _ser
        
if __name__ == '__main__':
    ser = ser_init()
    s = ser.serial_init()
    print "Yes!!!"
    print (s)
    
