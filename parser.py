# Yacc example

import sys
import ply.yacc as yacc
import VirtualMachine
from lexer import tokens
from MemoryPointer import MemoryPointer

# Directorio de funciones y tablas de variables
funcsDir = []  # {'name': "funcName", 'type': "int/float/void/programType", 'kind': "program/func"}
varsTables = {}  # {'tableName': {'varName': {'type': "int/float", 'kind': "local/global"}}}
# funcs/vars pre-data to save
name = []
tipo = "-1"
varsTipo = []  # multiple vars with same type ex: int a,b,c,d;

# current active func(to save vars in its table)
# Directorio de funciones y tablas de variables
funcsDir = []  # {'name': "funcName", 'type': "int/float/void/programType", 'kind': "program/func"}
varsTables = {}  # {'tableName': {'varName': {'type': "int/float", 'kind': "local/global"}}}
# funcs/vars pre-data to save
name = []
tipo = "-1"
varsTipo = []  # multiple vars with same type ex: int a,b,c,d;

# current active func(to save vars in its table)
activeFuncTable = "none"  # global should be outside of any function
activeScope = "global" #Variable para validar el scope actual
pOperators = [] #pila operadores para expresiones
pOperands = [] #pila operandos para expresiones
pTypes = [] #pila tipos para expresiones
pAssigns = [] #pila para manejar valores pendientes a asignacion
pAssignsTypes = [] #pila para manejar los tipos de los operandos pendientes en pila assigns
pCompOperands = [] #pila para operandos de expresiones comparativas
pCompOperators = [] #pila para operadores de expresiones comparativas
pCompTypes = [] #pila para tipos en expresiones comparativas
quads = [] #lista de cuaddruplos
quadCont = 1 #contador para temporales
contTempLocal = 0
contTempGlobal = 0
pJumps = []#pila saltos
tempsCont = 0 # Limite inferior
paramCounter = 0
paramPointer = 0
#pointers para asignar memorias virtuales
globalMemory = MemoryPointer("global",1000, 1000, 2000, 3000, 4000, 4999)
localMemory = MemoryPointer("local", 5000, 5000, 6000, 7000, 8000, 8999)
tempMemoryGlobal = MemoryPointer("temporal global", 9000, 9000, 10000, 11000, 12000, 12999)
tempMemoryLocal = MemoryPointer("temporal local", 13000, 13000, 14000, 15000, 16000, 17999)
constantsMemory = MemoryPointer("constant", 18000, 18000, 19000, 20000, 21000, 21999)
globalTempsTable = {}#tabla para guardar temporales globales
localTempsTable = {}#tabla para guardar temporales locales
constTable = {}#tabla de constantes
#Cubo semantico para validación semántica de tipos
#2 niveles para tipos de operandos y el tercero para el operador
#cada casilla almacena el resultado de la operacion entre esos tipos
semanticCube = {
    'int': {
        'float': {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '<': 'error',
            '>': 'error',
            '=': 'error'
        },
        'int': {
            '+': 'int',
            '-': 'int',
            '*': 'int',
            '/': 'int',
            '<': 'bool',
            '>': 'bool',
            '==': 'bool',
            '=': 'int'
        },
        'void': {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '<': 'error',
            '>': 'error',
            '=': 'error'
        }
    },
    'float': {
        'int': {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '<': 'error',
            '>': 'error',
            '=': 'error'
        },
        'float': {
            '+': 'float',
            '-': 'float',
            '/': 'float',
            '*': 'float',
            '<': 'bool',
            '>': 'bool',
            '==': 'bool',
            '=': 'float'
        },
        'void': {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '<': 'error',
            '>': 'error',
            '=': 'error'
        }
    },
    'void' :  {
        'int': {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '<': 'error',
            '>': 'error',
            '=': 'error'
        },
        'float' : {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '<': 'error',
            '>': 'error',
            '=': 'error'
        },
        'void' : {
            '+': 'error',
            '-': 'error',
            '*': 'error',
            '/': 'error',
            '<': 'error',
            '>': 'error',
            '=': 'error'
        }
    }
}

def p_PROGRAMA(p):
    '''PROGRAMA : programType SAVEPROGID semicolon main qpMainJump BLOQUE qpEnd
                | programType SAVEPROGID semicolon VARS main qpMainJump BLOQUE qpEnd
                | programType SAVEPROGID semicolon FUNCS main qpMainJump BLOQUE qpEnd
                | programType SAVEPROGID semicolon VARS FUNCS main qpMainJump BLOQUE qpEnd
    '''
    print(globalTempsTable)
    p[0] = 'COMPILA'

def p_qpMainJump(p):
    '''qpMainJump : empty'''
    global quads
    global funcsDir
    global activeScope
    quads[0].append(len(quads))
    #change active scope to global
    activeScope = "global"

def p_qpEnd(p):
    '''qpEnd : empty'''
    quads.append(["END", "", "", ""])

#Particion de la gramática, para guardar id de programa
def p_SAVEPROGID(p):
    '''SAVEPROGID : id'''
    global activeFuncTable
    global activeScope
    # save program id to funcsDir
    funcsDir.append({'name': p.__getitem__(1), 'type': "programType", 'kind': "program"})
    # create empty program varsTable(global vars)
    varsTables[p.__getitem__(1)] = {}
    # set activeScope global
    activeFuncTable = p.__getitem__(1)
    activeScope = "global"
    # INICIAMOS EL GO TO MAIN
    quads.append(["GOTO", "", ""])

