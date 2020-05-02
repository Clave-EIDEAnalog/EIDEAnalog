# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEAnalog library (Complete library. Release 0.0)                        #
#                                                                           #
# Librería EIDEAnalog (Librería completa. Versión 0.0)                      #
# Ver EIDEAnalog_ASI_SE_HIZO.pdf                                            #
# para más información (https://github.com/Clave-EIDEAnalog/DOCS)           #
#                                                                           #
# Copyright (c) 2020. Clave Ingenieros S.L.;                                #
# vicente.fombellida@claveingenieros.es                                     #
#                                                                           #
#############################################################################

import sys, os
import time
import smbus
import serial

import smbus

import RPi.GPIO as GPIO

  

def quit():
    GPIO.cleanup()

class services():
    def __init__(self):
        self.i2c = smbus.SMBus(1)

        self.tablesFolder = 'SENSOR_TABLES'
 
        self.standardSensorsData = {
            'DS18B20':      ['DS18B20', 0.001, 0, 0, None],
            'LM35':         ['LM35', 100, 0, 1.0, None],
            'LM50':         ['LM50', 100, 0.5, 1.0, None],
            'rawVoltage' :  ['rawVoltage', 1, 0, 5.0, None],
            'ADS1115_NTC':  ['ADS1115_NTC', 1, 0, 3.3, 'ADS1115_NTC'],
            }
        
srv = services()

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


class ADCBus():
    """ Base class for ADC-bus devices """

    instancedBuses = []     

    def chooseVref(self, sensorMax):
        anterior = self.refVoltageList[0]
        for position, i in enumerate(self.refVoltageList):
            if sensorMax == i:
                return (position - 1, i)
            elif ((sensorMax < i) & (sensorMax > anterior)):
                return (position - 1, i)
            anterior = i
            
        return (position - 1, anterior)

    def setChannel(self, channel):
        pass
    
    def setChannelGain(self, sensor):
        pass

    def singleShot(self):
        pass

    def ready(self):
        pass

    def readConversion(self):
        pass


class ADS1115(ADCBus):

    tipo = 'ADS1115'
    bits = 16 
    twosC = True 
    refVoltageList = (0, 0.256, 1.024, 2.048, 4.096, 6.144)

    # Registers
    confReg = 0b00000001
    convReg = 0b00000000

    # Start conversion
    startConv    = 0b1000000000000000
    # “Done” bit
    done         = 0b1000000000000000

                                        #O|MUX|PGA|M|DRT|COMPR
    reset        = 0b0000010110000000   #0|000|010|1|100|00000
    # Start conversion
    startConv    = 0b1000000000000000   #1|000|000|0|000|00000
    # “Done” bit
    done         = 0b1000000000000000   #1|000|000|0|000|00000
    # Channel selection (Multiplexer)
    channelReset = 0b0000111111100000   #0|000|111|1|111|00000
    setChannel1  = 0b0100000000000000   #0|100|000|0|000|00000
    setChannel2  = 0b0101000000000000   #0|101|000|0|000|00000
    setChannel3  = 0b0110000000000000   #0|110|000|0|000|00000
    setChannel4  = 0b0111000000000000   #0|111|000|0|000|00000
    # Gain
    gainReset    = 0b0111000111100000   #0|111|000|1|111|00000
    gain_6_144   = 0b0000000000000000   #0|000|000|0|000|00000
    gain_4_096   = 0b0000001000000000   #0|000|001|0|000|00000
    gain_2_048   = 0b0000010000000000   #0|000|010|0|000|00000
    gain_1_024   = 0b0000011000000000   #0|000|011|0|000|00000
    gain_0_512   = 0b0000100000000000   #0|000|100|0|000|00000
    gain_0_256   = 0b0000101000000000   #0|000|101|0|000|00000
    # Samples per second
    SPSReset     = 0b0111111100000000   #0|111|111|1|000|00000
    SPS_8        = 0b0000000000000000   #0|000|000|0|000|00000
    SPS_16       = 0b0000000000100000   #0|000|000|0|001|00000
    SPS_32       = 0b0000000001000000   #0|000|000|0|010|00000
    SPS_64       = 0b0000000001100000   #0|000|000|0|011|00000
    SPS_128      = 0b0000000010000000   #0|000|000|0|100|00000
    SPS_250      = 0b0000000010100000   #0|000|000|0|101|00000
    SPS_475      = 0b0000000011000000   #0|000|000|0|110|00000
    SPS_860      = 0b0000000011100000   #0|000|000|0|111|00000

    setChannels = (
        (channelReset, setChannel1),
        (channelReset, setChannel2),
        (channelReset, setChannel3),
        (channelReset, setChannel4),
    )

    setSPSs = (
        (SPSReset, SPS_8),
        (SPSReset, SPS_16),
        (SPSReset, SPS_32),
        (SPSReset, SPS_64),
        (SPSReset, SPS_128),
        (SPSReset, SPS_250),
        (SPSReset, SPS_475),
        (SPSReset, SPS_860),
    )

    setGains = (
        (gainReset, gain_0_256),
        (gainReset, gain_0_512),
        (gainReset, gain_1_024),
        (gainReset, gain_2_048),
        (gainReset, gain_4_096),
        (gainReset, gain_6_144),
    )

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
        valor = srv.i2c.read_word_data(self.addr, register)
        valor = self.swap(valor)
        return valor

    def sendWordToConfReg(self, word):
        """ Send a word to the ADS1115 configuration register """
        # swap byte order 
        word = self.swap(word)
        srv.i2c.write_word_data(self.addr, ADS1115.confReg, word)

    def readConfig(self):
        """ Read config reg. """
        r = self.readWord(ADS1115.confReg)
        return r

    def programConfReg(self, lista):
        """ Sends a -programming- command to the ADS1115"""
        #Read config register
        valor = self.readConfig()
        # reset value by lista[0]
        valor = valor & lista[0]
        # Set value by lista[1]
        valor = valor | lista[1]
        self.sendWordToConfReg(valor)
        return valor

    def setSPS(self, option):
        """ Sets the "samples per second" parameter"""
        self.programConfReg(ADS1115.setSPSs[option])

    def setGain(self, option):
        """ Sets the "gain" parameter"""
        self.programConfReg(ADS1115.setGains[option])
        
    def setChannel(self, channel):
        """ Sets a channel -multiplexer-"""
        self.programConfReg(ADS1115.setChannels[channel - 1])

    def setChannelGain(self, sensor):
        """ Set the channel # -multiplexer- and gain """
        self.programConfReg(ADS1115.setChannels[sensor.channel - 1])
        self.setGain(sensor.vRefPos)

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


