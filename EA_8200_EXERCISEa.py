# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEAnalog practising section                                             #
# File: EA_8200_EXERCISEa.py                                                #
#                                                                           #
# Archivo: EA_8200_EXERCISEa.py                                             #
# Librería EIDEAnalog (ejercicios de autoevaluación).                       #
# Consulte punto 8.2.- Uso con clases intermedias …                         #
# en EIDEAnalog_ASI_SE_HIZO.pdf (https://github.com/Clave-EIDEAnalog/DOCS)  #
#                                                                           #
# Copyright (c) 2020. Clave Ingenieros S.L.;                                #
# vicente.fombellida@claveingenieros.es                                     #
#                                                                           #
#############################################################################
import EIDEAnalog

class ADCBus_manager():
    busesDict = {'ADS1115': EIDEAnalog.ADS1115,
                 'oneWire': EIDEAnalog.oneWire}
    
    def __init__(self, project):
        self.sensorsCName = []
        self.sensorsType = []
        self.sensorsChannel = []
        self.sensorsName = []
        self.instancedSensors = []
        self.project = project       
        self.parseProject(self.project)
        self.instanceObjects()

    def parseProject(self, project):
        for i in project:
            if isinstance(i, list):
                # Sensor list
                self.sensorsCName.append(i[0])
                self.sensorsType.append(i[1])
                self.sensorsChannel.append(i[2])
                self.sensorsName.append(i[3])

    def instanceObjects(self):
        self.bus = ADCBus_manager.busesDict[self.project[0]](
            self.project[1])
        for contador, i in enumerate(self.sensorsCName):
            objeto = EIDEAnalog.sensor(self.sensorsType[contador],
                self.bus,
                self.sensorsChannel[contador],
                self.sensorsName[contador])
            self.instancedSensors.append(objeto)
            
    def readConversions(self):
        lecturas = []
        for i in self.instancedSensors:
            self.bus.setChannelGain(i)
            self.bus.singleShot()
            while not(self.bus.ready()):
                pass
            lectura = self.bus.readConversion()
            lecturas.append(i.readout(lectura))
        return lecturas

project1 = [
    'ADS1115', 0x48,
    ['NTC_china', 'ADS1115_NTC', 1, 'NTC_placa'],
    ['T_Exterior', 'LM35', 2, 'T_Exterior']
    ]

project3 = [
    'ADS1115', 0x49,
    ['NTC_china', 'ADS1115_NTC', 1, 'NTC_placa'],
    ['T_Exterior', 'LM50', 2, 'T_Exterior']
    ]

project2 = [
    'oneWire', 19,
    ['DS18B20_1', 'DS18B20', 1, 'DS18B20_1'],
    ['DS18B20_1', 'DS18B20', 2, 'DS18B20_1']
    ]

uno = ADCBus_manager(project1)
print (uno.readConversions())

dos = ADCBus_manager(project2)
print (dos.readConversions())

EIDEAnalog.quit()
