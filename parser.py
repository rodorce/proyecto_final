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
activeFuncTable = "none"  # global should be outside of any function
activeScope = "global"
pOperators = []
pOperands = []
pTypes = []
pAssigns = []
pAssignsTypes = []
pCompOperands = []
pCompOperators = []
pCompTypes = []
quads = []
quadCont = 1 #contador para temporales
contTempLocal = 0
contTempGlobal = 0
pJumps = []#pila saltos
tempsCont = 0 # Limite inferior
paramCounter = 0
paramPointer = 0
globalMemory = MemoryPointer("global",1000, 1000, 2000, 3000, 4000, 4999)
localMemory = MemoryPointer("local", 5000, 5000, 6000, 7000, 8000, 8999)
tempMemoryGlobal = MemoryPointer("temporal global", 9000, 9000, 10000, 11000, 12000, 12999)
tempMemoryLocal = MemoryPointer("temporal local", 13000, 13000, 14000, 15000, 16000, 17999)
constantsMemory = MemoryPointer("constant", 18000, 18000, 19000, 20000, 21000, 21999)
globalTempsTable = {}
localTempsTable = {}
constTable = {}
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
    '''PROGRAMA : programType SAVEPROGID semicolon main BLOQUE
                | programType SAVEPROGID semicolon VARS main BLOQUE
                | programType SAVEPROGID semicolon FUNCS main BLOQUE
                | programType SAVEPROGID semicolon VARS FUNCS main BLOQUE
    '''
    p[0] = 'COMPILA'

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


def p_MOREVARS(p):
    '''MOREVARS : VARS
                | empty'''


def p_VARS(p):
    '''VARS : TIPO VARSAUX semicolon MOREVARS'''


# def p_VARSAUX(p):
#     '''VARSAUX : id VARSCOMMA
#                | id ARRAYDIMENSION ARRAYDIMENSION VARSCOMMA semicolon'''

def p_VARSCOMMA(p):
    '''VARSCOMMA : comma VARSAUX
                 | empty'''
    global name
    global tipo
    global activeFuncTable
    global varsTipo


def p_FUNCS(p):
    '''FUNCS : function FUNCTIPO SAVEFUNCID leftParenthesis FUNCPARAM rightParenthesis leftBracket qpFuncsPN5 FUNCSVARS qpFuncsPN5Pt2 qpFuncsPN6 FUNCSESTATUTOS return FUNCEXP semicolon qpFuncsPN7 PNRIGHTBTACKETFUNC MOREFUNCS'''


# to acept more than one func
def p_MOREFUNCS(p):
    '''MOREFUNCS : FUNCS
                 | empty'''


def p_PNRIGHTBTACKETFUNC(p):
    '''PNRIGHTBTACKETFUNC : rightBracket'''
    global activeFuncTable
    global funcsDir
    varsTables.pop(activeFuncTable)
    activeFuncTable = "global"


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


def p_FUNCTIPO(p):
    '''FUNCTIPO : TIPO 
                | void'''
    global tipo
    if (p.__getitem__(1) == "void"):  # pre-save the func type
        tipo = "void"


def p_FUNCPARAM(p):
    '''FUNCPARAM : PARAM PARAMSCOMMA'''


def p_PARAMSCOMMA(p):
    '''PARAMSCOMMA : comma FUNCPARAM 
                    | empty'''


def p_FUNCSVARS(p):
    '''FUNCSVARS : VARS FUNCSVARS
                 | empty'''


def p_FUNCSESTATUTOS(p):
    '''FUNCSESTATUTOS : ESTATUTO FUNCSESTATUTOS
                     | empty'''


def p_FUNCEXP(p):
    '''FUNCEXP : EXPR 
               | empty'''


def p_BLOQUE(p):
    '''BLOQUE : leftBracket BLOQESTATUTO rightBracket'''


def p_BLOQESTATUTO(p):
    '''BLOQESTATUTO : ESTATUTO BLOQESTATUTO 
                    | empty'''


