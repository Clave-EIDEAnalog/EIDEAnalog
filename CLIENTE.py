import EIDEAnalog as EA

import facade as EGClient
EGUser = EGClient.EIDE.EIDEGraphics(1)

myBus = EA.ADS1115(0x48)
myAgent = EA.binaryAgent(5.0, 1, 0, 10, False)

currentValues = [0]

##while True:
##    myBus.singleShot()
##    while not(myBus.ready()):
##        pass
##    currentValues[0] = int(myBus.readConversion()/1000)
##    EGUser.EIDEGLoop(currentValues)


NTC_china = EA.sensor('ADS1115_NTC', myBus, 1, 'NTC_placa')
myBus.setChannelGain(NTC_china)
while True:
    myBus.singleShot()
    while not(myBus.ready()):
        pass
    currentValues[0] = NTC_china.readout(myBus.readConversion())
    EGUser.EIDEGLoop(currentValues)
    
