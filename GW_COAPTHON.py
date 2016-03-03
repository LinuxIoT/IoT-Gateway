import sys
sys.path.insert(0, '/home/ahmer/Ahmer/Techknox/Python_Exercises/IoT-Gateway-Embedded-V3/COAPTHON/')
from coapserver import CoAPServer
from time import *
import threading


class start_coap(threading.Thread):
	def __init__(self,ip,port,multicast):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.multicast=multicast
		global _data

	def run(self):
                while True:
                        sleep(0.5)
                        coap = CoAPServer(self.ip,self.port,self.multicast)
                        print "***************************Entering Server******************"
                        coap.main_2()
                        print "****************************Leaving Server *****************"
                
                        
