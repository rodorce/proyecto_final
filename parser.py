# Yacc example

import sys
import ply.yacc as yacc
from lexer import tokens

def p_PROGRAMA(p):
    '''PROGRAMA : programType id semicolon main BLOQUE
                | programType id semicolon VARS main BLOQUE
                | programType id semicolon FUNCS main BLOQUE
                | programType id semicolon VARS FUNCS main BLOQUE
    '''
    p[0] = 'COMPILA'

def p_VARS(p):
    '''VARS : TIPO VARSAUX semicolon'''

# def p_VARSAUX(p):
#     '''VARSAUX : id VARSCOMMA
#                | id ARRAYDIMENSION ARRAYDIMENSION VARSCOMMA semicolon'''

def p_VARSCOMMA(p):
    '''VARSCOMMA : comma VARSAUX
                 | empty'''

def p_FUNCS(p):
    '''FUNCS : function FUNCTIPO id leftParenthesis FUNCPARAM rightParenthesis leftBracket FUNCSVARS FUNCSESTATUTOS return FUNCEXP semicolon rightBracket'''

def p_FUNCTIPO(p):
    '''FUNCTIPO : TIPO 
                | void'''

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

def p_PARAM(p):
    '''PARAM : TIPO id'''

def p_VARSAUX(p):
    '''VARSAUX : id ARRAYDIMENSION ARRAYDIMENSION VARSCOMMA'''

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

