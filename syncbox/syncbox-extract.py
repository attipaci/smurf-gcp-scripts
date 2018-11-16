#!/usr/bin/python

# Script that extracts the relevant SyncBox parameters into a shell (bash)
# snipplet of variable declarations for ROW_LEN, NUM_ROWS, and DATA_RATE
#
# Author: Attila Kovacs <attila.kovacs@cfa.harvard.edu>
# Version: 12 Novembver 2018
#

import serial
import time

s = serial.Serial('/dev/ttyUSB0', 9600)

s.write('?\r\n')

# Give it some time to process
time.sleep(0.25)

values = s.read(s.inWaiting()).split('\r')

print('DATA_RATE=' + str(int(values[3].split('=')[1])))
print('ROW_LEN=' + str(int(values[4].split('=')[1])))
print('NUM_ROWS=' + str(int(values[5].split('=')[1])))
print('CLK_DIV=' + str(int(values[6].split('=')[1])))


