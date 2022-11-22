import ply.lex as lex
from ply.lex import TOKEN

# Reserved words
reserved = {
    'if': 'if',
    'then': 'then',
    'else': 'else',
    'while': 'while',
    'int': 'intType',
    'float': 'floatType',
    'func': 'function',
    'print': 'print',
    'main': 'main',
    'program': 'programType',
    'return': 'return',
    'void': 'void',
    'input': 'input'
}
# Regular expression rules for simple tokens
t_notEqual = r'<>'
# List of token names.   This is always required
tokens = ['id',
          'int',
          'float',
          'cteString',
          'cteFloat',
          'cteInt',
          'comparison',
          'notEqual',
          'leftBracket',
          'rightBracket',
          'leftParenthesis',
          'rightParenthesis',
          'comma',
          'colon',
          'semicolon',
          'rightSqBracket',
          'leftSqBracket',
          'plusSign',
          'minusSign',
          'multiplicationSign',
          'divisionSign',
          'equalSign',
          'greaterThan',
          'lessThan',
          ] + list(reserved.values())

literals = ['(', ')', '{', '}', '[', ']', '+', '-', '*', '/', ',', ';', ':', '=', '>', '<']


# A regular expression rule with some action code
def t_id(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'id')  # Check for reserved words
    return t


def t_cteString(t):
    r'\".*\"'
    return t


def t_float(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


def t_int(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_comma(t):
    r'\,'
    t.type = 'comma'  # Set token type to the expected literal
    return t


def t_colon(t):
    r'\:'
    t.type = 'colon'  # Set token type to the expected literal
    return t


def t_semicolon(t):
    r'\;'
    t.type = 'semicolon'  # Set token type to the expected literal
    return t


def t_comparison(t):
    r'\=='
    t.type = 'comparison'
    return t


def t_equalSign(t):
    r'\='
    t.type = 'equalSign'  # Set token type to the expected literal
    return t


def t_plusSign(t):
    r'\+'
    t.type = 'plusSign'  # Set token type to the expected literal
    return t


def t_minusSign(t):
    r'\-'
    t.type = 'minusSign'  # Set token type to the expected literal
    return t


def t_multiplicationSign(t):
    r'\*'
    t.type = 'multiplicationSign'  # Set token type to the expected literal
    return t


def t_divisionSign(t):
    r'\/'
    t.type = 'divisionSign'  # Set token type to the expected literal
    return t


def t_leftParenthesis(t):
    r'\('
    t.type = 'leftParenthesis'  # Set token type to the expected literal
    return t


def t_rightParenthesis(t):
    r'\)'
    t.type = 'rightParenthesis'  # Set token type to the expected literal
    return t


def t_leftBracket(t):
    r'\{'
    t.type = 'leftBracket'  # Set token type to the expected literal
    return t


def t_rightBracket(t):
    r'\}'
    t.type = 'rightBracket'  # Set token type to the expected literal
    return t


def t_leftSqBracket(t):
    r'\['
    t.type = 'leftSqBracket'  # Set token type to the expected literal
    return t


def t_rightSqBracket(t):
    r'\]'
    t.type = 'rightSqBracket'  # Set token type to the expected literal
    return t


def t_greaterThan(t):
    r'>'
    return t


def t_lessThan(t):
    r'<'
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


r_NUMERO = r'[0-9]*\.?[0-9]+((E|e)(\+|-)?[0-9]+)?'

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Test it out
data = """
program programita;

int a,b;;

func int funcionUno(int param1){
 param1=8;
 return param1;
}

main{
 a=8;
 b=9;
 a=a+b-funcionUno(4+4);
 print(a);
 if(a<b){
  a=a-4;
 }
 if(a==b){
 x = d
 }else if(b<>c){
    g = h
 }

 while(a+3<b-1){
  a=a+1;
 }
}
"""

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)