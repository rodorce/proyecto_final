class VirtualMachine:
    quads = []
    funcsDir = []
    varsTable = {}
    globalTempsTable = {}
    localTempsTable = {}
    operatorCodes = {
        '=': 1,
        '+' : 2,
        '-' : 3,
        '*' : 4,
        '/' : 5,
        '<' : 6,
        "PRINT" : 7,
        'GOTOF' : 8,
        'GOTO' : 9,
        '==': 10,
        'Ver' : 11
    }
    memorySpace = [None] * 29999

    def __init__(self, quads, funcsDir, varsTable, constTable, globalTempsTable, localTempsTable):
        self.quads = quads
        self.funcsDir = funcsDir
        self.varsTable = varsTable
        self.constTable = constTable
        self.globalTempsTable = globalTempsTable
        self.localTempsTable = localTempsTable

    def debug_structs(self):
        for (idx, quad) in enumerate(self.quads):
            print(idx, quad)
        print("funcsDir", self.funcsDir)
        print("varsTable", self.varsTable)
        print("constTable", self.constTable)
        print("global temps table", self.globalTempsTable)
        print("local temps table", self.localTempsTable)

    def reduce_vars_table(self):
        globalVarsTable = {}
        for var in self.varsTable[self.funcsDir[0]["name"]]:
            print(var, self.varsTable[self.funcsDir[0]["name"]][var]["dirV"])
            globalVarsTable[var]= self.varsTable[self.funcsDir[0]["name"]][var]["dirV"]
        return globalVarsTable

    def translate_quads(self):
        globalVarsTable = self.reduce_vars_table()
        for quad in self.quads:
            # TRADUCIR CONSTANTES Y GUARDARLAS EN MEMORIA
            if quad[1] in self.constTable:
                self.saveDataInMemory(self.constTable[quad[1]], quad[1])
                quad[1] = self.constTable[quad[1]]
            if quad[2] in self.constTable:
                self.saveDataInMemory(self.constTable[quad[2]], quad[2])
                quad[2] = self.constTable[quad[2]]
            if quad[3] in self.constTable:
                if quad[0] == 'GOTO' or quad[0] == 'GOTOF':
                    print('entra')
                else:
                    self.saveDataInMemory(self.constTable[quad[3]], quad[3])
                    quad[3] = self.constTable[quad[3]]
            # TRADUCIR OPERADORES
            if quad[0] in self.operatorCodes:
                quad[0] = self.operatorCodes[quad[0]]
            # TRADUCIR VARIABLES GLOBALES
            if quad[1] in globalVarsTable:
                quad[1] = globalVarsTable[quad[1]]
            if quad[2] in globalVarsTable:
                quad[2] = globalVarsTable[quad[2]]
            if quad[3] in globalVarsTable:
                quad[3] = globalVarsTable[quad[3]]
            #TRADUCIR TEMPORALES GLOBALES
            if quad[1] in self.globalTempsTable:
                quad[1] = self.globalTempsTable[quad[1]]
            if quad[2] in self.globalTempsTable:
                quad[2] = self.globalTempsTable[quad[2]]
            if quad[3] in self.globalTempsTable:
                quad[3] = self.globalTempsTable[quad[3]]
            # TRADUCCION DE POINTERS TEMPORALES GLOBALES
            if type(quad[1]) == str and quad[1] != "" and quad[1][1:len(quad[1])-1] in self.globalTempsTable:
                quad[1] = "(" + str(self.globalTempsTable[quad[1][1:len(quad[1])-1]]) + ")"
            if type(quad[2]) == str and  quad[2] != "" and quad[2][1:len(quad[2])-1] in self.globalTempsTable:
                quad[2] = "(" + str(self.globalTempsTable[quad[2][1:len(quad[2])-1]]) + ")"
            if type(quad[3]) == str and quad[3] != "" and quad[3][1:len(quad[3])-1] in self.globalTempsTable:
                quad[3] = "(" + str(self.globalTempsTable[quad[3][1:len(quad[3])-1]]) + ")"

    def verifyIfPointer(self, value):
        if type(value) == str and len(value) > 0 and value[0] == "(":
            dir = int(value[1:len(value) - 1])
            return self.memorySpace[dir]
        else:
            return value

    def executeProgram(self):
        print(self.debug_structs())
        self.translate_quads()
        for (idx,quad) in enumerate(self.quads):
            print(idx, quad)
        quads = self.quads
        cont = 0
        while cont < len(quads):
            q1 = self.verifyIfPointer(quads[cont][1])
            q2 = self.verifyIfPointer(quads[cont][2])
            q3 = self.verifyIfPointer(quads[cont][3])
            if quads[cont][0] == 2:
                result = self.memorySpace[q1] + self.memorySpace[q2]
                self.memorySpace[q3] = result
            elif quads[cont][0] == 1:
                self.memorySpace[q3] = self.memorySpace[q1]
            elif quads[cont][0] == 3:
                result = self.memorySpace[q1] - self.memorySpace[q2]
                self.memorySpace[q3] = result
            elif quads[cont][0] == 7:
                print(self.memorySpace[q3])
            elif quads[cont][0] == 4:
                result = self.memorySpace[q1] * self.memorySpace[q2]
                self.memorySpace[q3] = result
            elif quads[cont][0] == 5:
                result = self.memorySpace[q1] // self.memorySpace[q2]
                self.memorySpace[q3] = result
            elif quads[cont][0] == 6:
                result = not self.memorySpace[q1] < self.memorySpace[q2]
                self.memorySpace[q3] = result
            elif quads[cont][0] == 8:
                if not self.memorySpace[q1]:
                    cont = q3 - 1
            elif quads[cont][0] == 9:
                cont = q3 - 1
            elif quads[cont][0] == 10:
                result = self.memorySpace[q1] == self.memorySpace[q2]
                self.memorySpace[q3] = result
            elif quads[cont][0] == 11:
                pass
            cont+=1

    def saveDataInMemory(self, dir, value):
        self.memorySpace[dir] = value