#Auxiliar de regla de declaracion de variables
def p_MOREVARS(p):
    '''MOREVARS : VARS
                | empty'''

#Regla de declaracion de variables
def p_VARS(p):
    '''VARS : TIPO VARSAUX semicolon MOREVARS'''

# def p_VARSAUX(p):
#     '''VARSAUX : id VARSCOMMA
#                | id ARRAYDIMENSION ARRAYDIMENSION VARSCOMMA semicolon'''
#Regla para seguir declarando variables o salir de la declaración de variables
def p_VARSCOMMA(p):
    '''VARSCOMMA : comma VARSAUX
                 | empty'''
    global name
    global tipo
    global activeFuncTable
    global varsTipo

#Regla para declaración de funciones
def p_FUNCS(p):
    '''FUNCS : function FUNCTIPO SAVEFUNCID leftParenthesis FUNCPARAM rightParenthesis leftBracket qpFuncsPN5 FUNCSVARS qpFuncsPN5Pt2 qpFuncsPN6 FUNCSESTATUTOS return FUNCEXP semicolon qpFuncsPN7 PNRIGHTBTACKETFUNC MOREFUNCS'''

#Regla auxiliar para seguir declarando más funciones o salir de declaración de funciones
# to acept more than one func
def p_MOREFUNCS(p):
    '''MOREFUNCS : FUNCS
                 | empty'''

#Particion de regla, para marcar cambio de scope y borrar tabla de variables
def p_PNRIGHTBTACKETFUNC(p):
    '''PNRIGHTBTACKETFUNC : rightBracket'''
    global activeFuncTable
    global funcsDir
    global quads
    global localTempsTable
    print(varsTables)
    # ANTES DE QUE SE ELIMINE LA TABLA DE VARIABLES DE ESTA FUNCION
    print(funcsDir)
    startOfFunc = funcsDir[len(funcsDir)-1]["startFunc"] - 1
    for i in range(startOfFunc, len(quads)-1):
        q1, hasParenthesis1 = verifyIfPointer(quads[i][1])
        q2, hasParenthesis2 = verifyIfPointer(quads[i][2])
        q3, hasParenthesis3 = verifyIfPointer(quads[i][3])
        if quads[i][1] in varsTables[activeFuncTable]:
            quads[i][1] = varsTables[activeFuncTable][quads[i][1]]["dirV"]
        if quads[i][2] in varsTables[activeFuncTable]:
            quads[i][2] = varsTables[activeFuncTable][quads[i][2]]["dirV"]
        if quads[i][3] in varsTables[activeFuncTable]:
            quads[i][3] = varsTables[activeFuncTable][quads[i][3]]["dirV"]
        #TRADUCIR TEMPORALES LOCALES
        if q1 in localTempsTable:
            quads[i][1] = localTempsTable[q1]
            if hasParenthesis1:
                quads[i][1] = "(" + str(localTempsTable[q1]) + ")"
        if q2 in localTempsTable:
            quads[i][2] = localTempsTable[q2]
            if hasParenthesis2:
                quads[i][2] = "(" + str(localTempsTable[q2]) + ")"
        if q3 in localTempsTable:
            quads[i][3] = localTempsTable[q3]
            if hasParenthesis3:
                quads[i][3] = "(" + str(localTempsTable[q3]) + ")"
    #LIMPIAR POINTERS DE MEMORIA VIRTUAL LOCAL
    localMemory.resetPointers()
    localTempsTable = {}
    varsTables.pop(activeFuncTable)
    activeFuncTable = "global"

#Particion de regla, para guardar id
def p_SAVEFUNCID(p):
    '''SAVEFUNCID : id'''
    # Punto neuralgico 1 para las funciones donde se almacena el nombre de la funcion, y su tipo.
    global name
    global tipo
    global activeFuncTable
    global activeScope
    name.append(p.__getitem__(1))  # pre-save the id
    if name[0] not in funcsDir:
        # save in funcsDir
        funcsDir.append({'name': name[0], 'type': tipo, 'kind': "func", "param": [], "paramSize": 0})
        # create empty func varsTable????
        varsTables[name[0]] = {}
        # set current func as active varsTable and scope
        activeFuncTable = name[0]
        activeScope = "local"
        # clear the temp vars
        name.clear()
        tipo = "-1"
    else:
        print("Error duplicated func id")

#Particion regla tipo, para guardar tipo de funcion
def p_FUNCTIPO(p):
    '''FUNCTIPO : TIPO 
                | void'''
    global tipo
    if (p.__getitem__(1) == "void"):  # pre-save the func type
        tipo = "void"

#Regla para parametros de declaración de función
def p_FUNCPARAM(p):
    '''FUNCPARAM : PARAM PARAMSCOMMA'''

#Regla auxiliar de funcparam, para agregar más parametros o salir de regla
def p_PARAMSCOMMA(p):
    '''PARAMSCOMMA : comma FUNCPARAM 
                    | empty'''

#Regla para declaración de variables dentro de una función
def p_FUNCSVARS(p):
    '''FUNCSVARS : VARS FUNCSVARS
                 | empty'''

#Regla para acotar los estatutos validos para una función
def p_FUNCSESTATUTOS(p):
    '''FUNCSESTATUTOS : ESTATUTO FUNCSESTATUTOS
                     | empty'''

#Regla para acotar las expresiones validas en una función
def p_FUNCEXP(p):
    '''FUNCEXP : EXPR 
               | empty'''
    # Return cuadruplo
    global quads
    global pOperands
    global pTypes
    quads.append(["RETURN", "","",pOperands.pop()])
    pTypes.pop()

