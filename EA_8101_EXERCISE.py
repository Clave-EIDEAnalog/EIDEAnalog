# Import EIDEAnalog.
import EIDEAnalog

# Instance bus and sensor.
myBus  = EIDEAnalog.ADS1115(0x48)
NTC_china = EIDEAnalog.sensor('ADS1115_NTC', myBus, 1, name='NTC_placa')

# Configure and trigger ADC. Wait for bus ready.
myBus.setChannel(1)
myBus.setGain(4)
myBus.singleShot()
while not(myBus.ready()):
	pass

# Read conversion. Convert and display it.
lectura = myBus.readConversion()
a_visualizar = NTC_china.readout(lectura)
print (a_visualizar)


# Instance sensor
T_Exterior = EIDEAnalog.sensor('LM35', myBus, 2, name='TE_LM35')

# Configure and trigger ADC. Wait for bus ready.
myBus.setChannel(2)
myBus.setGain(2)
myBus.singleShot()
while not(myBus.ready()):
	pass

# Read conversion. Convert and display it.
lectura = myBus.readConversion()
a_visualizar = T_Exterior.readout(lectura)
print (a_visualizar)

##########################################################
# Bus oneWire
##########################################################
# Instance bus and sensor.
myBus  = EIDEAnalog.oneWire(19)
DS18B20_1 = EIDEAnalog.sensor('DS18B20', myBus, 1, name='oW1')

# Configure and trigger ADC. Wait for bus ready.
myBus.setChannel(1)
myBus.singleShot()
while not(myBus.ready()):
	pass

# Read conversion. Convert and display it.
lectura = myBus.readConversion()
a_visualizar = DS18B20_1.readout(lectura)
print (a_visualizar)


# Instance sensor
DS18B20_2 = EIDEAnalog.sensor('DS18B20', myBus, 2, name='oW2')

# Configure and trigger ADC. Wait for bus ready.
myBus.setChannel(2)
myBus.singleShot()
while not(myBus.ready()):
	pass

# Read conversion. Convert and display it.
lectura = myBus.readConversion()
a_visualizar = DS18B20_2.readout(lectura)
print (a_visualizar)

EIDEAnalog.quit()
