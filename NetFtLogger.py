#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
# Created 2018 by Lukas Kaul

from struct import *
import socket
from datetime import datetime
import time
import sys, getopt, time, glob


## Initialization
# initialize bytearrays
data = bytearray(36)
Fx_ = bytearray(4)
Fy_ = bytearray(4)
Fz_ = bytearray(4)
Tx_ = bytearray(4)
Ty_ = bytearray(4)
Tz_ = bytearray(4)

# ATI start command: 0x0002
# ATI stop command: 0x0000
start_command = str(unichr(18))+str(unichr(52))+str(unichr(00))+str(unichr(02))+str(unichr(00))+str(unichr(00))+str(unichr(00))+str(unichr(00))
stop_command = str(unichr(18))+str(unichr(52))+str(unichr(00))+str(unichr(00))+str(unichr(00))+str(unichr(00))+str(unichr(00))+str(unichr(01))


# ATI NET-FT
atiAddress = ('192.168.1.1',49152)
# create socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# connect to NetBox
sock.connect(atiAddress)
print 'Socket opened'

def logData(path):
	print "Logging to path ", path
	basename = raw_input('Enter file name: ')	
	
	# start streaming FT-data by sending start command
	sock.sendto(start_command,atiAddress)
	timeOffset = time.time();

	with open(path+basename+'.csv','w') as logFile:
		logFile.write('Time,Fx,Fy,Fz\n')
		try:
			print "logging data...."
			# logging as fast as possible			
			while True:	
				logFile.write('%f,'%(time.time()-timeOffset)) # timestamp				
					
				# FT-Data 
				d = sock.recvfrom_into(data,36)
				for i in range(4):
					Fx_[i] = data[12+i]
					Fy_[i] = data[16+i]
					Fz_[i] = data[20+i]
					Tx_[i] = data[24+i]
					Ty_[i] = data[28+i]
					Tz_[i] = data[32+i]
				
				# convert binary data to float
				Fx = unpack('!i',Fx_)
				Fy = unpack('!i',Fy_)
				Fz = unpack('!i',Fz_)
				Tx = unpack('!i',Tx_)
				Ty = unpack('!i',Ty_)
				Tz = unpack('!i',Tz_)
				
				logFile.write('%f,%f,%f'%(Fx[0]/float(1000000),Fy[0]/float(1000000),Fz[0]/float(1000000)))
				logFile.write('%f,%f,%f'%(Tx[0]/float(1000000),Ty[0]/float(1000000),Tz[0]/float(1000000)))				
				
				# print for online feedback
				print Fz[0]/float(1000000)
								
				logFile.write('\n')
			
		except KeyboardInterrupt:
			logFile.close()
			sock.sendto(stop_command,atiAddress)
			print "\n\nInterrupted by user - sensor connecetion and output files closed\n\n"
		
logData(path = 'NetFT/')
