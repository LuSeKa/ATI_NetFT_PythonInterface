#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
# Created 2018 by Lukas Kaul

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def printData(path, basename):
	print "plotting from file ", path+basename+'.csv'
	data = np.genfromtxt(path+basename+'.csv', delimiter=',', skip_header=1, skip_footer=1, names=['time', 'Fx', 'Fy', 'Fz', 'Tx', 'Ty', 'Tz'])
	
	plt.plot(data['time'], data['Fx'], color='r', label='Fx')
	plt.plot(data['time'], data['Fy'], color='g', label='Fy')
	plt.plot(data['time'], data['Fz'], color='b', label='Fz')
	
	plt.plot(data['time'], data['Tx'], color='r', label='Tx')
	plt.plot(data['time'], data['Ty'], color='g', label='Ty')
	plt.plot(data['time'], data['Tz'], color='b', label='Tz')
	plt.legend()	
	plt.show()
	
basename = raw_input('Enter file basename: ')
printData('NetFT/', basename)
