#!/usr/bin/env python
# Dumps system memory via some Arcadyan bootloaders.

import sys
import time
import serial

class SerialDumper(object):

    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.line_end = "\r\n"
        self.serial = serial.Serial(port, baudrate=baudrate, timeout=1)

    def __del__(self):
        self.close()

    def close(self):
        self.serial.close()

    def command(self, cmd):
        self.serial.write(cmd + self.line_end)

    def dump(self, commands=[], read_until=""):
        count = 0

        for i in range(0, len(commands)):
            self.command(commands[i])
            if (i+1) != len(commands):
                time.sleep(1)
                self.serial.flush()
                self.serial.flushInput()

        while not data.endswith(read_until):
            byte = self.serial.read(1)
            if not byte:
                break
            else:
                sys.stdout.write(byte)
                count += 1
                if (count % 1024) == 0:
                    sys.stderr.write("\b" * 80)
                    sys.stderr.write("Read status: 0x%X..." % count)

        return count

if __name__ == '__main__':
    data = ''
    bytes_read = 0
    sd = SerialDumper()
    read_address = 0xBF000000
    read_size = 2 * 1024 * 1024
    block_size = 8192

    while bytes_read < read_size:
        sd.dump(commands=["r", "%8X" % read_address, "1", block_size], read_until="[WG7005G11-LF-88 Boot]")
        read_address += (block_size * 4)
        bytes_read += (block_size * 4)
        sys.stderr.write("Bytes read: 0x%8X / 0x%8X [0x%8X]\n" % (bytes_read, read_size, read_address))

    sd.close()

