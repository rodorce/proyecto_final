# Clase que sirve para poder crear distintos bloques de memoria y cada uno con apuntadores respectivos
# a los tipos de datos y que ayudan a asignar una direccion virtual a la tabla de variables y constantes

class MemoryPointer:
    memoryType = ""
    start = 0
    intAddressPointer = 0
    floatAddressPointer = 0
    boolAddressPointer = 0
    stringAddressPointer = 0
    end = 0
    originalStart = 0

    def __init__(self, memoryType, start, intAddressPointer, floatAddressPointer, boolAddressPointer, stringAddressPointer, end):
        self.memoryType = memoryType
        self.start = start
        self.intAddressPointer = intAddressPointer
        self.floatAddressPointer = floatAddressPointer
        self.boolAddressPointer = boolAddressPointer
        self.stringAddressPointer = stringAddressPointer
        self.end = end
        self.originalStart = start

    def updateVirtualAddressPointer(self):
        if self.start < self.floatAddressPointer:
            self.intAddressPointer += 1
        elif self.start < self.boolAddressPointer:
            self.floatAddressPointer += 1
        elif self.start < self.stringAddressPointer:
            self.boolAddressPointer += 1
        elif self.start < end:
            self.stringAddressPointer += 1
        return self.start

    def getIntAddress(self):
        return self.intAddressPointer

    def getFloatAddress(self):
        return self.floatAddressPointer

    def getBoolAddress(self):
        return self.boolAddressPointer

    def getStringAddress(self):
        return self.stringAddressPointer

    def setStartPointer(self, type):
        if type == 'int':
            self.start = self.intAddressPointer
        elif type == 'float':
            self.start = self.floatAddressPointer
        elif type == 'string':
            self.start = self.stringAddressPointer

    def getAddressPointers(self, type):
        if type == 'int':
            return self.getIntAddress()
        elif type == 'float':
            return self.getFloatAddress()
        elif type == 'bool':
            return self.getBoolAddress()
        elif type == 'string':
            return self.stringAddressPointer()

    def resetPointers(self):
            self.intAddressPointer = self.originalStart
            self.floatAddressPointer = self.originalStart + 1000
            self.boolAddressPointer = self.originalStart + 2000
            self.stringAddressPointer = self.originalStart + 3000