def p_TIPO(p):
    '''TIPO : intType
           | floatType'''
    global tipo
    tipo = p.__getitem__(1)  # pre-save the var type


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
        varsTables[activeFuncTable][name[0]] = {'type': tipo, 'kind': "local"}
        # clear the temp vars
        name.clear()
        # Punto neuralgico 3 donde se agrega el tipo de cada parametro en el directorio de funciones.
        funcsDir[len(funcsDir) - 1]["param"].append(tipo)
        #Punto neuralgico 4 donde se inserta el numero de parametros de la funcion
        funcsDir[len(funcsDir)-1]["paramSize"]+=1
        tipo = "-1"
    else:
        print("Error duplicated param var id")

def p_VARSAUX(p):
    '''VARSAUX : id ARRAYDIMENSION ARRAYDIMENSION VARSCOMMA'''
    global name
    global tipo
    global activeFuncTable
    global varsTipo
    global globalMemory
    name.append(p.__getitem__(1))  # pre-save the id
    varsTipo.append(tipo)

    # if id not in current funcTable add it
    for item in name:
        if item not in varsTables[activeFuncTable]:
            # add var id(item) to activeFuncTable (if it is global make var kind global)
            if activeScope != "global":
                varsTables[activeFuncTable][item] = {'type': varsTipo[0], 'kind': "local"}
            else:
                if varsTipo[0] == 'int':
                    globalMemory.setStartPointer(varsTipo[0])
                    globalMemory.updateVirtualAddressPointer()
                    varsTables[activeFuncTable][item] = {'type': varsTipo[0], 'kind': "global", "dirV": globalMemory.getIntAddress()}
                elif varsTipo[0] == "float":
                    globalMemory.setStartPointer(varsTipo[0])
                    globalMemory.updateVirtualAddressPointer()
                    varsTables[activeFuncTable][item] = {'type': varsTipo[0], 'kind': "global", "dirV": globalMemory.getFloatAddress()}
            name.remove(item)
            varsTipo.pop(0)
        else:
            print("Error duplicated var id")


def p_ARRAYDIMENSION(p):
    '''ARRAYDIMENSION : leftBracket int rightBracket
                    | empty'''


def p_ESTATUTO(p):
    '''ESTATUTO : ASSIGN 
                | PRINT
                | COND
                | LLAMADAVOID
                | CICLO'''


def p_VARIABLE(p):
    '''VARIABLE : id VARIABLEIDM VARIABLEIDM'''
    try:
        pAssigns.append(p[1])
        pAssignsTypes.append(varsTables[funcsDir[0]["name"]][p[1]]["type"])
    except:
        try:
            pAssigns.append(p[1])
            pAssignsTypes.append(varsTables[activeFuncTable][p[1]]["type"])
        except:
            print("No existe la variable " + p[1])


def p_VARIABLEIDM(p):
    '''VARIABLEIDM : leftSqBracket EXPR rightSqBracket
                    | empty'''
def p_EXPR(p):
    '''EXPR : TERMINO MASOMENOST qpExpPN4'''

def p_MASOMENOST(p):
    '''MASOMENOST : qpExpPN3 TERMINO qpExpPN4 MASOMENOST
                  | empty'''
def p_TERMINO(p):
    '''TERMINO : FACTOR PORENTREF qpExpPN5'''

def p_PORENTREF(p):
    '''PORENTREF : qpExpPN2 FACTOR qpExpPN5 PORENTREF
                 | empty'''


def p_FACTOR(p):
    '''FACTOR : qpExpPN1
              | leftParenthesis minusSign FACTOR qpExpPN8 rightParenthesis
              | NUMERO
              | leftParenthesis qpExpPN6 EXPR rightParenthesis qpExpPN7
              | LLAMADA'''
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

def p_qpExpPN2(p):
    '''qpExpPN2 : multiplicationSign
                | divisionSign'''
    pOperators.append(p[1])

