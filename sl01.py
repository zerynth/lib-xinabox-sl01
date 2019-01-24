"""
.. module:: sl01

***************
SL01 Module
***************

This is a Module for the `SL01 <https:#wiki.xinabox.cc/SL01_-_UVA,_UVB,_Light>`_ UVA, UVB, UV Index and luminosity sensor.
The xChip is based on the VEML6075 UVA and UVB Light Sensor and the TSL4531 digital ambient light sensor.
The board uses I2C for communication.

Data Sheets:

-  `VEML6075 <http:#www.vishay.com/docs/84304/veml6075.pdf>`_
-  `TSL4531 <https:#media.digikey.com/pdf/Data%20Sheets/Austriamicrosystems%20PDFs/TSL4531.pdf>`_

    """

import i2c

# Defines VEML6075 Registers
VEML6075_REG_CONF           = 0x00  # Configuration register 
VEML6075_REG_UVA            = 0x07  # UVA register  
VEML6075_REG_UVB            = 0x09  # UVB register
VEML6075_REG_UVCOMP1        = 0x0A  # Visible compensation register
VEML6075_REG_UVCOMP2        = 0x0B  # IR compensation register

# Defines VEML6075
VEML6075_CONF_HD_NORM       = 0x00  # Normal Dynamic Setting
VEML6075_CONF_HD_HIGH       = 0x80  # High Dynamic Setting
VEML6075_CONF_UV_TRIG_ONCE  = 0x04  # Triggers UV Measurement Once
VEML6075_CONF_UV_TRIG_NORM  = 0x00  # Normal Mode Operation
VEML6075_CONF_AF_FORCE      = 0x00  # Normal Mode Enabled
VEML6075_CONF_AF_AUTO       = 0x02  # Active Force Mode Disabled
VEML6075_CONF_SD_OFF        = 0x00  # Power ON
VEML6075_CONF_SD_ON         = 0x01  # Power OFF

VEML6075_CONF_IT_50         = 0x00  # 50ms
VEML6075_CONF_IT_100        = 0x10  # 100ms
VEML6075_CONF_IT_200        = 0x20  # 200ms
VEML6075_CONF_IT_400        = 0x30  # 400ms
VEML6075_CONF_IT_800        = 0x40  # 800ms

# Page 15/22 VEML6075 AppNote 84339
# No teflon (open air)
VEML6075_UVA_VIS_COEFF      = 2.22
VEML6075_UVA_IR_COEFF       = 1.33
VEML6075_UVB_VIS_COEFF      = 2.95
VEML6075_UVB_IR_COEFF       = 1.74
VEML6075_UVA_RESP           = (1.0 / 684.46)
VEML6075_UVB_RESP           = (1.0 / 385.95)

# Defines TSL4531 Registers
TSL4531_REG_CONTROL     = 0x00  # Control Register Address
TSL4531_REG_CONF        = 0x01  # Configuration Register Address
TSL4531_REG_DATA_LOW    = 0x04  # ADC low byte
TSL4531_REG_DATA_HIGH   = 0x05  # ADC high byte

# Defines TSL4531
TSL4531_WRITE_CMD       = 0x80  # Command Register. Must write as 1.
TSL4531_CONF_PWR_DOWN   = 0x00  # Power OFF
TSL4531_CONF_ONE_RUN    = 0x02  # Run ONCE then Power OFF
TSL4531_CONF_START      = 0x03  # Power ON

TSL4531_CONF_IT_100     = 0x02  # 100ms
TSL4531_CONF_IT_200     = 0x01  # 200ms
TSL4531_CONF_IT_400     = 0x00  # 400ms

TSL4531_CONF_PSAVE      = 0x08