class oneWire(ADCBus):
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
        time.sleep(14)

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


class sensor():
    """ Sensor information and readout calculation """
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
        self.gain = float(srv.standardSensorsData[tipo][1])     # i.e. 0.001
        self.zero = float(srv.standardSensorsData[tipo][2])     # i.e. 0.0
        self.VMax = float(srv.standardSensorsData[tipo][3])     # i.e. 2.0
        self.tableDefined = srv.standardSensorsData[tipo][4]
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


class sensorTable():
    """ Class for sensor tables """
    head = os.getcwd()
    tables = os.path.join(head, srv.tablesFolder)

    def __init__(self, archivo):

        self.name = archivo.split(".")[0]
        self.table = []
        self.archivoPath = os.path.join(sensorTable.tables, self.name + '.txt')
        self.read(self.archivoPath)
        
        self.mapLen = len(self.table)
        self.mapMinimum = self.table[0][0]
        self.mapMaximum = self.table[len(self.table) - 1][0]
        self.sort()
        self.verify()

        self.position = -1

    def read(self, file):
        fichero = open(self.archivoPath, "r+")
        for linea in fichero:
            pointsList = (float(linea.split(",")[0]),
                float(linea.split(",")[1]))
            self.table.append(pointsList)
        fichero.close()

    def sort(self):
        self.table.sort()

    def verify(self):
        if self.mapLen < 4:
            raise EIDEError("", "Sensor table error: less than three points")
        for counter, i in enumerate(self.table):
            if counter == self.mapLen - 1:
                # Table top reached.
                return
            if i[0] == self.table[counter+1][0]:
                raise EIDEError("", "Sensor table error: double abcissa")

    def lookup(self, abcissa):
        """ Return ordinate for abcissa """
        return self.linearInterpolate(self.abcissaPoints(
            self.pointer(abcissa)), abcissa)
    
    def pointer(self, abcissa):
        """ Return position of equal or first smaller number  """        
        if abcissa < self.table[0][0]:
            # abcissa 'below' table.
            return 0
        for contador,i in enumerate(self.table):
            if i[0] > abcissa:
                return contador - 1
        return contador
            
    def abcissaPoints(self, pointer):        
        """ Return a list holding interpolation points """
        if pointer >= (self.mapLen - 1):
            # Point 'above' table.
            return (self.table[self.mapLen - 2],
                self.table[self.mapLen - 1])
        return (self.table[pointer],
                self.table[pointer + 1])
            
    def linearInterpolate(self, points, abcissa):
        """ Return a list holding interpolation points """
        x1 = points[0][0]
        y1 = points[0][1]
        x2 = points[1][0]
        y2 = points[1][1]
        m = (y2-y1)/(x2-x1)
        b = y2 - (x2/(x2-x1))*(y2-y1)
        return (m * abcissa + b)

