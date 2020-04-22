# Import EIDEAnalog.
import EIDEAnalog

instancedSensors = []

# Instance buses and sensors. Add them to list.
myBus  = EIDEAnalog.ADS1115(0x48)
NTC_china = EIDEAnalog.sensor('ADS1115_NTC', myBus, 1, name='NTC_placa')
T_Exterior = EIDEAnalog.sensor('LM35', myBus, 2, name='TE_LM35')
instancedSensors.append(NTC_china)
instancedSensors.append(T_Exterior)

myOtherBus  = EIDEAnalog.oneWire(19)
DS18B20_1 = EIDEAnalog.sensor('DS18B20', myOtherBus, 1, name='oW1')
DS18B20_2 = EIDEAnalog.sensor('DS18B20', myOtherBus, 2, name='oW2')
instancedSensors.append(DS18B20_1)
instancedSensors.append(DS18B20_2)

for i in instancedSensors:
    i.sensorBus.setChannelGain(i)
    i.sensorBus.singleShot()
    while not(i.sensorBus.ready()):
        pass
    print (i.name, "reads", i.readout(i.sensorBus.readConversion()))
         
EIDEAnalog.quit()