#Regla para definir un bloque
def p_BLOQUE(p):
    '''BLOQUE : leftBracket BLOQESTATUTO rightBracket'''

#Regla para estatutos
def p_BLOQESTATUTO(p):
    '''BLOQESTATUTO : ESTATUTO BLOQESTATUTO 
                    | empty'''

#Regla para definir tipo de dato
def p_TIPO(p):
    '''TIPO : intType
           | floatType'''
    global tipo
    tipo = p.__getitem__(1)  # pre-save the var type

#Particion de regla funcparam, para guardar tipo y id de parametro
def p_PARAM(p):
    '''PARAM : TIPO id'''
    global name
    global tipo
    global activeFuncTable
    name.clear()
    name.append(p.__getitem__(2))  # pre-save the id
    # if id not in current funcTable add it
    if name[0] not in varsTables[activeFuncTable]:
        # add var id(name) to activeFuncTable
        localMemory.setStartPointer(tipo)
        localMemory.updateVirtualAddressPointer()
        varsTables[activeFuncTable][name[0]] = {'type': tipo, 'kind': "local", "dirV": localMemory.getAddressPointers(tipo)}
        # clear the temp vars
        name.clear()
        # Punto neuralgico 3 donde se agrega el tipo de cada parametro en el directorio de funciones.
        funcsDir[len(funcsDir) - 1]["param"].append(tipo)
        #Punto neuralgico 4 donde se inserta el numero de parametros de la funcion
        funcsDir[len(funcsDir)-1]["paramSize"]+=1

        tipo = "-1"
    else:
        print("Error duplicated param var id")

#Regla auxiliar de variables para guardar id
def p_VARSAUX(p):
    '''VARSAUX : VARSAUXID ARRAYDIMENSION ARRAYDIMENSION qpArrPN7 VARSCOMMA'''

#Regla para definir estructura del indexamiento de una dimensión
def p_VARSAUXID(p):
    '''VARSAUXID : id'''
    global name
    global tipo
    global activeFuncTable
    global varsTipo
    global globalMemory
    global scopeKey
    # Punto neuralgico 1 de arreglos que a su vez es usado para tambien definir una variable simple.
    name.append(p.__getitem__(1))  # pre-save the id
    varsTipo.append(tipo)
    scopeKey = activeFuncTable
    # if id not in current funcTable add it
    for item in name:
        if item not in varsTables[activeFuncTable]:
            # add var id(item) to activeFuncTable (if it is global make var kind global)
            if activeScope != "global":
                varsTables[activeFuncTable][item] = {'type': varsTipo[0], 'kind': "local", "isArray": False}
                if varsTipo[0] == 'int':
                    localMemory.setStartPointer(varsTipo[0])
                    localMemory.updateVirtualAddressPointer()
                    varsTables[activeFuncTable][item] = {'type': varsTipo[0], 'kind': "global",
                                                         "dirV": localMemory.getIntAddress(), "isArray": False,
                                                         "arrDims": []}
                elif varsTipo[0] == "float":
                    localMemory.setStartPointer(varsTipo[0])
                    localMemory.updateVirtualAddressPointer()
                    varsTables[activeFuncTable][item] = {'type': varsTipo[0], 'kind': "global",
                                                         "dirV": localMemory.getFloatAddress(), "isArray": False,
                                                         "arrDims": []}
            else:
                if varsTipo[0] == 'int':
                    globalMemory.setStartPointer(varsTipo[0])
                    globalMemory.updateVirtualAddressPointer()
                    varsTables[activeFuncTable][item] = {'type': varsTipo[0], 'kind': "global",
                                                         "dirV": globalMemory.getIntAddress(), "isArray": False,
                                                         "arrDims": []}
                elif varsTipo[0] == "float":
                    globalMemory.setStartPointer(varsTipo[0])
                    globalMemory.updateVirtualAddressPointer()
                    varsTables[activeFuncTable][item] = {'type': varsTipo[0], 'kind': "global",
                                                         "dirV": globalMemory.getFloatAddress(), "isArray": False,
                                                         "arrDims": []}
            name.remove(item)
            varsTipo.pop(0)
        else:
            print("Error duplicated var id")

def p_ARRAYDIMENSION(p):
    '''ARRAYDIMENSION : leftSqBracket qpArrPN6 qpArrPN2 qpArrPN3 intArrDim rightSqBracket
                    | empty'''

def p_qpArrPN2(p):
    '''qpArrPN2 : empty'''
    global varsTables
    global scopeKey
    last_key = list(varsTables[scopeKey].keys())[-1]
    varsTables[scopeKey][last_key]["isArray"] = True

def p_qpArrPN3(p):
    '''qpArrPN3 : empty'''
    global varsTables
    global dim
    global scopeKey
    dim += 1
    last_key = list(varsTables[scopeKey].keys())[-1]
    varsTables[scopeKey][last_key]["arrDims"].append({"LI": 0, "LS": 0, "M": 0})

# def p_qpArrPN4(p):
#     '''qpArrPN4 : empty'''
#     global varsTables
#     global scopeKey
#     last_key = list(varsTables[scopeKey].keys())[-1]
#     dim = len(varsTables[scopeKey][last_key]["arrsDims"] - 1)
#     varsTables[scopeKey][last_key]["arrsDims"][dim]["LI"] = 0

