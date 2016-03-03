##from netifaces import interfaces, ifaddresses, AF_INET6
##
##def ip6_addresses():
##    ip_list = []
##    for interface in interfaces():
##        for link in ifaddresses(interface)[AF_INET6]:
##            ip_list.append(link['addr'])
##    return ip_list
##
##
##ip6_addresses()
##
##
##
##
##


import sys, socket;
host = socket.gethostname();
result = socket.getaddrinfo(host, None);
print "family:%i socktype:%i proto:%i canonname:%s sockaddr:%s"%result[0];
result = socket.getaddrinfo(host, None, socket.AF_INET);
print "family:%i socktype:%i proto:%i canonname:%s sockaddr:%s"%result[0];
result = socket.getaddrinfo(host, None, socket.AF_INET6);
print "family:%i socktype:%i proto:%i canonname:%s sockaddr:%s"%result[0];












### Echo server program
##import socket
##import sys
##
##HOST = None               # Symbolic name meaning all available interfaces
##PORT = 50007              # Arbitrary non-privileged port
##s = None
##for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
##                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
##    af, socktype, proto, canonname, sa = res
##    print af, socktype, proto, canonname, sa
##    try:
##        s = socket.socket(af, socktype, proto)
##    except socket.error as msg:
##        s = None
##        continue
##    try:
##        s.bind(sa)
##        s.listen(1)
##    except socket.error as msg:
##        s.close()
##        s = None
##        continue
##    break
##if s is None:
##    print 'could not open socket'
##    sys.exit(1)
##conn, addr = s.accept()
##print 'Connected by', addr
##
##print conn
##print addr
##while 1:
##    data = conn.recv(1024)
##    if not data: break
##    conn.send(data)
##conn.close()
##


















###!/usr/bin/env python
##import sys
##import struct
##import socket
##
##
##print socket.has_ipv6
##HOST = 'fe80::d27e:35ff:fe95:9ceb'
##PORT = 50007
##
##socket.getaddrinfo(HOST, PORT, 0, 0, 6)
##sa = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
##sa.bind((HOST , PORT))
##
##print "YES"
##print sa
##
##res = socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_DGRAM, 0, socket.AI_PASSIVE)
##print res[0]
##
##family, socktype, proto, canonname, sockaddr = res[0]
##print proto
##print sockaddr
##
