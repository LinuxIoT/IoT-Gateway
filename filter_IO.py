#from serial_raw_queue import serial_queue
import threading
from time import *
from frame_FILTER import frame_filter
from Dynamic_False_Reduction_Alarm_queue import DFRA_out_queue


class filter_data(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global _filter_data

    def run(self):
        f = frame_filter()
        queue = DFRA_out_queue()
        while True:
            sleep(1)
            _data = f.read_frame()
            if _data is False:
                pass
            elif _data == "NULL":
                pass
            else:
                queue.get_lock()
                queue.put(_data)
                print "PUT Data to Filter Queue = "
                print str(_data)
                queue.release_lock()