def p_qpArrPN6(p):
    '''qpArrPN6 : empty'''
    # MISMA FUNCIONALIDAD QUE EN EL PUNTO NEURALGICO 3

def p_qpArrPN7(p):
    '''qpArrPN7 : empty'''
    global varsTables
    global scopeKey
    global r
    last_key = list(varsTables[scopeKey].keys())[-1]
    if varsTables[scopeKey][last_key]["isArray"] == True:
        varsTables[scopeKey][last_key]["size"] = r
        for item in varsTables[scopeKey][last_key]["arrDims"]:
            item["M"] = r // (item["LS"] - item["LI"] + 1)
            r = item["M"]
        r = 1


def p_intArrDim(p):
    '''intArrDim : int'''
    # PUNTO NEURALGICO 5 - Se guarda el limite superior.
    global varsTables
    global scopeKey
    global r
    last_key = list(varsTables[scopeKey].keys())[-1]
    varsTables[scopeKey][last_key]["arrDims"][dim-1]["LS"] = p[1]
    limSup = varsTables[scopeKey][last_key]["arrDims"][dim-1]["LS"]
    limInf = varsTables[scopeKey][last_key]["arrDims"][dim-1]["LI"]
    r = (limSup - limInf + 1) * r

#Regla estatuto
def p_ESTATUTO(p):
    '''ESTATUTO : ASSIGN 
                | PRINT
                | COND
                | LLAMADAVOID
                | CICLO'''


#Regla para definir estructura de una Variable dimensionada y simple
def p_VARIABLE(p):
    '''VARIABLE : qpExpPN1
                | qpArrCallPN1 qpArrCallPN2 VARIABLEIDM qpArrCallPN5
                | qpArrCallPN1 qpArrCallPN2 VARIABLEIDM qpArrCallPN4 VARIABLEIDM qpArrCallPN5'''

def p_qpArrCallPN1(p):
    '''qpArrCallPN1 : id'''
    global pOperands
    global scopeKey
    try:
        pOperands.append(p[1])
        pTypes.append(varsTables[funcsDir[0]["name"]][p[1]]["type"])
        scopeKey = funcsDir[0]["name"]
    except:
        try:
            pOperands.append(p[1])
            pTypes.append(varsTables[activeFuncTable][p[1]]["type"])
            scopeKey = activeFuncTable
        except:
            print("No existe la variable " + p[1])

def p_qpArrCallPN2(p):
    '''qpArrCallPN2 : empty'''
    global pilaDim
    global dim
    global scopeKey
    global arrId
    global arrType
    global pOperators
    arrId = pOperands.pop()
    arrType = pTypes.pop()
    #try en caso de que variable no esté declarada
    try:
        #Verificar si el id tiene dimensiones
        if(varsTables[scopeKey][arrId]['isArray'] == True):
            dim = 1
            pilaDim.append(arrId)
            pilaDim.append(dim)
            # get first node of dimension (list)
            pOperators.append("[")
    except:
        print("Sintax error: variable ", arrId, " no declarada")

def p_qpArrCallPN3(p):
   '''qpArrCallPN3 : empty'''
   global pOperands
   global dim
   global varsTables
   global constTable
   global scopeKey
   global arrId
   global quadCont
   global quads
   expr = pOperands[len(pOperands)-1]
   quads.append(["Ver", expr, 0, varsTables[scopeKey][arrId]["arrDims"][dim-1]["LS"]])
   if dim == 1 and len(varsTables[scopeKey][arrId]["arrDims"]) == 2:
       aux = pOperands.pop()
       constantsMemory.setStartPointer("int")
       constantsMemory.updateVirtualAddressPointer()
       constTable[varsTables[scopeKey][arrId]["arrDims"][dim-1]["M"]] = constantsMemory.getAddressPointers("int")
       quads.append(["*", aux, varsTables[scopeKey][arrId]["arrDims"][dim-1]["M"], "t" + str(quadCont)])
       pOperands.append("t" + str(quadCont))
       if activeScope != "global":
           tempMemoryLocal.setStartPointer(arrType)
           tempMemoryLocal.updateVirtualAddressPointer()
           localTempsTable["t" + str(quadCont)] = tempMemoryLocal.getAddressPointers(arrType)
       else:
           tempMemoryGlobal.setStartPointer(arrType)
           tempMemoryGlobal.updateVirtualAddressPointer()
           globalTempsTable["t" + str(quadCont)] = tempMemoryGlobal.getAddressPointers(arrType)
       quadCont+=1
   if dim == 2:
       aux2 = pOperands.pop()
       aux1 = pOperands.pop()
       quads.append(["+", aux1, aux2, "t" + str(quadCont)])
       pOperands.append("t" + str(quadCont))
       if activeScope != "global":
           tempMemoryLocal.setStartPointer(arrType)
           tempMemoryLocal.updateVirtualAddressPointer()
           localTempsTable["t" + str(quadCont)] = tempMemoryLocal.getAddressPointers(arrType)
       else:
           tempMemoryGlobal.setStartPointer(arrType)
           tempMemoryGlobal.updateVirtualAddressPointer()
           globalTempsTable["t" + str(quadCont)] = tempMemoryGlobal.getAddressPointers(arrType)
       quadCont+=1


def p_qpArrCallPN4(p):
    '''qpArrCallPN4 : empty'''
    global dim
    global pilaDim
    #only execute if id has len(arrDims) == 2
    dim = dim + 1
    pilaDim.pop()
    pilaDim.append(dim)


