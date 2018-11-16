#!/usr/bin/python

# A simple script to send commands to the SyncBox
#
# Author: Attila Kovacs <attila.kovacs@cfa.harvard.edu>
# Version: 12 November 2018

import serial
import sys
import time

s = serial.Serial('/dev/ttyUSB0', 9600)

cmd = ''
for i in range (1, len(sys.argv)):
	cmd += sys.argv[i] + ' '

s.write(cmd + '\r\n')

# give it some time to process...
time.sleep(0.25)

result = s.read(s.inWaiting()).split('\r')

for i in range(0, len(result)):
	print(result[i])


