import hashlib

class RingBuffer(object):
	""" class that implements a not-yet-full buffer """
	def __init__(self, size_max):
		self.max = size_max
		self.data = [  ]
	class __Full(object):
		""" class that implements a full buffer """
		def append(self, x):
			""" Append an element overwriting the oldest one. """
			self.data[self.cur] = x
			self.cur = (self.cur+1) % self.max
		def tolist(self):
			""" return list of elements in correct order. """
			return self.data[self.cur:] + self.data[:self.cur]
		def search(self, item):
			if (item in self.data):
				return 1
			else:
				return 0
		def md5_generate(self, arr):
			return hashlib.md5(arr).hexdigest()

	def append(self, x):
		""" append an element at the end of the buffer. """
		self.data.append(x)
		if len(self.data) == self.max:
			self.cur = 0
			# Permanently change self's class from non-full to full
			self.__class__ = self.__Full
	def tolist(self):
		""" Return a list of elements from the oldest to the newest. """
		return self.data
	def search(self, item):
		if (item in self.data):
			return 1
		else:
			return 0
	def md5_generate(self, arr):
		return hashlib.md5(arr).hexdigest()
		