def p_qpArrCallPN5(p):
   '''qpArrCallPN5 : empty'''
   #only execute if id isArray
   global quads
   global quadCont
   global arrId
   global pOperators
   aux1 = pOperands.pop()
   tempAux = "t" + str(quadCont)
   quads.append(["+", aux1, 0, tempAux])
   if activeScope != "global":
       tempMemoryLocal.setStartPointer(arrType)
       tempMemoryLocal.updateVirtualAddressPointer()
       localTempsTable[tempAux] = tempMemoryLocal.getAddressPointers(arrType)
       quadCont += 1
       pointersMemoryLocal.setStartPointer(arrType)
       pointersMemoryLocal.updateVirtualAddressPointer()
       localTempsTable["t"+str(quadCont)] = pointersMemoryLocal.getAddressPointers(arrType)
       constantsMemory.setStartPointer("int")
       constantsMemory.updateVirtualAddressPointer()
       constTable[varsTables[scopeKey][arrId]["dirV"]] = constantsMemory.getAddressPointers("int")
       quads.append(["+", tempAux, varsTables[scopeKey][arrId]["dirV"], "t"+str(quadCont)])
       pOperands.append("(t"+str(quadCont)+")")
       pOperators.pop()
       quadCont+=1
   else:
       tempMemoryGlobal.setStartPointer(arrType)
       tempMemoryGlobal.updateVirtualAddressPointer()
       globalTempsTable[tempAux] = tempMemoryGlobal.getAddressPointers(arrType)
       quadCont += 1
       pointersMemoryGlobal.setStartPointer(arrType)
       pointersMemoryGlobal.updateVirtualAddressPointer()
       globalTempsTable["t"+str(quadCont)] = pointersMemoryGlobal.getAddressPointers(arrType)
       constantsMemory.setStartPointer("int")
       constantsMemory.updateVirtualAddressPointer()
       constTable[varsTables[scopeKey][arrId]["dirV"]] = constantsMemory.getAddressPointers("int")
       quads.append(["+", tempAux, varsTables[scopeKey][arrId]["dirV"], "t"+str(quadCont)])
       pOperands.append("(t"+str(quadCont)+")")
       pOperators.pop()
       quadCont+=1

#Regla para definir dimensión de variable
def p_VARIABLEIDM(p):
    '''VARIABLEIDM : leftSqBracket EXPR qpArrCallPN3 rightSqBracket'''

#Regla para expresión aritmética
def p_EXPR(p):
    '''EXPR : TERMINO MASOMENOST qpExpPN4'''

#Regla auxiliar para permitir suma resta de terminos
def p_MASOMENOST(p):
    '''MASOMENOST : qpExpPN3 TERMINO qpExpPN4 MASOMENOST
                  | empty'''

#Regla para término
def p_TERMINO(p):
    '''TERMINO : FACTOR PORENTREF qpExpPN5'''

#Regla para permitir la multiplicación/division de factores
def p_PORENTREF(p):
    '''PORENTREF : qpExpPN2 FACTOR qpExpPN5 PORENTREF
                 | empty'''

#Regla para definirlos elementos validos de un factor
def p_FACTOR(p):
    '''FACTOR : VARIABLE
              | leftParenthesis minusSign FACTOR qpExpPN8 rightParenthesis
              | NUMERO
              | leftParenthesis qpExpPN6 EXPR rightParenthesis qpExpPN7
              | LLAMADA'''


def p_VARIABLEFACTOR(p):
    '''VARIABLEFACTOR : VARIABLE'''
    pOperands.append(p[1])
    try:
        pTypes.append(varsTables[funcsDir[0]["name"]][p[1]]["type"])
    except:
        try:
            pTypes.append(varsTables[activeFuncTable][p[1]]["type"])
        except:
            print("No existe la variable " + p[1])

#Punto neuralgico 1 de expresiones
def p_qpExpPN1(p):
    '''qpExpPN1 : id '''
    pOperands.append(p[1])
    try:
        pTypes.append(varsTables[funcsDir[0]["name"]][p[1]]["type"])
    except:
        try:
            pTypes.append(varsTables[activeFuncTable][p[1]]["type"])
        except:
            print("No existe la variable " + p[1])

#PN 3 de expresiones
def p_qpExpPN2(p):
    '''qpExpPN2 : multiplicationSign
                | divisionSign'''
    pOperators.append(p[1])

#PN3 de expresiones
def p_qpExpPN3(p):
    '''qpExpPN3 : plusSign
                | minusSign'''
    pOperators.append(p[1])

#PN4 de expresiones
def p_qpExpPN4(p):
    '''qpExpPN4 : empty'''
    global quadCont
    global activeScope
    if len(pOperators) > 0:
        if pOperators[len(pOperators)-1] == '+' or pOperators[len(pOperators)-1] == '-':
            right_operand = pOperands.pop()
            right_type = pTypes.pop()
            left_operand = pOperands.pop()
            left_type = pTypes.pop()
            operator = pOperators.pop()
            result = "t" + str(quadCont)
            result_type = semanticCube[left_type][right_type][operator]
            if result_type != "error":
                quads.append([operator, left_operand, right_operand, result])
                quadCont += 1
                pOperands.append(result)
                pTypes.append(result_type)
                if activeScope != "global":
                    tempMemoryLocal.setStartPointer(result_type)
                    tempMemoryLocal.updateVirtualAddressPointer()
                    localTempsTable[result] = tempMemoryLocal.getAddressPointers(result_type)
                else:
                    tempMemoryGlobal.setStartPointer(result_type)
                    tempMemoryGlobal.updateVirtualAddressPointer()
                    globalTempsTable[result] = tempMemoryGlobal.getAddressPointers(result_type)
            else:
                print("Type mismatch")

