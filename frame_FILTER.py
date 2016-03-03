from sysconfigx import *
from time import *
from serial_raw_queue import serial_queue

class frame_filter():

    def __init__(self):
        global _frame
        self.parse = Parser_Functions()
	self.parse.parser_init()
	self.parse.ConfigSectionMap()
        self.queue = serial_queue()
        self.read_frame_size()
        pass
        
    def read_frame_size(self):

        #Initialize FRAME
        _section = 'FRAME'
        global _frame_netid_len
        global _frame_srcid_len
        global _frame_dstid_len
        global _frame_phytype_len
        global _frame_devtype_len
        global _frame_tom_len
        global _frame_prio_len
        global _frame_seqnum_len
        global _frame_pdul_len
        global _frame_pdut_len
        global _frame_pdu_len
        global _frame_ecc_len
        global _frame_fields_num
        global _frame_min_len
        global _frame_max_len
        
        _frame_netid_len = int(self.parse.getSectionOption(_section, 'netid'))
        _frame_srcid_len = int(self.parse.getSectionOption(_section, 'srcid'))
        _frame_dstid_len = int(self.parse.getSectionOption(_section, 'dstid'))
        _frame_phytype_len = int(self.parse.getSectionOption(_section, 'phytype'))
        _frame_devtype_len = int(self.parse.getSectionOption(_section, 'devtype'))
        _frame_tom_len = int(self.parse.getSectionOption(_section, 'tom'))
        _frame_prio_len = int(self.parse.getSectionOption(_section, 'prio'))
        _frame_seqnum_len = int(self.parse.getSectionOption(_section, 'seqnum'))
        _frame_pdul_len = int(self.parse.getSectionOption(_section, 'pdul'))
        _frame_pdut_len = int(self.parse.getSectionOption(_section, 'pdut'))
        _frame_pdu_len = int(self.parse.getSectionOption(_section, 'pdu'))
        _frame_ecc_len = int(self.parse.getSectionOption(_section, 'ecc'))
        _frame_fields_num = int(self.parse.getSectionOption(_section, 'framefields'))
        _frame_min_len = _frame_netid_len + _frame_srcid_len + _frame_dstid_len + _frame_phytype_len + _frame_devtype_len + \
                 _frame_tom_len + _frame_prio_len + _frame_seqnum_len + _frame_pdul_len + _frame_pdut_len + _frame_ecc_len
        _frame_max_len = _frame_min_len + _frame_pdu_len
        print("Frame Min Length =  %d"% _frame_min_len)

    def read_frame(self):
	if self.queue.is_empty():
	    print "Raw Data queue is Empty!\n"
	    return False
	else:
            self.queue.get_lock()
            _frame = self.queue.get()
            self.queue.release_lock()
            print "MY FRAME IS = " + str(_frame)

            if _frame is "":
                return False
            else:
                _validation_status, _reconstructed_frame = self.validate_frame(_frame)
                if _validation_status is True:
                    print "Frame is Valid!\n"
                    return _reconstructed_frame
                else:
                   print "ERROR -> Frame is InValid!\n"
                   return False

    def validate_frame(self,_frame):
        _reconstructed_frame = "NULL"

        if _frame is None:
            return [False, _reconstructed_frame]
        elif _frame is "":
            return [False, _reconstructed_frame]
##        elif _frame.startswith('OK'):
##            return [False, _reconstructed_frame]
        elif len(_frame) < _frame_min_len:
            print "len(_frame) < _frame_min_len\n"
            return [False, _reconstructed_frame]
        elif len(_frame) > _frame_max_len:
            print "len(_frame) > _frame_max_len\n"
            return [False, _reconstructed_frame]


