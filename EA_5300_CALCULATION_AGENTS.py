# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEAnalog library (excerpt). Calculation agents (classes)                #
#                                                                           #
# Librería EIDEAnalog (extracto). Clases ‘agentes de cálculo’               #
# Ver 5.3.- Algoritmos de cálculo … en EIDEAnalog_ASI_SE_HIZO.pdf           #
# para más información (https://github.com/Clave-EIDEAnalog/DOCS)           #
#                                                                           #
# Copyright (c) 2020. Clave Ingenieros S.L.;                                #
# vicente.fombellida@claveingenieros.es                                     #
#                                                                           #
#############################################################################
class calculationAgent():
    
    def __init__(self, Vref, gain, zero, bits, twosC, table=None):
        self.Vref = Vref
        self.gain = gain
        self.zero = zero
        self.bits = bits
        self.twosC = twosC
        self.table = table

    def convert(self):
        pass
       

class binaryAgent(calculationAgent):
    
    def __init__(self, Vref, gain, zero, bits, twosC, table=None):
        calculationAgent.__init__(self, Vref, gain, zero, bits, twosC, None)
        self.name = 'binary'

    def binaryToDecimal(self, value):
        if self.twosC:
            # Two's complement format
            value = value - int((value << 1) & 2**self.bits) # Int value
            value = value / float(2**(self.bits - 1))
        else:
            value = value / float(2**self.bits)
            
        value = ((value * self.Vref) - self.zero) * self.gain
        return value

    def convert(self, value):
        return self.binaryToDecimal(value)


class ASCIIAgent(calculationAgent):
    """  'ascii' calculation agent """
    
    def __init__(self, Vref, gain, zero, bits, twosC, tabla):
        calculationAgent.__init__(self, Vref, gain, zero, bits, twosC, None)
        self.name = 'ASCII'

    def ASCIIToDecimal(self, value):
        """ Return a float from (ascii) """
        return value * self.gain
 
    def convert(self, value):
        """ Return a float from the raw value (ascii) """
        return self.ASCIIToDecimal(value)
            

class tabulatedAgent():
    
    def __init__(self, table):
        self.table = table
        self.name = 'tabulated'

    def lookupTable(self, value):
        return self.table.lookup(value)

    def convert(self, value):
        return sensorTable(binaryToDecimal(value))


class binaryTabulatedAgent(binaryAgent, tabulatedAgent):
    
    def __init__(self, Vref, gain, zero, bits, twosC, sensorTable):
        binaryAgent.__init__(self, Vref, gain, zero, bits, twosC, sensorTable)
        tabulatedAgent.__init__(self, sensorTable)
        self.name = 'binary tabulated'

    def convert(self, value):
        return self.lookupTable(self.binaryToDecimal(value))


class ASCIITabulatedAgent(ASCIIAgent, tabulatedAgent):

    def __init__(self, Vref, gain, zero, bits, twosC, sensorTable):
        binaryAgent.__init__(self, Vref, gain, zero, bits, twosC, sensorTable)
        tabulatedAgent.__init__(self, sensorTable)
        self.name = 'ASCII tabulated'

    def convert(self, value):
        return self.sensorTable(self.ASCIIToDecimal(value))

