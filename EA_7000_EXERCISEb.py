import os

class sensorTable():
    """ Class for sensor tables """
    head = os.getcwd()
    tables = os.path.join(head, 'SENSOR_TABLES')

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

table = sensorTable('VAPOUR_PRESSURE')
values = [36.0, 62.5]
for i in values:
    print ('For', i, "table gives", table.lookup(i))
