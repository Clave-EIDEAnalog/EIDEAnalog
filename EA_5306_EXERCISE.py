# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEAnalog practising section                                             #
# File: EA_5306_EXERCISE.py                                                 #
#                                                                           #
# Archivo: EA_5306_EXERCISE.py                                              #
# Librería EIDEAnalog (ejercicios de autoevaluación).                       #
# Consulte punto 5.3.6.- Familia de clases agente de cálculo …              #
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

class decibelsAgent(calculationAgent):
    
    def __init__(self, Vref, gain, zero, bits, twosC, table=None):
        calculationAgent.__init__(self, Vref, gain, zero, bits, twosC, None)
        self.name = 'binary'

    def decibelsCalc(self, value):
        value = (2.71**value - self.Vref) * self.gain
        return value

    def convert(self, value):
        return self.decibelsCalc(value)


agent = decibelsAgent(.9, 4.2, 0, 0, False)

for i in range(0, 20, 1):
    print ("input:", i/10, "output:", int(agent.convert(i/10)))
    
