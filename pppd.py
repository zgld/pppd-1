#!/bin/python
"""
pppd.py: Implementation of PPP connection establishment in Python
by Kwon Hyuckmin
June 3, 2013.
"""
import sys
import os
import re
import termios
import fcntl
import time
import errno

option = {"noaccomp": False,
          "nopcomp": False,
          "asyncmap": False,
          "ip_src": "0.0.0.0",
          "ip_dest": "0.0.0.0"}

#noccp noaccomp nopcomp asyncmap 0xffffffff
#pppd -detach crtscts lock debug record /root/ppp1 noccp
#192.168.56.101:192.168.56.102 /dev/ttyS0 38400
argv = sys.argv
ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', argv)

if argv.find("noaccomp") != -1:
    option["noaccomp"] = True

if argv.find("nopcomp") != -1:
    option["nopcomp"] = True

if argv.find("asyncmap") != -1:
    option["asyncmap"] = argv[argv.find("asyncmap")+1]

option["ip_src"] = ip[0]
option["ip_dest"] = ip[1]

BAUDRATE = termios.B38400
SERIALDEVICE = "/dev/ttyS0"

fd_serial_device = os.open(SERIALDEVICE,
                           os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)

term_attr = termios.tcgetattr(fd_serial_device)
term_attr[0] = termios.IGNPAR | termios.ICRNL
term_attr[2] = BAUDRATE | termios.CRTSCTS | termios.CS8 | termios.CREAD

termios.tcflush(fd_serial_device, termios.TCIOFLUSH)
termios.tcsetattr(fd_serial_device, termios.TCSANOW, term_attr)

while True:


#pppd -detach crtscts lock debug record /root/ppp2 noccp 192.168.56.102:192.168.56.101 /dev/ttyS0 38400
