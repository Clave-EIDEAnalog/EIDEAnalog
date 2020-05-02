# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEAnalog practising section                                             #
# File: EA_5301_EXERCISEa.py                                                #
#                                                                           #
# Archivo: EA_5301_EXERCISEa.py                                             #
# Librería EIDEAnalog (ejercicios de autoevaluación).                       #
# Consulte punto 5.3.1.- Agente de cálculo ‘binario’ (binaryAgent) …        #
# en EIDEAnalog_ASI_SE_HIZO.pdf (https://github.com/Clave-EIDEAnalog/DOCS)  #
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


agent = binaryAgent(5.0, 1, 0, 10, False)
inputs = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]

for i in inputs:
    print ("input:", i, "output:", agent.convert(i))
    
