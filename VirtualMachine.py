class VirtualMachine:
    #Vars to save Context of functions/params and returns
    pContext = []
    paramsToSend = {}
    returns = []

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
        'Ver' : 11,
        '>' : 12,
        'GOSUB' : 13,
        'ENDFUNC' : 14,
        'PARAMETRO' : 15,
        'RETURN' : 16,
        'RETURNASSIGN' : 17,
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
        #Context variables
        global pContext
        global paramsToSend
        self.pContext.append({'quadToReturn': 0})#just to save the same key as in funcs
        #print(self.debug_structs())
        #self.translate_quads()
        for (idx,quad) in enumerate(self.quads):
            print(idx, quad)
        quads = self.quads
        cont = 0
        while cont < len(quads):
            q1 = self.verifyIfPointer(quads[cont][1])
            q2 = self.verifyIfPointer(quads[cont][2])
            q3 = self.verifyIfPointer(quads[cont][3])
            if quads[cont][0] == 2:#+
                #print("+ ", self.memorySpace[q1], " ", self.memorySpace[q2])
                result = self.memorySpace[q1] + self.memorySpace[q2]
                self.writeInMemory(q3, result)
                #self.memorySpace[q3] = result
            elif quads[cont][0] == 1:
                self.writeInMemory(q3, self.memorySpace[q1])
                #self.memorySpace[q3] = self.memorySpace[q1]
            elif quads[cont][0] == 3:
                result = self.memorySpace[q1] - self.memorySpace[q2]
                self.writeInMemory(q3, result)
                #self.memorySpace[q3] = result
            elif quads[cont][0] == 7:#PRINT
                print(self.memorySpace[q3])
            elif quads[cont][0] == 4:#*
                result = self.memorySpace[q1] * self.memorySpace[q2]
                self.writeInMemory(q3, result)
                #self.memorySpace[q3] = result
            elif quads[cont][0] == 5:
                result = self.memorySpace[q1] // self.memorySpace[q2]
                self.writeInMemory(q3, result)
                #self.memorySpace[q3] = result
            elif quads[cont][0] == 6:
                result = not self.memorySpace[q1] < self.memorySpace[q2]
                self.writeInMemory(q3, result)
                #self.memorySpace[q3] = result
            elif quads[cont][0] == 12:
                result = not self.memorySpace[q1] > self.memorySpace[q2]
                self.writeInMemory(q3, result)
                #self.memorySpace[q3] = result
            elif quads[cont][0] == 8:#GOTOF
                if not self.memorySpace[q1]:
                    cont = q3 - 1
            elif quads[cont][0] == 9:
                cont = q3 - 1
            elif quads[cont][0] == 10:#==
                result = self.memorySpace[q1] == self.memorySpace[q2]
                self.writeInMemory(q3, result)
                #self.memorySpace[q3] = result
            elif quads[cont][0] == 11:
                #VERIFICA RANGO ARREGLO - PENDIENTE
                pass
            elif quads[cont][0] == 13:#GOSUB
                #delete current local memory reigsters
                for i in list(range(4000)):
                    self.memorySpace[i+5000] = None #reset register no None
                
                print("previous context: ", self.pContext)
                self.pContext.append({'quadToReturn': cont + 1}) #guardar en nuevo contexto, quad a regresar
                #search for func name
                for func in self.funcsDir:
                    if func["name"] == quads[cont][1]:
                        cont = func["startFunc"]-1#goto func start
                        if(func['paramSize'] != len(self.paramsToSend)):
                            print("Error en numero de parametros")
                        else:
                            i = 0
                            print(self.paramsToSend)
                            while(i < len(self.paramsToSend)):
                                if func['param'][i] == "int":
                                    self.writeInMemory(5001+i, self.paramsToSend[i])#param as key and cont
                                else:
                                    self.writeInMemory(6001+i, self.paramsToSend[i])#param as key and cont
                                i +=1
                                #add values to their respected address in the new function
                            self.paramsToSend.clear()
            elif quads[cont][0] == 14:#ENDFUNC
                cont = self.pContext[len(self.pContext) - 1]['quadToReturn'] - 1 #Regresar a cuadruplo guardado en pContext(pero a uno previo por el cont++ de abajo)
                self.pContext.pop()#delete actual context
                for item in self.pContext[len(self.pContext)-1]:#guarda en memoria toods los registros del contexto previo
                    if item != 'quadToReturn':
                        self.saveDataInMemory(item, self.pContext[len(self.pContext)-1][item])#save in that address the saved value
                # PENDIENTE CHECAR EL CAMBIO DE CONTEXTO
            elif quads[cont][0] == 15:#PARAMETRO
                #constant 0 no translated#nvm
                if q3 == 0:
                    self.paramsToSend[0] = self.getFromMemory(q1)
                else:
                    self.paramsToSend[self.getFromMemory(q3)] = self.getFromMemory(q1)#key->num de param, value->valor para ese param
            elif quads[cont][0] == 16:#RETURN
                #Save value en pila returns, por que se limpiara memoria del scope actual
                self.returns.append(self.getFromMemory(q3))
                # print("Dir 5000: ", self.getFromMemory(5000))
                # print("Dir 5001: ", self.getFromMemory(5001))
                # print("Dir 5002: ", self.getFromMemory(5002))
                # print("Dir 5003: ", self.getFromMemory(5003))
                # print("Dir 5004: ", self.getFromMemory(5004))
                # print("Dir 5005: ", self.getFromMemory(5005))
            elif quads[cont][0] == 17: #RETURNASSIGN
                #save the data received in the expected temp var
                if len(self.returns) > 0:
                    self.writeInMemory(q3,self.returns.pop()) #last saved return
                else:
                    #no returns
                    #print("Return error, no value")
                    #debug mode return default 14
                    self.writeInMemory(q3, 14)

            cont+=1
    def saveDataInMemory(self, dir, value):
        self.memorySpace[dir] = value

    def writeInMemory(self, dir, value):
        global pContext
        self.pContext[len(self.pContext)-1][dir] = value #GUARDAR VALOR DE MEMORIA EN CONTEXTO
        self.memorySpace[dir] = value #GUARDAR A MEMORIA REAL
    
    def getFromMemory(self, dir):
        return self.memorySpace[dir]#return the value from that address