##        elif _frame.startswith("+DATA:") and ("BYTES" in _frame):
##            print "_frame.startswith(+DATA:)\n"

        
##          try:
##              _mac_id=_frame.split(" ")[4]
##              print "MAC: " + _mac_id + "\n"
##          except IndexError:
##              print "Invalid Frame, Unable to parse MAC: List index out of range" + "\n"
##              return [False, _reconstructed_frame]
##          return [True, _reconstructed_frame]
        #elif _mac_id is None:
        #   print "MAC ID: is NULL\n"
        #   return [False, _reconstructed_frame]


        
        else:   
            print "FRAME: " + str(_frame) + "\n"
            _expanded_frame=['NETID', 'SRCID', 'DSTID', 'PHYTYPE','DEVTYPE', 'TOM', \
                     'PRIO', 'SEQNUM', 'PDUL' , 'PDUT', 'PDU', 'ECC']
            try:    
                _expanded_frame[0] = _frame[1:3]
                _expanded_frame[1] = _frame[3:5]
                _expanded_frame[2] = _frame[5:7]
                _expanded_frame[3] = _frame[7]
            except IndexError:
                print "error parsing, index out of range!\n"
                return [False, _reconstructed_frame]

            
##            try:
##                _mac_id
##            except NameError:
##                return [False, _reconstructed_frame]

            try:
                _expanded_frame[4] = _frame[8]
                _expanded_frame[5] = _frame[9]
                _expanded_frame[6] = _frame[10]
                _expanded_frame[7] = _frame[11:13]
                _expanded_frame[8] = _frame[13]
                _expanded_frame[9] = _frame[14]
                dat = 15 + int(_expanded_frame[8])
                _expanded_frame[10] = _frame[15:dat]
                _expanded_frame[11] = _frame[dat:dat+2]
            except IndexError:
                print "Invalid Frame, Unable to parse MAC: List index out of range" + "\n"
                return [False, _reconstructed_frame]

            _reconstructed_frame = {'NETID'     : _expanded_frame[0], \
                            'SRCID'     : _expanded_frame[1], \
                            'DSTID'     : _expanded_frame[2], \
                            'PHYTYPE'   : _expanded_frame[3], \
                            'DEVTYPE'   : _expanded_frame[4], \
                            'TOM'       : _expanded_frame[5], \
                            'PRIO'      : _expanded_frame[6], \
                            'SEQNUM'    : _expanded_frame[7], \
                            'PDUL'      : _expanded_frame[8], \
                            'PDUT'      : _expanded_frame[9], \
                            'PDU'       : _expanded_frame[10], \
                            'ECC'       : _expanded_frame[11]}
            print "Reconstructed FRAME is: " + str(_reconstructed_frame) + "\n"
                
            
            if len(_expanded_frame) < _frame_fields_num:
                print "_frame_fields_num"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame) > _frame_fields_num:
                print "_frame_fields_num"
                return [False, _reconstructed_frame]
            
            #Verify NETID Field Width
            elif len(_expanded_frame[0]) > _frame_netid_len:
                print "_frame_netid"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame[0]) < _frame_netid_len:
                print "_frame_netid"
                return [False, _reconstructed_frame]

            #Verify SRCID Field Width
            elif len(_expanded_frame[1]) > _frame_srcid_len:
                print "_frame_srcid"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame[1]) < _frame_srcid_len:
                print "_frame_srcid"
                return [False, _reconstructed_frame]

            #Verify DSTID Field Width
            elif len(_expanded_frame[2]) > _frame_dstid_len:
                print "_frame_dstid"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame[2]) < _frame_dstid_len:
                print "_frame_dstid"
                return [False, _reconstructed_frame]

            #Verify PHYTYPE Field Width
            elif len(_expanded_frame[3]) > _frame_phytype_len:
                print "_frame_phytype"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame[3]) < _frame_phytype_len:
                print "_frame_phytype"
                return [False, _reconstructed_frame]
            elif _expanded_frame[3] != 'Z' and _expanded_frame[4] != 'W' and _expanded_frame[4] != 'E' \
                 and _expanded_frame[3] != 'z' and _expanded_frame[4] != 'w' and _expanded_frame[4] != 'e':
                print "INVALID PHYTYPE"
                return [False, _reconstructed_frame]            

            #Verify DEVTYPE Field Width
            elif len(_expanded_frame[4]) > _frame_devtype_len:
                print "_frame_devtype"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame[4]) < _frame_devtype_len:
                print "_frame_devtype"
                return [False, _reconstructed_frame]
            elif _expanded_frame[4] != 'S' and _expanded_frame[5] != 'R' and _expanded_frame[5] != 'G' and _expanded_frame[5] != 'C' \
                 and _expanded_frame[4] != 's' and _expanded_frame[5] != 'r' and _expanded_frame[5] != 'g' and _expanded_frame[5] != 'c':
                print "INVALID DEVTYPE"
                return [False, _reconstructed_frame]
            
