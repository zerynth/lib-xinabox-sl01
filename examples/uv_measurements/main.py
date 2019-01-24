##############################################
#   This is an example for SL01 UV and light
#	sensor.
#
#   UV data is read and printed out on the 
# 	console.
##############################################

import streams
from xinabox.sl01 import sl01

streams.serial()

# SL01 instance
SL01_V = sl01.VEML6075(I2C0)

# configure and start SL01
SL01_V.init()

while True:
    uva=SL01_V.getUVA()		# return uva intensity 
    uvb=SL01_V.getUVB()		# return uvb intensity
    uvi=SL01_V.getUVIndex()	# return uv index
    
    print('UVA Intensity: ', uva, ' uW/m^2\n\n')
    print('UVB Intensity: ', uvb, ' uW/m^2\n\n')
    print('UV Index     : ', uvi, '\n\n')
    
    sleep(2000)