def p_qpExpPN3(p):
    '''qpExpPN3 : plusSign
                | minusSign'''
    pOperators.append(p[1])

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
                if activeFuncTable != "global":
                    tempMemoryGlobal.setStartPointer(result_type)
                    tempMemoryGlobal.updateVirtualAddressPointer()
                    globalTempsTable[result] = tempMemoryGlobal.getAddressPointers(result_type)
                else:
                    tempMemoryLocal.setStartPointer(result_type)
                    tempMemoryLocal.updateVirtualAddressPointer()
                    localTempsTable[result] = tempMemoryLocal.getAddressPointers(result_type)
            else:
                print("Type mismatch")

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
                if activeFuncTable != "global":
                    tempMemoryGlobal.setStartPointer(result_type)
                    tempMemoryGlobal.updateVirtualAddressPointer()
                    globalTempsTable[result] = tempMemoryGlobal.getAddressPointers(result_type)
                else:
                    tempMemoryLocal.setStartPointer(result_type)
                    tempMemoryLocal.updateVirtualAddressPointer()
                    localTempsTable[result] = tempMemoryLocal.getAddressPointers(result_type)
            else:
                print("Type mismatch")

def p_qpExpPN6(p):
    '''qpExpPN6 : empty'''
    pOperators.append("(")

def p_qpExpPN7(p):
    '''qpExpPN7 : empty'''
    pOperators.pop()

def p_qpExpPN8(p):
    '''qpExpPN8 : empty'''
    negValue = pOperands.pop()
    negValue = "-" + str(negValue)
    pOperands.append(negValue)

def p_qpAssignPN1(p):
    '''qpAssignPN1 : empty'''
    global quadCont
    if True:
        right_operand = pOperands.pop()
        right_type = pTypes.pop()
        operator = "="
        result = pAssigns.pop()
        left_type = pAssignsTypes.pop()
        result_type = semanticCube[left_type][right_type][operator]
        if result_type != "error":
            quads.append([operator, right_operand, "", result])
            pOperands.append(result)
            pTypes.append(result_type)
        else:
            print("Type mismatch")

def p_qpInputPN1(p):
    '''qpInputPN1 : empty'''
    # PENDIENTE VALIDAR TIPOS
    global quadCont
    result = pAssigns.pop()
    pAssignsTypes.pop()
    quads.append(["INPUT", "", "", result])

def p_qPrintPN1(p):
    '''qpPrintPN1 : empty'''
    global quadCont
    result = pOperands.pop()
    quads.append(["PRINT", "", "", result])

def p_qPrintPN2(p):
    '''qpPrintPN2 : cteString'''
    global quadCont
    result = p[1]
    quads.append(["PRINT", "", "", result])

def p_qpBoolPN1(p):
    '''qpBoolPN1 : empty'''
    operand = pOperands.pop()
    type = pTypes.pop()
    pCompOperands.append(operand)
    pCompTypes.append(type)


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
        tempMemoryGlobal.setStartPointer(result_type)
        tempMemoryGlobal.updateVirtualAddressPointer()
        globalTempsTable[result] = tempMemoryGlobal.getAddressPointers(result_type)
    else:
        print("Type mismatch")

def p_qpFuncsPN5(p):
    '''qpFuncsPN5 : empty'''
    global tempsCont
    global contTempLocal
    global contTempGlobal
    global quadCont
    tempsCont = quadCont
    contTempGlobal = quadCont
    quadCont = 1

def p_qpFuncsPN5Pt2(p):
    '''qpFuncsPN5Pt2 : empty'''
    funcsDir[len(funcsDir)-1]["varsSize"] = len(varsTables[activeFuncTable])

def p_qpFuncsPN6(p):
    '''qpFuncsPN6 : empty'''
    funcsDir[len(funcsDir)-1]["startFunc"] = len(quads)+1

def p_qpFuncsPN7(p):
    '''qpFuncsPN7 : empty'''
    global tempsCont
    global quadCont
    tempsCont = quadCont - tempsCont
    funcsDir[len(funcsDir)-1]["tempSize"] = tempsCont
    quads.append(["ENDFUNC", "", "", ""])
    quadCont = contTempGlobal

def p_EXPCOMPARATIVA(p):
    '''EXPCOMPARATIVA : EXPR qpBoolPN1 COMPARISONOP EXPR qpBoolPN2'''


def p_COMPARISONOP(p):
    '''COMPARISONOP : greaterThan
                    | lessThan
                    | notEqual
                    | comparison'''

    pCompOperators.append(p[1])

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


#llenar cuadruplo pendiente
def p_qpCondPN2(p):
    '''qpCondPN2 : empty'''
    #llenar el goto que se encuentre en la posicion guardada en pila saltos, con dir. de cuadruplo siguiente
    quads[pJumps.pop()].append(len(quads))

