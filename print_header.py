__author__ = "Weqaar Janjua & "
__copyright__ = "Copyright (C) 2016 Linux IoT"
__revision__ = "$Id$"
__version__ = "0.2"


class _header:
       def __init__(self,__file__,__author__,__copyright__,__version__):
              self._marker = '-------------------------------------------'
              self._n = '\n'
              self.__file__=__file__
              self.__author__=__author__
              self.__copyright__=__copyright__
              self.__version__ =__version__ 
           
       def _print(self):
              print self._n + self._marker
              print "Process name:" + self.__file__ + self._n 
              print "Author: " + self.__author__ + self._n  
              print "Copyright: " + self.__copyright__ + self._n 
              print "Version: " + self.__version__ + self._n 
              print self._marker + self._n 
            

if __name__ == '__main__':
    x = _header(__file__,__author__,__copyright__,__version__)
    x._print()
