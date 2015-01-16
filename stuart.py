#!/usr/bin/env python

import sys
import serial

try:
    tty = sys.argv[1]
    baudrate = int(sys.argv[2])
    command = sys.argv[3]
    end_marker = sys.argv[4]
except:
    print ""
    print "Utility that executes a command over a serial port and prints the output to stdout."
    print "Useful for capturing large amounts of data (e.g., hex/binary dumps) over serial ports."
    print ""
    print "Usage: %s <tty> <baudrate> <command to execute> <end marker> [--no-newline]" % sys.argv[0]
    print ""
    print "Example: %s /dev/ttyUSB0 115200 'dump 0x80001000 0x80001100' 'operation complete'" % sys.argv[0]
    print ""
    sys.exit(1)

if "--no-newline" not in sys.argv:
    command += "\n"

line = ""
tty = serial.Serial(tty, baudrate)

tty.write(command)
while end_marker not in line:
    line = tty.readline()
    sys.stdout.write(line)