class VEML6075(i2c.I2C):
    '''

===============
VEML6075 class
===============

.. class:: VEML6075(self, drvname, addr=0x10, clk=100000)

        Create an instance of the VEML6075 class.

        :param drvname: I2C Bus used '( I2C0, ... )'
        :param addr: Slave address, default 0x10
        :param clk: Clock speed, default 100kHz

    '''

    def __init__(self, drvname = I2C0, addr = 0x10, clk = 100000):
        i2c.I2C.__init__(self, drvname, addr, clk)
        self._addr = addr
        self.__UVAintensity = 0.0
        self.__UVBintensity = 0.0
        self.__UVindex = 0.0
        self.__rawUVA = 0
        self.__rawUVB = 0
        self.__UVcomp1 = 0
        self.__UVcomp2 = 0
        try:
            self.start()
        except PeripheralError as e:
            print(e)
            raise e

    def init(self):
        '''
.. method:: init()

        Configure registers of VEML6075 for UV measurements.
        Call after instantiating VEML6075 class.
        Exception raised if unsuccessful.

        '''
        try:
            self.write_bytes(VEML6075_REG_CONF, VEML6075_CONF_IT_100)
            self.write_bytes(0x00)
        except Exception as e:
            print(e)
            raise e
    def getUVA(self):
        '''
.. method:: getUVA()

        Reads the UVA value and returns it.

        Return the real UVA value as a float data type.

        '''
        self.GET_VEML()
        return self.__UVAintensity

    def getUVB(self):
        '''
.. method:: getUVB()

        Reads the UVB value and returns it.

        Return the real UVB value as a float data type.

        '''
        self.GET_VEML()
        return self.__UVBintensity

    def getUVIndex(self):
        '''
.. method:: getUVIndex()

        Reads the UV Index value and returns it.

        Return the real UV index as a float.

        '''
        self.GET_VEML()
        self.calculateIndex()
        return self.__UVindex

    def GET_VEML(self):
        self.readUVdata()
        self.__UVAintensity = float(self.__rawUVA)
        self.__UVBintensity = float(self.__rawUVB)
        self.__UVAintensity -= (VEML6075_UVA_VIS_COEFF * self.__UVcomp1) - (VEML6075_UVA_IR_COEFF * self.__UVcomp2)
        self.__UVBintensity -= (VEML6075_UVB_VIS_COEFF * self.__UVcomp1) - (VEML6075_UVB_IR_COEFF * self.__UVcomp2)

    def readUVdata(self):
        self.__rawUVA = self.readVEML(VEML6075_REG_UVA)
        self.__rawUVB = self.readVEML(VEML6075_REG_UVB)
        self.__UVcomp1 = self.readVEML(VEML6075_REG_UVCOMP1)
        self.__UVcomp2 = self.readVEML(VEML6075_REG_UVCOMP2)

    def calculateIndex(self):
        UVAComp = 0
        UVBComp = 0
        UVAComp = (self.__UVAintensity * VEML6075_UVA_RESP)
        UVBComp = (self.__UVBintensity * VEML6075_UVB_RESP)
        self.__UVindex = (UVAComp + UVBComp)/2.0

    def readVEML(self, reg):
        raw=self.write_read(reg, 2)
        value = raw[1]*256 + raw[0]
        return value

class TSL4531(i2c.I2C):
    '''

===============
TSL4531 class
===============

.. class:: TSL4531(self, drvname, addr=0x29, clk=100000)

        Create an instance of the TSL4531 class.

        :param drvname: I2C Bus used '( I2C0, ... )'
        :param addr: Slave address, default 0x29
        :param clk: Clock speed, default 100kHz

    '''

    def __init__(self, drvname = I2C0, addr = 0x29, clk = 100000):
        i2c.I2C.__init__(self, drvname, addr, clk)
        self._addr = addr
        self.__LUX = 0.0
        try:
            self.start()
        except PeripheralError as e:
            print(e)
            raise e
            
    def init(self):
        '''
.. method:: init()

        Configure registers of TSL4531 for light measurement.
        Call after instantiating TSL4531 class.
        Exception raised if unsuccessful.

        '''
        try:
            self.write_bytes((TSL4531_WRITE_CMD | TSL4531_REG_CONTROL), TSL4531_CONF_START)
            self.write_bytes((TSL4531_WRITE_CMD | TSL4531_REG_CONF), TSL4531_CONF_IT_100)
        except Exception as e:
            print(e)
            raise e

    def getLUX(self):
        '''
.. method:: getLUX()

        Reads the luminosity value and returns it in LUX.

        Return the LUX value as a float.

        '''
        self.GET_TSL()
        return self.__LUX
        
    def GET_TSL(self):
        multi = int(4)
        raw_LUX_H = self.write_read((TSL4531_WRITE_CMD | TSL4531_REG_DATA_HIGH), 1)[0]
        raw_LUX_L = self.write_read((TSL4531_WRITE_CMD | TSL4531_REG_DATA_LOW), 1)[0]
        data = ((raw_LUX_H <<8)|(raw_LUX_L))
        self.__LUX = multi*(float(data))
