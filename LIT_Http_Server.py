import threading
from LIT_Gateway_Http_Server_Methods import LIT_http_server_Functions

class Http_Server(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		_HTTP_SERVER = LIT_http_server_Functions()
		_HTTP_SERVER.start_server()
