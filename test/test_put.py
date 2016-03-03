from COAP_queue import coap_queue
from time import *


coap = coap_queue()
while True:
    sleep(1)
    coap.get_lock()
    coap.put("ahmer")
    coap.release_lock()
    