#GOTO si o si a fin de else
def p_qpCondPN3(p):
    '''qpCondPN3 : empty'''
    #goto si o si
    #quads.append(["GOTO", "", "", ____])
    quads.append(["GOTO","",""])
    quads[pJumps.pop()].append(len(quads))
    #agregarlo a pila saltos como pendiente (es el ultimo cuadruplo actual de la pila)
    pJumps.append(len(quads) - 1)

def p_qpCicloPN1(p):
    '''qpCicloPN1 : empty'''

#llenar cuadruplo pendiente
def p_qpCicloPN2(p):
    '''qpCicloPN2 : empty'''
    pJumps.append(len(quads))
    if pCompTypes.pop() == "bool":
        quads.append(["GOTOF", pCompOperands.pop(), ""])
        pJumps.append(len(quads) - 1)
    else:
        print("While statement, type mismatch")

#GOTO si o si a fin de else
def p_qpCicloPN3(p):
    '''qpCicloPN3 : empty'''
    returnSt = pJumps.pop() - 1
    quads.append(["GOTO","","",returnSt])
    quads[pJumps.pop()].append(len(quads))

def p_qpLlamadaPN2(p):
    '''qpLlamadaPN2 : empty'''
    global paramCounter
    global paramPointer
    paramCounter = 1 #global to use it in PN3
    paramPointer = 0 #global to use it in PN3
    global calledFuncId
    calledFuncId = pOperands.pop()#save it to generate the quad and, to use it in PN3
    quads.append(["ERA",calledFuncId,"",""])#func id saved in pOperands at PN1

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

def p_qpLlamadaPN4(p):
    '''qpLlamadaPN4 : empty'''
    global paramCounter
    paramCounter = paramCounter + 1

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

def p_qpLlamadaPN6(p):
    '''qpLlamadaPN6 : empty'''
    try:
        for element in funcsDir:  # to find called func in dirFunc
            if (element["name"] == calledFuncId):  # when you find it
                quads.append(['GOSUB',element["name"],'',element["startFunc"]])
    except:
        print("Params error in func: ", calledFuncId)


def p_LLAMADA(p):
    '''LLAMADA : LLAMADAID leftParenthesis qpLlamadaPN2 LLAMADAEXPR qpLlamadaPN5 rightParenthesis qpLlamadaPN6
               | LLAMADAID leftParenthesis qpLlamadaPN2 rightParenthesis qpLlamadaPN6'''

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

def p_LLAMADAVOID(p):
    '''LLAMADAVOID : LLAMADAID leftParenthesis qpLlamadaPN2 LLAMADAEXPR qpLlamadaPN5 rightParenthesis qpLlamadaPN6 semicolon
               | LLAMADAID leftParenthesis qpLlamadaPN2 rightParenthesis qpLlamadaPN6 semicolon'''


def p_LLAMADAEXPR(p):
    '''LLAMADAEXPR : EXPR qpLlamadaPN3 LLAMADAEXPRAUX'''


def p_LLAMADAEXPRAUX(p):
    '''LLAMADAEXPRAUX : qpLlamadaPN4 comma LLAMADAEXPR
                      | empty'''


def p_CICLO(p):
    '''CICLO : while qpCicloPN1 leftParenthesis EXPCOMPARATIVA qpCicloPN2 rightParenthesis BLOQUE qpCicloPN3'''


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


def p_ASSIGN(p):
    '''ASSIGN : VARIABLE equalSign EXPR semicolon qpAssignPN1
              | VARIABLE equalSign INPUT semicolon qpInputPN1'''

def p_INPUT(p):
    '''INPUT : input'''

def p_PRINT(p):
    '''PRINT : print leftParenthesis PRINTARGS rightParenthesis semicolon'''


def p_PRINTARGS(p):
    '''PRINTARGS : EXPR qpPrintPN1 EXPRARGSAUX
                 | qpPrintPN2 EXPRARGSAUX'''


def p_EXPRARGSAUX(p):
    '''EXPRARGSAUX : comma PRINTARGS
                   | empty'''


def p_empty(p):
    'empty :'
    pass


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input: ", p.value)


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
                vm.executeProgram()
        except EOFError:
            print(EOFError)
    else:
        print("No file to test found")