#PN5 de expresiones
def p_qpExpPN5(p):
    '''qpExpPN5 : empty'''
    global quadCont
    global activeScope
    if len(pOperators) > 0:
        if pOperators[len(pOperators)-1] == '*' or pOperators[len(pOperators)-1] == '/':
            right_operand = pOperands.pop()
            right_type = pTypes.pop()
            left_operand = pOperands.pop()
            left_type = pTypes.pop()
            operator = pOperators.pop()
            result_type = semanticCube[left_type][right_type][operator]
            result = "t" + str(quadCont)
            if result_type != "error":
                quads.append([operator, left_operand, right_operand, result])
                quadCont += 1
                pOperands.append(result)
                pTypes.append(result_type)
                print("pilas despues de append quad", pOperators)
                if activeScope != "global":
                    tempMemoryLocal.setStartPointer(result_type)
                    tempMemoryLocal.updateVirtualAddressPointer()
                    localTempsTable[result] = tempMemoryLocal.getAddressPointers(result_type)
                else:
                    tempMemoryGlobal.setStartPointer(result_type)
                    tempMemoryGlobal.updateVirtualAddressPointer()
                    globalTempsTable[result] = tempMemoryGlobal.getAddressPointers(result_type)
            else:
                print("Type mismatch")

#PN6 de expresiones
def p_qpExpPN6(p):
    '''qpExpPN6 : empty'''
    pOperators.append("(")

#PN7 de expresiones
def p_qpExpPN7(p):
    '''qpExpPN7 : empty'''
    pOperators.pop()

#PN8 de expresiones
def p_qpExpPN8(p):
    '''qpExpPN8 : empty'''
    negValue = pOperands.pop()
    negValue = "-" + str(negValue)
    pOperands.append(negValue)

#PN1 de asignación
def p_qpAssignPN1(p):
    '''qpAssignPN1 : empty'''
    global quadCont
    if True:
        right_operand = pOperands.pop()
        right_type = pTypes.pop()
        operator = "="
        result = pOperands.pop()
        left_type = pTypes.pop()
        result_type = semanticCube[left_type][right_type][operator]
        if result_type != "error":
            quads.append([operator, right_operand, "", result])
            pOperands.append(result)
            pTypes.append(result_type)
        else:
            print("Type mismatch")

#PN1 de input
def p_qpInputPN1(p):
    '''qpInputPN1 : empty'''
    # PENDIENTE VALIDAR TIPOS
    global quadCont
    result = pAssigns.pop()
    pAssignsTypes.pop()
    quads.append(["INPUT", "", "", result])

#PN1 de print
def p_qPrintPN1(p):
    '''qpPrintPN1 : empty'''
    global quadCont
    result = pOperands.pop()
    quads.append(["PRINT", "", "", result])

#PN2 de print
def p_qPrintPN2(p):
    '''qpPrintPN2 : cteString'''
    global quadCont
    result = p[1]
    quads.append(["PRINT", "", "", result])

#PN1 de bool
def p_qpBoolPN1(p):
    '''qpBoolPN1 : empty'''
    operand = pOperands.pop()
    type = pTypes.pop()
    pCompOperands.append(operand)
    pCompTypes.append(type)

#PN de bool
def p_qpBoolPN2(p):
    '''qpBoolPN2 : empty'''
    global quadCont
    right_operand = pCompOperands.pop()
    right_type = pCompTypes.pop()
    left_operand = pOperands.pop()
    left_type = pTypes.pop()
    operator = pCompOperators.pop()
    result = "t" + str(quadCont)
    result_type = semanticCube[left_type][right_type][operator]
    if result_type != "error":
        quads.append([operator, left_operand, right_operand, result])
        quadCont += 1
        pCompOperands.append(result)#estaba en pila de expresiones normakes
        pCompTypes.append(result_type)#same
        if activeScope != "global":
            tempMemoryLocal.setStartPointer(result_type)
            tempMemoryLocal.updateVirtualAddressPointer()
            localTempsTable[result] = tempMemoryLocal.getAddressPointers(result_type)
            # print("quads ", quads)
            # print("local temps table: ", localTempsTable)
        else:
            tempMemoryGlobal.setStartPointer(result_type)
            tempMemoryGlobal.updateVirtualAddressPointer()
            globalTempsTable[result] = tempMemoryGlobal.getAddressPointers(result_type)

    else:
        print("Type mismatch")

#PN5 de funciones
def p_qpFuncsPN5(p):
    '''qpFuncsPN5 : empty'''
    global tempsCont
    global contTempLocal
    global contTempGlobal
    global quadCont
    tempsCont = quadCont
    contTempGlobal = quadCont
    quadCont = 1

#PN5 de funciones parte 2
def p_qpFuncsPN5Pt2(p):
    '''qpFuncsPN5Pt2 : empty'''
    funcsDir[len(funcsDir)-1]["varsSize"] = len(varsTables[activeFuncTable])

#PN6 de funciones
def p_qpFuncsPN6(p):
    '''qpFuncsPN6 : empty'''
    funcsDir[len(funcsDir)-1]["startFunc"] = len(quads)+1

