# Yacc example

import sys
import ply.yacc as yacc
from lexer import tokens

#Directorio de funciones y tablas de variables
funcsDir = []#{'name': "funcName", 'type': "int/float/void/programType", 'kind': "program/func"}
varsTables = {}#{'tableName': {'varName': {'type': "int/float", 'kind': "local/global"}}}
#funcs/vars pre-data to save
name = []
tipo = "-1"
varsTipo = []#multiple vars with same type ex: int a,b,c,d;

#current active func(to save vars in its table)
activeFuncTable = "none" #global should be outside of any function
activeScope = "global"

def p_PROGRAMA(p):
    '''PROGRAMA : programType SAVEPROGID semicolon main BLOQUE
                | programType SAVEPROGID semicolon VARS main BLOQUE
                | programType SAVEPROGID semicolon FUNCS main BLOQUE
                | programType SAVEPROGID semicolon VARS FUNCS main BLOQUE
    '''
    p[0] = 'COMPILA'
    print("FuncsDir")
    print(funcsDir)
    print("Vars:")
    print(varsTables)

def p_SAVEPROGID(p):
    '''SAVEPROGID : id'''
    global activeFuncTable
    global activeScope
    #save program id to funcsDir
    funcsDir.append({'name': p.__getitem__(1), 'type': "programType", 'kind': "program"})
    #create empty program varsTable(global vars)
    varsTables[p.__getitem__(1)] = {}
    #set activeScope global
    activeFuncTable = p.__getitem__(1)
    activeScope = "global"

def p_VARS(p):
    '''VARS : TIPO VARSAUX semicolon'''

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
    '''FUNCS : function FUNCTIPO SAVEFUNCID leftParenthesis FUNCPARAM rightParenthesis leftBracket FUNCSVARS FUNCSESTATUTOS return FUNCEXP semicolon PNRIGHTBTACKETFUNC MOREFUNCS'''
#to acept more than one func
def p_MOREFUNCS(p):
    '''MOREFUNCS : FUNCS
                 | empty'''
def p_PNRIGHTBTACKETFUNC(p):
    '''PNRIGHTBTACKETFUNC : rightBracket'''
    global activeFuncTable
    activeFuncTable = "global"

def p_SAVEFUNCID(p):
    '''SAVEFUNCID : id'''
    global name
    global tipo
    global activeFuncTable
    global activeScope
    name.append(p.__getitem__(1))#pre-save the id
    if name[0] not in funcsDir:
        #save in funcsDir
        funcsDir.append({'name': name[0], 'type': tipo, 'kind': "func"})
        #create empty func varsTable????
        varsTables[name[0]] = {}
        #set current func as active varsTable and scope
        activeFuncTable = name[0]
        activeScope = "local"
        #clear the temp vars
        name.clear()
        tipo = "-1"
    else:
        print("Error duplicated func id")

def p_FUNCTIPO(p):
    '''FUNCTIPO : TIPO 
                | void'''
    global tipo
    if(p.__getitem__(1) == "void"):#pre-save the func type
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
    tipo = p.__getitem__(1)#pre-save the var type

def p_PARAM(p):
    '''PARAM : TIPO id'''
    global name
    global tipo
    global activeFuncTable
    name.clear()
    name.append(p.__getitem__(2))#pre-save the id
    #if id not in current funcTable add it
    if name[0] not in varsTables[activeFuncTable]:
        #add var id(name) to activeFuncTable
        varsTables[activeFuncTable][name[0]] = {'type': tipo, 'kind': "local"}
        #clear the temp vars
        name.clear()
        tipo = "-1"
    else:
        print("Error duplicated param var id")

def p_VARSAUX(p):
    '''VARSAUX : id ARRAYDIMENSION ARRAYDIMENSION VARSCOMMA'''
    global name
    global tipo
    global activeFuncTable
    global varsTipo
    name.append(p.__getitem__(1))#pre-save the id
    varsTipo.append(tipo)

    #if id not in current funcTable add it
    for item in name:
        if item not in varsTables[activeFuncTable]:
            #add var id(item) to activeFuncTable (if it is global make var kind global)
            if(activeScope != "global"):
                varsTables[activeFuncTable][item] = {'type': varsTipo[0], 'kind': "local"}
            else:
                varsTables[activeFuncTable][item] = {'type': varsTipo[0], 'kind': "global"}
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

def p_VARIABLEIDM(p):
    '''VARIABLEIDM : leftSqBracket EXPR rightSqBracket
                    | empty'''

def p_EXPR(p):
    '''EXPR : TERMINO MASOMENOST'''

def p_MASOMENOST(p):
    '''MASOMENOST : plusSign TERMINO
                  | minusSign TERMINO
                  | empty'''

def p_TERMINO(p):
    '''TERMINO : FACTOR PORENTREF'''

def p_PORENTREF(p):
    '''PORENTREF : multiplicationSign TERMINO
                 | minusSign TERMINO
                 | empty'''

def p_FACTOR(p):
    '''FACTOR : id
              | leftParenthesis minusSign FACTOR rightParenthesis
              | NUMERO
              | leftParenthesis EXPR rightParenthesis
              | LLAMADA'''

def p_EXPCOMPARATIVA(p):
    '''EXPCOMPARATIVA : EXPR COMPARISONOP EXPR'''

def p_COMPARISONOP(p):
    '''COMPARISONOP : greaterThan
                    | lessThan
                    | notEqual
                    | comparison'''

def p_COND(p):
    '''COND : if leftParenthesis EXPCOMPARATIVA rightParenthesis BLOQUE
            | if leftParenthesis EXPCOMPARATIVA rightParenthesis BLOQUE else BLOQUE'''

def p_LLAMADA(p):
    '''LLAMADA : id leftParenthesis LLAMADAEXPR rightParenthesis
               | id leftParenthesis rightParenthesis'''
def p_LLAMADAVOID(p):
    '''LLAMADAVOID : id leftParenthesis LLAMADAEXPR rightParenthesis semicolon
               | id leftParenthesis rightParenthesis semicolon'''

def p_LLAMADAEXPR(p):
    '''LLAMADAEXPR : EXPR LLAMADAEXPRAUX'''

def p_LLAMADAEXPRAUX(p):
    '''LLAMADAEXPRAUX : comma LLAMADAEXPR
                      | empty'''

def p_CICLO(p):
    '''CICLO : while leftParenthesis EXPCOMPARATIVA rightParenthesis BLOQUE'''

def p_NUMERO(p):
    '''NUMERO : int
              | float'''

def p_ASSIGN(p):
    '''ASSIGN : VARIABLE equalSign EXPR semicolon'''

def p_PRINT(p):
    '''PRINT : print leftParenthesis PRINTARGS rightParenthesis semicolon'''

def p_PRINTARGS(p):
    '''PRINTARGS : EXPR EXPRARGSAUX
                 | cteString EXPRARGSAUX'''

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
        except EOFError:
            print(EOFError)
    else:
        print("No file to test found")