##            #Verify MACID Field Width
##            elif len(_expanded_frame[3]) > _frame_macid_len:
##                return [False, _reconstructed_frame]
##            elif len(_expanded_frame[3]) < _frame_macid_len:
##                return [False, _reconstructed_frame]

            #Verify TOM Field Width
            elif len(_expanded_frame[5]) > _frame_tom_len:
                print "_frame_tom"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame[5]) < _frame_tom_len:
                print "_frame_tom"
                return [False, _reconstructed_frame]
            elif _expanded_frame[5] != 'A' and _expanded_frame[5] != 'T' and _expanded_frame[5] != 'I' and _expanded_frame[5] != 'P' and _expanded_frame[5] != 'G' \
                 and _expanded_frame[5] != 'B' and _expanded_frame[5] != 'H' and _expanded_frame[5] != 'S' and _expanded_frame[5] != 'R' and _expanded_frame[5] != 'W' \
                 and _expanded_frame[5] != 'a' and _expanded_frame[5] != 't' and _expanded_frame[5] != 'i' and _expanded_frame[5] != 'p' and _expanded_frame[5] != 'g' \
                 and _expanded_frame[5] != 'b' and _expanded_frame[5] != 'h' and _expanded_frame[5] != 's' and _expanded_frame[5] != 'r' and _expanded_frame[5] != 'w':
                print "INVALID TOM"
                return [False, _reconstructed_frame]

            #Verify PRIO Field Width
            elif len(_expanded_frame[6]) > _frame_prio_len:
                print "_prio"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame[6]) < _frame_prio_len:
                print "_frame_prio"
                return [False, _reconstructed_frame]
            elif _expanded_frame[6].isdigit() == False:
                print "PRIO must be number string"
                return [False, _reconstructed_frame]
            
            #Verify SEQNUM Field Width
            elif len(_expanded_frame[7]) > _frame_seqnum_len:
                print "_frame_seqnum"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame[7]) < _frame_seqnum_len:
                print "_frame_seqnum"
                return [False, _reconstructed_frame]
                        

            #Verify PDUL Field Width
            elif len(_expanded_frame[8]) > _frame_pdul_len:
                print "_frame_PDUL"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame[8]) < _frame_pdul_len:
                print "_frame_PDUL"
                return [False, _reconstructed_frame]
            elif _expanded_frame[8].isdigit() == False:
                print "PDUL must be number string"
                return [False, _reconstructed_frame]
            

            #Verify PDUT Field Width
            elif len(_expanded_frame[9]) > _frame_pdut_len:
                print "_frame_PDUT"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame[9]) < _frame_pdut_len:
                print "_frame_PDUT"
                return [False, _reconstructed_frame]

            #Verify ECC Field Width
            elif len(_expanded_frame[11]) > _frame_ecc_len:
                print "_frame_ECC"
                return [False, _reconstructed_frame]
            elif len(_expanded_frame[11]) < _frame_ecc_len:
                print "_frame_ECC"
                return [False, _reconstructed_frame]

            #Verify PDU Field Width
            elif len(_expanded_frame[10]) > _frame_pdu_len:
                print "_frame_PDU"
                return [False, _reconstructed_frame]
            else:       
                _reconstructed_frame = {'NETID'     : _expanded_frame[0], \
                            'SRCID'     : _expanded_frame[1], \
                            'DSTID'     : _expanded_frame[2], \
                            'PHYTYPE'   : _expanded_frame[3], \
                            'DEVTYPE'   : _expanded_frame[4], \
                            'TOM'       : _expanded_frame[5], \
                            'PRIO'      : _expanded_frame[6], \
                            'SEQNUM'    : _expanded_frame[7], \
                            'PDUL'      : _expanded_frame[8], \
                            'PDUT'      : _expanded_frame[9], \
                            'PDU'       : _expanded_frame[10], \
                            'ECC'       : _expanded_frame[11]}
                print "Reconstructed FRAME is: " + str(_reconstructed_frame) + "\n"
                return [True, _reconstructed_frame]
