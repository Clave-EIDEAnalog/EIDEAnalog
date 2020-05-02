# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEAnalog library (excerpt). Class ADS1115. Minimum version              #
#                                                                           #
# Librería EIDEAnalog (extracto). Clase ADS1115. Versión mínima             #
# Consulte punto 4, ‘Clase ADS1115’ en EIDEAnalog_ASI_SE_HIZO.pdf           #
# para más información (https://github.com/Clave-EIDEAnalog/DOCS)           #
#                                                                           #
# Copyright (c) 2020. Clave Ingenieros S.L.;                                #
# vicente.fombellida@claveingenieros.es                                     #
#                                                                           #
#############################################################################
import smbus
i2c = smbus.SMBus(1)


class ADS1115():

    # Registers
    confReg = 0b00000001
    convReg = 0b00000000

    # Start conversion
    startConv    = 0b1000000000000000
    # “Done” bit
    done         = 0b1000000000000000

    def __init__(self, address, ordinal=0, name=None):
        # ADS bus and address (i2c)
        self.addr = address
        self.ordinal = ordinal
        self.name = name
     
    def swap(self, word):
        """ Swaps the two bytes of a word """
        valor = ((word&0xff00)>>8) | ((word&0x00ff)<<8)
        return valor

    def readWord(self, register):
        """Read word from ADS1115 register """
        valor = i2c.read_word_data(self.addr, register)
        valor = self.swap(valor)
        return valor

    def readConfig(self):
        """ Read config reg. """
        r = self.readWord(ADS1115.confReg)
        return r

    def sendWordToConfReg(self, word):
        """ Send a word to the ADS1115 configuration register """
        # swap byte order 
        word = self.swap(word)
        i2c.write_word_data(self.addr, ADS1115.confReg, word)
        
    def singleShot(self):
        """ Start an analog to digital conversion """
        #Read config register
        valor = self.readConfig()
        # Set "single shot" bit
        valor = valor | ADS1115.startConv
        self.sendWordToConfReg(valor)

    def ready(self):
        """ Return true if last task accomplished """
        valor = self.readConfig()
        ready = valor & ADS1115.done
        return ready

    def readConversion(self):
        """ Returns the conversion register contents """
        valor = self.readWord(ADS1115.convReg)
        return valor

