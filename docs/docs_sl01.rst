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

    
===============
VEML6075 class
===============

.. class:: VEML6075(self, drvname, addr=0x10, clk=100000)

        Create an instance of the SL01 class.

        :param drvname: I2C Bus used '( I2C0, ... )'
        :param addr: Slave address, default 0x10
        :param clk: Clock speed, default 100kHz

    
.. method:: init()

        Configure registers of VEML6075 for UV measurements.
        Call after instantiating VEML6075 class.
        Exception raised if unsuccessful.

        
.. method:: getUVA()

        Reads the UVA value and returns it.

        Return the real UVA value as a float data type.

        
.. method:: getUVB()

        Reads the UVB value and returns it.

        Return the real UVB value as a float data type.

        
.. method:: getUVIndex()

        Reads the UV Index value and returns it.

        Return the real UV index as a float.

        
===============
TSL4531 class
===============

.. class:: TSL4531(self, drvname, addr=0x29, clk=100000)

        Create an instance of the TSL4531 class.

        :param drvname: I2C Bus used '( I2C0, ... )'
        :param addr: Slave address, default 0x29
        :param clk: Clock speed, default 100kHz

    
.. method:: init()

        Configure registers of TSL4531 for light measurement.
        Call after instantiating TSL4531 class.
        Exception raised if unsuccessful.

        
.. method:: getLUX()

        Reads the luminosity value and returns it in LUX.

        Return the LUX value as a float.

        
