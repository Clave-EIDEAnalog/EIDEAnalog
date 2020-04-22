import smbus
i2c = smbus.SMBus(1)

import time

class ADS1115():

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

    def chooseVref(self, sensorMax):
        """ Return an ADC reference index and value """
        anterior = self.refVoltageList[0]
        for position, i in enumerate(self.refVoltageList):
            if sensorMax == i:
                return (position - 1, i)
            elif ((sensorMax < i) & (sensorMax > anterior)):
                return (position - 1, i)
            anterior = i        
        return (position - 1, anterior) 
     
    def swap(self, word):
        """ Swaps the two bytes of a word """
        valor = ((word&0xff00)>>8) | ((word&0x00ff)<<8)
        return valor

    def readWord(self, register):
        """Read word from ADS1115 register """
        valor = i2c.read_word_data(self.addr, register)
        valor = self.swap(valor)
        return valor

    def sendWordToConfReg(self, word):
        """ Send a word to the ADS1115 configuration register """
        # swap byte order 
        word = self.swap(word)
        i2c.write_word_data(self.addr, ADS1115.confReg, word)

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


myBus = ADS1115(0x48)
loops = 1000
myBus.setSPS(7)
myBus.setChannel(1)

start_time = time.time()
for i in range(loops):
    myBus.singleShot()
    while not(myBus.ready()):
        pass

total_time = time.time() - start_time
print ("Samples per second:", int((1/total_time)*loops))