#PN7 de funciones
def p_qpFuncsPN7(p):
    '''qpFuncsPN7 : empty'''
    global tempsCont
    global quadCont
    tempsCont = quadCont - tempsCont
    funcsDir[len(funcsDir)-1]["tempSize"] = tempsCont
    quads.append(["ENDFUNC", "", "", ""])
    quadCont = contTempGlobal

#Regla de expresiones comparativas
def p_EXPCOMPARATIVA(p):
    '''EXPCOMPARATIVA : EXPR qpBoolPN1 COMPARISONOP EXPR qpBoolPN2'''

# Regla de operadores comparativos
def p_COMPARISONOP(p):
    '''COMPARISONOP : greaterThan
                    | lessThan
                    | notEqual
                    | comparison'''

    pCompOperators.append(p[1])

#PN1 de estatutos condicionales
def p_COND(p):
    '''COND : if leftParenthesis EXPCOMPARATIVA qpCondPN1 rightParenthesis BLOQUE qpCondPN2
            | if leftParenthesis EXPCOMPARATIVA qpCondPN1 rightParenthesis BLOQUE qpCondPN3 else BLOQUE qpCondPN2'''

#Se ejecuta despues de evaluar la expresión del if, crea un GOTOF llevando como parametro
#el resultado de EXPCOMPARATIVA y agrega el cuadruplo actual a la pila de saltos
def p_qpCondPN1(p):
    '''qpCondPN1 : empty'''
    #quads.append(["GOTOF", pCompOperands.pop(), "", ____])
    #pSaltos.append(len(quads) - 1)
    #...pendiente
    if pCompTypes.pop() == "bool":
        quads.append(["GOTOF", pCompOperands.pop(), ""])
        pJumps.append(len(quads) - 1)#quad recien agregado queda pendiente de llenar
    else:
        print("If statement, type mismatch")

#PN2 de Condiciones
#llenar cuadruplo pendiente
def p_qpCondPN2(p):
    '''qpCondPN2 : empty'''
    #llenar el goto que se encuentre en la posicion guardada en pila saltos, con dir. de cuadruplo siguiente
    quads[pJumps.pop()].append(len(quads))


#PN3 de estatutos condicionales
#GOTO si o si a fin de else
def p_qpCondPN3(p):
    '''qpCondPN3 : empty'''
    #goto si o si
    #quads.append(["GOTO", "", "", ____])
    quads.append(["GOTO","",""])
    quads[pJumps.pop()].append(len(quads))
    #agregarlo a pila saltos como pendiente (es el ultimo cuadruplo actual de la pila)
    pJumps.append(len(quads) - 1)

#PN1 de ciclos
def p_qpCicloPN1(p):
    '''qpCicloPN1 : empty'''

#PN2 de ciclos
#llenar cuadruplo pendiente
def p_qpCicloPN2(p):
    '''qpCicloPN2 : empty'''
    pJumps.append(len(quads))
    if pCompTypes.pop() == "bool":
        quads.append(["GOTOF", pCompOperands.pop(), ""])
        pJumps.append(len(quads) - 1)
    else:
        print("While statement, type mismatch")

#PN3 de ciclos
#GOTO si o si a fin de else
def p_qpCicloPN3(p):
    '''qpCicloPN3 : empty'''
    returnSt = pJumps.pop() - 1
    quads.append(["GOTO","","",returnSt])
    quads[pJumps.pop()].append(len(quads))

#PN2 de llamada
def p_qpLlamadaPN2(p):
    '''qpLlamadaPN2 : empty'''
    global paramCounter
    global paramPointer
    paramCounter = 1 #global to use it in PN3
    paramPointer = 0 #global to use it in PN3
    global calledFuncId
    calledFuncId = pOperands.pop()#save it to generate the quad and, to use it in PN3
    quads.append(["ERA",calledFuncId,"",""])#func id saved in pOperands at PN1

#PN3 de llamada
def p_qpLlamadaPN3(p):
    '''qpLlamadaPN3 : empty'''
    global paramCounter
    arg = pOperands.pop()#argumento
    argType = pTypes.pop()#tipo argumento
    #Verify argType against func.parametros[paramPointer]
    #funcsDir.append({'name': name[0], 'type': tipo, 'kind': "func", "param": []
    try:
        for element in funcsDir:#to find called func in dirFunc
            if(element["name"] == calledFuncId):#when you find it
                if(element["param"][paramCounter - 1] != argType):#actual verify param type
                    print("Wrong param type: ", calledFuncId)#print error about param type
                else:
                    #genera cuadruplo [PARAMETRO, "parametro origen(expr)", "", "Parametro receptor en funcion"]
                    quads.append(["PARAMETRO", arg, "", paramCounter-1])#se guarda numero de parametro
                    #paramCounter += 1
    except:
        print("Params error in func: ", calledFuncId)

#PN4 de llamada
def p_qpLlamadaPN4(p):
    '''qpLlamadaPN4 : empty'''
    global paramCounter
    paramCounter = paramCounter + 1

#PN5 de llamada
def p_qpLlamadaPN5(p):
    '''qpLlamadaPN5 : empty'''
    global paramCounter
    try:
        for element in funcsDir:  # to find called func in dirFunc
            if (element["name"] == calledFuncId):  # when you find it
                if len(element["param"]) != paramCounter:
                    print("Params out of range")
    except:
        print("Params error in func: ", calledFuncId)

#PN6 de llamada
def p_qpLlamadaPN6(p):
    '''qpLlamadaPN6 : empty'''
    try:
        for element in funcsDir:  # to find called func in dirFunc
            if (element["name"] == calledFuncId):  # when you find it
                quads.append(['GOSUB',element["name"],'',element["startFunc"]-1])
    except:
        print("Params error in func: ", calledFuncId)

