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
        'GOTOF' : 8
    }
    memorySpace = [None] * 22000

    def __init__(self, quads, funcsDir, varsTable, constTable, globalTempsTable, localTempsTable):
        self.quads = quads
        self.funcsDir = funcsDir
        self.varsTable = varsTable
        self.constTable = constTable
        self.globalTempsTable = globalTempsTable
        self.localTempsTable = localTempsTable

    def debug_structs(self):
        for (idx, quad) in enumerate(self.quads):
            print(idx + 1, quad)
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
            # TRADUCIR CONSTANTES Y GUARDARLAS EN MEMORIA
            if quad[1] in self.constTable:
                self.saveDataInMemory(self.constTable[quad[1]],quad[1])
                quad[1] = self.constTable[quad[1]]
            if quad[2] in self.constTable:
                self.saveDataInMemory(self.constTable[quad[2]],quad[2])
                quad[2] = self.constTable[quad[2]]
            if quad[3] in self.constTable:
                self.saveDataInMemory(self.constTable[quad[3]],quad[3])
                quad[3] = self.constTable[quad[3]]
            #TRADUCIR TEMPORALES
            if quad[1] in self.globalTempsTable:
                quad[1] = self.globalTempsTable[quad[1]]
            if quad[2] in self.globalTempsTable:
                quad[2] = self.globalTempsTable[quad[2]]
            if quad[3] in self.globalTempsTable:
                quad[3] = self.globalTempsTable[quad[3]]

    def executeProgram(self):
        print(self.debug_structs())
        self.translate_quads()
        for (idx,quad) in enumerate(self.quads):
            print(quad)
        quads = self.quads
        cont = 0
        while cont < len(quads):
            if quads[cont][0] == 2:
                result = self.memorySpace[quads[cont][1]] + self.memorySpace[quads[cont][2]]
                self.memorySpace[quads[cont][3]] = result
            if quads[cont][0] == 1:
                self.memorySpace[quads[cont][3]] = self.memorySpace[quads[cont][1]]
            if quads[cont][0] == 3:
                result = self.memorySpace[quads[cont][1]] - self.memorySpace[quads[cont][2]]
                self.memorySpace[quads[cont][3]] = result
            if quads[cont][0] == 7:
                print(self.memorySpace[quads[cont][3]])
            if quads[cont][0] == 4:
                result = self.memorySpace[quads[cont][1]] * self.memorySpace[quads[cont][2]]
                self.memorySpace[quads[cont][3]] = result
            if quads[cont][0] == 5:
                result = self.memorySpace[quads[cont][1]] // self.memorySpace[quads[cont][2]]
                self.memorySpace[quads[cont][3]] = result
            if quads[cont][0] == 6:
                result = self.memorySpace[quads[cont][1]] < self.memorySpace[quads[cont][2]]
                self.memorySpace[quads[cont][3]] = result
            if quads[cont][0] == 8:
                if self.memorySpace[quads[cont][1]]:
                    cont = quads[cont][3] - 1
                    print('cont',cont)
            cont+=1

    def saveDataInMemory(self, dir, value):
        self.memorySpace[dir] = value