#############
#
#	i2c_RTC Clock Module
#
#
#
############


import smbus
import time

bus = smbus.SMBus(0)

address = 0x60