#Regla para una llamada
def p_LLAMADA(p):
    '''LLAMADA : LLAMADAID leftParenthesis qpLlamadaPN2 LLAMADAEXPR qpLlamadaPN5 rightParenthesis qpLlamadaPN6
               | LLAMADAID leftParenthesis qpLlamadaPN2 rightParenthesis qpLlamadaPN6'''
    global quads
    global quadCont
    global funcsDir
    ##add quad to save func return
    #func id = quads[len(quads)-1][1]   (last quad "GOSUB")
    calledFuncId=quads[len(quads)-1][1]
    result = "t" + str(quadCont)
    quads.append(["RETURNASSIGN", '', '', result])
    quadCont += 1
    pOperands.append(result)
    resultType = "returnType"
    #search for func type
    for item in funcsDir:
        if item["name"] == calledFuncId:
            resultType = item["type"]
    pTypes.append(resultType)
    if activeScope != "global":
        tempMemoryLocal.setStartPointer(resultType)
        tempMemoryLocal.updateVirtualAddressPointer()
        localTempsTable[result] = tempMemoryLocal.getAddressPointers(resultType)
        #print("quads ", quads)
        #print("local temps table: ", localTempsTable)
    else:
        tempMemoryGlobal.setStartPointer(resultType)
        tempMemoryGlobal.updateVirtualAddressPointer()
        globalTempsTable[result] = tempMemoryGlobal.getAddressPointers(resultType)
        #print("quads ", quads)
        #print("global temps table: ", globalTempsTable)




#Particion de regla llamada, para guardar id de función
def p_LLAMADAID(p):
    '''LLAMADAID : id'''
    #qpLlamadaPN1 - Validar si función está declarada.
    flag = False
    for item in funcsDir:
        if item["name"] == p[1]:
            flag = True
            #save func if in order to use it in PN2
            pOperands.append(p[1])
            print("func  exists")

    if flag == False:
        print("Función " , p[1], " no declarada")

#Regla para llamadas a funciones de tipo void
def p_LLAMADAVOID(p):
    '''LLAMADAVOID : LLAMADAID leftParenthesis qpLlamadaPN2 LLAMADAEXPR qpLlamadaPN5 rightParenthesis qpLlamadaPN6 semicolon
               | LLAMADAID leftParenthesis qpLlamadaPN2 rightParenthesis qpLlamadaPN6 semicolon'''

#Particion de regla llamada funcion, para introducir puntos neuralgicos
def p_LLAMADAEXPR(p):
    '''LLAMADAEXPR : EXPR qpLlamadaPN3 LLAMADAEXPRAUX'''

#Regla auxiliar de llamadaexpr, para seguir agregando expresiones (nuevos argumentos para la funcion),  o salir
def p_LLAMADAEXPRAUX(p):
    '''LLAMADAEXPRAUX : qpLlamadaPN4 comma LLAMADAEXPR
                      | empty'''

#Regla para ciclo
def p_CICLO(p):
    '''CICLO : while qpCicloPN1 leftParenthesis EXPCOMPARATIVA qpCicloPN2 rightParenthesis BLOQUE qpCicloPN3'''

#Regla para aceptar constantes de tipo numero
def p_NUMERO(p):
    '''NUMERO : int
              | float'''
    pOperands.append(p[1])
    global constantsMemory
    if type(p[1]) == int:
        pTypes.append("int")
        constantsMemory.setStartPointer("int")
        constantsMemory.updateVirtualAddressPointer()
        constTable[p[1]] = constantsMemory.getIntAddress()
    else:
        pTypes.append("float")
        constantsMemory.setStartPointer("float")
        constantsMemory.updateVirtualAddressPointer()
        constTable[p[1]] = constantsMemory.getFloatAddress()

#Regla para asignacion
def p_ASSIGN(p):
    '''ASSIGN : VARIABLE equalSign EXPR semicolon qpAssignPN1
              | VARIABLE equalSign INPUT semicolon qpInputPN1'''

#Regla para input
def p_INPUT(p):
    '''INPUT : input'''

#Regla para print
def p_PRINT(p):
    '''PRINT : print leftParenthesis PRINTARGS rightParenthesis semicolon'''

#Regla para manejar multiples argumentos del print
def p_PRINTARGS(p):
    '''PRINTARGS : EXPR qpPrintPN1 EXPRARGSAUX
                 | qpPrintPN2 EXPRARGSAUX'''

#Regla auxiliar de exprsargs, para salir o continuar imprimiendo argumentos
def p_EXPRARGSAUX(p):
    '''EXPRARGSAUX : comma PRINTARGS
                   | empty'''

#Regla vacia para la insersión de puntos neurálgicos
def p_empty(p):
    'empty :'
    pass


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input: ", p.value)

def verifyIfPointer(value):
    if type(value) == str and len(value) > 0 and value[0] == "(":
        dir = str(value[1:len(value) - 1])
        return dir, True
    else:
        return value, False

yacc.yacc()

# Build the parser
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            if yacc.parse(data) == "COMPILA":
                print("Valid input")
                vm = VirtualMachine.VirtualMachine(quads, funcsDir, varsTables, constTable, globalTempsTable, localTempsTable)
                vm.debug_structs()
                vm.translate_quads()
                vm.debug_structs()
                vm.executeProgram()
        except EOFError:
            print(EOFError)
    else:
        print("No file to test found")
