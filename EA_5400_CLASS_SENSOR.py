# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEAnalog library (excerpt). Class sensor                                #
#                                                                           #
# Librería EIDEAnalog (extracto). Clase sensor                              #
# Ver 5.4.- Código de la clase sensor … en EIDEAnalog_ASI_SE_HIZO.pdf       #
# para más información (https://github.com/Clave-EIDEAnalog/DOCS)           #
#                                                                           #
# Copyright (c) 2020. Clave Ingenieros S.L.;                                #
# vicente.fombellida@claveingenieros.es                                     #
#                                                                           #
#############################################################################
class sensor():
    """ Sensor information and readout calculation """
 
    standardSensorsData = {
        'DS18B20':      ['DS18B20', 0.001, 0, 0, None],
        'LM35':         ['LM35', 100, 0, 1.0, None],
        'LM50':         ['LM50', 100, 0.5, 1.0, None],
        'rawVoltage' :  ['rawVoltage', 1, 0, 5.0, None],
        'ADS1115_NTC':  ['ADS1115_NTC', 1, 0, 3.3, 'ADS1115_NTC'],
        }
    # Agent selection dictionary
    calculationAgentDict = {
        'bNT': binaryAgent,         # Binary; not table
        'bT': binaryTabulatedAgent, # Binary; table
        'ANT': ASCIIAgent,          # ASCII; not table
        'AT': ASCIITabulatedAgent,  # ASCII; table
        }

    instancedSensors = []
    
    def __init__(self, tipo, device, canal, name=None, identificacion=None):

        self.name = name                                        # i.e. 'Hot water'
        self.ID = identificacion                                # i.e. '00000674869d'
        self.tipo = tipo                                        # i.e. 'DS18B20'
        self.sensorBus = device                                 # bus object
        self.channel = canal                                    # i.e. 1
        self.gain = float(sensor.standardSensorsData[tipo][1])  # i.e. 0.001
        self.zero = float(sensor.standardSensorsData[tipo][2])  # i.e. 0.0
        self.VMax = float(sensor.standardSensorsData[tipo][3])  # i.e. 2.0
        self.tableDefined = sensor.standardSensorsData[tipo][4]
        self.bits = self.sensorBus.bits                         # i.e. 16
        self.twosC = self.sensorBus.twosC                       
        self.sensorWizard()

        self.lastReadout = 0

# sensor ####################
    def sensorWizard(self):
        """ Assign sensor other data """
        # Search for reference voltage and index it.
        self.vRefPos = self.sensorBus.chooseVref(self.VMax)[0] + 1
        self.vRef = self.sensorBus.chooseVref(self.VMax)[1]
        # Instantiate table (if any).
        if self.tableDefined:
            self.table = sensorTable(self.tableDefined)
        else:
            self.table = None
        # Calculate and instance calculation agent
        key = ''
        if self.bits > 0: key = key + 'b'   # binary
        else: key = key + 'A'               # ASCII
        if self.table: key = key + 'T'      # Tabulated
        else: key = key + 'NT'              # Not table

        self.agent = sensor.calculationAgentDict[key](
            self.vRef, self.gain, self.zero, self.bits,
            self.twosC, self.table)

# sensor ####################
    def readout(self, value):
        """ Calculate readout """
        self.lastReadout = self.agent.convert(value)
        return self.lastReadout
