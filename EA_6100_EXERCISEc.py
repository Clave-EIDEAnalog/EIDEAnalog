# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEAnalog practising section                                             #
# File: EA_6100_EXERCISEc.py                                                #
#                                                                           #
# Archivo: EA_6100_EXERCISEc.py                                             #
# Librería EIDEAnalog (ejercicios de autoevaluación).                       #
# Consulte punto 6.1.- Clase oneWire.                                       #
# en EIDEAnalog_ASI_SE_HIZO.pdf (https://github.com/Clave-EIDEAnalog/DOCS)  #
#                                                                           #
# Copyright (c) 2020. Clave Ingenieros S.L.;                                #
# vicente.fombellida@claveingenieros.es                                     #
#                                                                           #
#############################################################################
import time
import os
import RPi.GPIO as GPIO

# oneWire ##############################################################
class oneWire():
    """ Class to implement a 1wire bus with DS18B20 sensors """

    tipo = 'oneWire'
    refVoltageList = [0, 9999]
    bits = 0 
    twosC = False 

    baseDirectory = "/sys/bus/w1/devices/" 
    folderPrefix = '28-'
    sensorInfoFile = 'w1_slave'

    def __init__(self, pin, ordinal=0, name=None):
        self.ordinal = ordinal
        self.name = name
        self.initPin(pin)
        # Get sensors info.
        self.sensorsData = self.sensorsID()

        # 1st channel selected by default.
        self.setChannel(1)

    def initPin(self, pin):
        """ Set passed pin as Vcc """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)
        time.sleep(1)

    def sensorsID(self):
        """ Construct and return a list with the sensors info. """
        # Read base folder contents.
        folders = os.listdir(oneWire.baseDirectory)
        sensorsData = []
        for folder in folders:
            if not(oneWire.folderPrefix in folder):
                pass
            else:
                sensor = folder[len(oneWire.folderPrefix)-len(folder):]
                sensorsData.append(sensor)
        return sensorsData

    def getIDs(self):
        """ Return a list with the sensors ID """
        return self.sensorsData

    def setChannel(self, channel):
        """ Sets the channel for next 'readConversion()' """
        self.channel = channel
        self.currentChannelID = self.sensorsData[channel-1]

    def setChannelGain(self, sensor):
        """ Sets a channel """
        self.setChannel(sensor.channel)

    def ready(self):
        """ Return true if new data available"""
        # oneWire ALWAYS has data available (see class comment)
        return True
        
    def readConversion(self):
        """ Returns the conversion for current channel """
        sensorFile = os.path.join(oneWire.baseDirectory,
            (oneWire.folderPrefix+self.currentChannelID))
        sensorFile = os.path.join(sensorFile, oneWire.sensorInfoFile)
        with open(sensorFile, "r") as f:
            data = f.readlines()
            return float(data[1].split("=")[1])

    def readChannelByID(self, ID):
        channel = myBus.sensorsData.index(ID)
        self.setChannel(channel)
        return self.readConversion()


myBus = oneWire(19)
channelID = myBus.sensorsData[0]  # Select first probe
print (int(myBus.readChannelByID(channelID)/1000))
