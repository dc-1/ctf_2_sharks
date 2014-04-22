#!/usr/bin/python
#
# Note that the user might need special permissions to be able to use
# raw sockets.
# 
# Original Code:
#  Gerardo Richarte <gera@coresecurity.com>
#  Javier Kohen <jkohen@coresecurity.com>
#
# Reference for:
#  ImpactDecoder.

from select import select
import socket
import sys

import impacket
from impacket import ImpactDecoder
from impacket import ImpactPacket

#import curses
#stdscr = curses.initscr()

DEFAULT_PROTOCOLS = ('icmp', 'tcp', 'udp')

if len(sys.argv) == 1:
        toListen = DEFAULT_PROTOCOLS
        print "Using default set of protocols. A list of protocols can be supplied from the command line, eg.: %s <proto1> [proto2] ..." % sys.argv[0]
else:
        toListen = sys.argv[1:]

# Open one socket for each specified protocol.
# A special option is set on the socket so that IP headers are included with
# the returned data.
sockets = []
for protocol in toListen:
        try:
                protocol_num = socket.getprotobyname(protocol)
        except socket.error:
                print "Ignoring unknown protocol:" + protocol
                toListen.remove(protocol)
                continue
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol_num)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sockets.append(s)

if 0 == len(toListen):
        print "There are no protocols available."
        sys.exit(0)


# Instantiate an IP packets decoder.
decoder = ImpactDecoder.IPDecoder()
tcpdecoder = ImpactDecoder.TCPDecoder()

#stdscr.nodelay(1)
#curses.cbreak()
#curses.noecho()
while len(sockets) > 0:
        # Wait for an incoming packet on any socket.
	#c = stdscr.getch()
	#if c != -1:
		#curses.nocbreak()
		#curses.echo()
		#curses.endwin()
		#sys.exit(0)
        ready = select(sockets, [], [])[0]
        for s in ready:
                packet = s.recv(8192,socket.MSG_TRUNC)
                if 0 == len(packet):
                        # Socket remotely closed. Discard it.
                        sockets.remove(s)
                        s.close()
                else:
                        # Packet received. Decode and display it.
			p = packet
                        packet = decoder.decode(packet)
			if packet.get_ip_src()[2] == '.':
				for i in range(0,3):
					if s.proto == socket.getprotobyname(DEFAULT_PROTOCOLS[i]):
						type = DEFAULT_PROTOCOLS[i]
						print type
						if type == 'tcp':
							k = ImpactPacket.IP(p)
							off = k.get_header_size()
							p = tcpdecoder.decode(p[off:])
							print p.get_SYN()
						print packet.get_ip_src()
						#print packet.get_size()
