#!/usr/bin/python

__author__ = "Weqaar Janjua & Ahmer Malik"
__copyright__ = "Copyright (C) 2016 Linux IoT"
__revision__ = "$Id$"
__version__ = "1.0"

import sys
import gc
import socket
from time import *

from print_header import _header
from init import sysinit
from serial_config import ser_init
from serial_IO import serial_data
from filter_IO import filter_data
from DFRA_decoder import DFRA

from GW_COAPTHON import start_coap
from sysconfigx import *

from ZMQ_High_Latency_Thread import *
from ZMQ_Low_Latency_Thread import *
from LIT_Http_Server import Http_Server


_thread_pool = []


def main():
        
        # Print headers. Use print_header.py
        h = _header(__file__,__author__,__copyright__,__version__)
        h._print()
        
        # Initiallize the System. Use init.py
        sysinit_obj = sysinit()
        sysinit_obj.run()
        
        # Print the grabage collector = True/False
        print "Garbage Collector Enabled: " + str(gc.isenabled()) + "\n"

        # Initiallize the Serial Port for reading data from serial
        ser_obj = ser_init()
        ser = ser_obj.serial_init()
        print ser

        # Check whether  to initiallize Coap Server or Not
        parse = Parser_Functions()
        parse.parser_init()
        parse.ConfigSectionMap()

        _section = 'COAP'
        _server = parse.getSectionOption(_section, 'server')
        _ip = parse.getSectionOption(_section, 'ip')
        _port = int(parse.getSectionOption(_section, 'port'))

        if _server == '0':
                print "OFF COAP Server"
        elif _server == '1':
                print "COAP Server has been Started"
                t0 = start_coap(_ip,_port,False)
                t0.start()
                _thread_pool.append(t0)
        else:
                print "INVALID Section [COAP] = OPTION [Server]. Only 0/1 boolean"
                return exit
            
        # Spawn Threads
        
        # Get Serial Data by spawning thread t1. Use serial_IO.py
        t1 = serial_data(ser)
        t1.start()
        _thread_pool.append(t1)

        # Filter the raw serial data based on the frame structure.
        t2 = filter_data()
        t2.start()
        _thread_pool.append(t2)

        t3 = DFRA()
        t3.start()
        _thread_pool.append(t3)

        t4 = ZMQ_LL()
	t4.start()
	_thread_pool.append(t4)

        
	t5 = ZMQ_HL()
	t5.start()
	_thread_pool.append(t5)

##	
	t6 = Http_Server()
	t6.start()
	_thread_pool.append(t6)
	


if __name__ == '__main__':
        main()

