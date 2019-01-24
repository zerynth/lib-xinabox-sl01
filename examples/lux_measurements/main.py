##############################################
#   This is an example for SL01 UV and light
#	sensor.
#
#   Ambient light level is measured and
# 	printed out on the console.
##############################################

import streams
from xinabox.sl01 import sl01

streams.serial()

# SL01 instance
SL01_T = sl01.TSL4531(I2C0)

# configure and start TSL4531
SL01_T.init()

while True:
	lux=SL01_T.getLUX()	#return ambient light level as lux
	print('Light level: ', lux, ' LUX')

	sleep(2000)