#!/usr/bin/env python2

import re
import serial
import consts

class CoffeePot:
    
	def __init__(self, device):
		self.pot = serial.Serial(device, 9600)
		self.pot.open()
		if not self.pot.isOpen():
			raise Exception('Coffee pot is not connected!')
	
	def brew(self):
		return self.sendAndReceive(consts.BREW_COFFEE)

	def stopBrewing(self):
		return self.sendAndReceive(consts.STOP_BREWING)

	def isCoffeeBrewing(self):
		return self.sendAndReceive(consts.IS_COFFEE_BREWING)

	def getNbLitres(self):
		self.pot.write(consts.WATER_STATUS['message'] + '\n')
		line = self.pot.readline()
		print line
		if line != consts.WATER_STATUS['bad']:
			return int(re.findall(consts.WATER_STATUS['statuses']['good'])[0], line)
		else:
			return 0
	
	def isEmpty(self):
		return self.getNbLitres() == 0
	
	def hasBucket(self):
		return self.sendAndReceive(consts.BUCKET_STATUS)
		
	def sendAndReceive(self, message):	
		self.pot.write(message['message'] + '\n')
		line = self.pot.readline()
		return line == message['statuses']['good']

if __name__ == '__main__':
	pot = CoffeePot('/dev/ttyUSB0')
	print pot.getNbLitres()

