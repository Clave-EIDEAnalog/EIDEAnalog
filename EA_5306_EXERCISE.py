
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
    
