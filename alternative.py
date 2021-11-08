#Alternative file structure due to errors by Andres Carlos Barrera A00815749
#Lexer/Parser using PLY

import ply.lex as lex
import ply.yacc as yacc
import sys
from ply.lex import TOKEN

reserved = {
    'Program' : 'PROGRAM', # program reserved word
    'principal' : 'PRINCIPAL', # main reserved word
    'function' : 'FUNCTION', # function reserved word 
    'VARS' : 'VARS', # VARS reserved word
    'int' : 'INT', # int reserved word
    'float' : 'FLOAT', # flot reserved word
    'char' : 'CHAR', # char reserved word
    'return' : 'RETURN', # return reserved word
    'read' : 'READ', # read reserved word
    'write' : 'WRITE', # write reserved word
    'if' : 'IF', # if reserved word
    'then' : 'THEN', # then reserved word
    'else' : 'ELSE',  # else reserved word
    'while' : 'WHILE', # while reserved word
    'do' : 'DO', # do reserved word
    'for' : 'FOR', # for reserved word
    'to' : 'TO', # to reserved word
    'void' : 'VOID', # void reserved word
    'media' : 'MEDIA', # special function average
    'moda' : 'MODA', # special function mode
    'varianza' : 'VARIANZA', # special function variance
    'regresionsimple' : 'REGRESIONSIMPLE', # special function simple regression
    'plotxy' : 'PLOTXY', # special function plot two data columns
}


# list of TOKENS
tokens = [
   
    'ID', # ID token
    'PLUS', # + symbol
    'REST', # - symbol
    'TIMES', # * symbol
    'DIVIDE', # / symbol
    'AND', # & symbol
    'OR', # | symbol
    'GREATER', # > symbol
    'GREATERAND', # >= symbol
    'LESSER', # < symbol
    'LESSERAND', # <= symbol
    'SAME', # == symbol
    'NOTSAME', # <> symbol
    'EQUAL', # = symbol
    'LEFTBR', # { symbol
    'RIGHTBR', # } symbol
    'LEFTPAR', # ( symbol
    'RIGHTPAR', # ) symbol
    'LEFTSQR', # [ symbol
    'RIGHTSQR', # ] symbol
    'COLON', # : symbol
    'SEMICOLON', # ; symbol
    'COMMA', # , symbol
    'DOT', # . symbol
    'QUOT', # " symbol
    'CTEINT', # constant int
    'CTEFLOAT', # constant float
    'CTESTRING', # constant string
    'CTECHAR', # constant char
    'nl', # end symbol
    ] + list(reserved.values())

# Tokens DEFINITION
#Symbols

def t_PLUS(t):
    r'\+'
    return t

def t_REST(t):
    r'\-'
    return t

def t_TIMES(t):
    r'\*'
    return t

def t_DIVIDE(t):
    r'\/'
    return t    

def t_AND(t):
    r'\&'
    return t

def t_OR(t):
    r'\|'
    return t

def t_GREATER(t):
    r'\>'
    return t

def t_GREATERAND(t):
    r'\>='
    return t

def t_LESSER(t):
    r'\<'
    return t

def t_LESSERAND(t):
    r'\<='
    return t

def t_SAME(t):
    r'\=\='
    return t

def t_NOTSAME(t):
    r'\<>'
    return t

def t_EQUAL(t):
    r'\='
    return t

def t_LEFTBR(t):
    r'\{'
    return t

def t_RIGHTBR(t):
    r'\}'
    return t

def t_LEFTPAR(t):
    r'\('
    return t

def t_RIGHTPAR(t):
    r'\)'
    return t

def t_LEFTSQR(t):
    r'\['
    return t

def t_RIGHTSQR(t):
    r'\]'
    return t

def t_COLON(t):
    r'\:'
    return t

def t_SEMICOLON(t):
    r'\;'
    return t

def t_COMMA(t):
    r'\,'
    return t

def t_DOT(t):
    r'\.'
    return t

#def t_QUOT(t):
#    r'\"'
#    return t


#Complex Definitions
#cte char breaks the flow, see how to fix this
#def t_CTECHAR(t):
#    r'[a-zA-Z0-9]'
#    t.value = str(t.value)
#    return t

def t_CTESTRING(t):
    r'\"[\w\d\s\,. ]*\"|\'[\w\d\s\,. ]*\'' # taking note of both "string" and 'string'
    t.value = str(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_CTEINT(t):
    r'0|[-+]?[1-9][0-9]*' # taking account if sign symbol is present
    return t

def t_CTEFLOAT(t):
    r'[-+]?\d*\.\d+' # able to accept sign symbols, and .97 (numbers without the integer part)
    return t

# every symbol that doesn't match with almost one of the previous tokens is considered an error
#modification so that all errors can be processed and debugged
def t_error(t):
    print("ERROR at: '%s'" % t.value)
    t.lexer.skip(1)

def t_nl(t):
    r'(\n|\r|\r\n)|\s'
    pass

lexer = lex.lex()

#######################PARSER SECTION#############################
########### GRAMMAR START DEFINITION###############
##Outer shell grammar#####
def p_PROGRAM(p):
    '''
    program : PROGRAM ID SEMICOLON program1
    '''   
    p[0] = 'Compiled check' 

def p_program1(p):
    '''
    program1 : vars functions principal
            | vars functions 
            | program2
    '''   

def p_program2(p):
    '''
    program2 : principal
    '''   

def p_PRINCIPAL(p):
    '''
    principal : PRINCIPAL LEFTPAR RIGHTPAR LEFTBR statutes RIGHTBR
    '''   

#####SIMPLE STATUTES GRAMMAR####
def p_STATUTES(p):
    '''
    statutes : assign SEMICOLON statutes
            | callFunction SEMICOLON statutes
            | reading statutes SEMICOLON statutes
            | writing statutes SEMICOLON statutes
            | if statutes
            | while statutes
            | for statutes
            | return statutes
            | empty
    '''

def p_ASSIGN(p):
    '''
    assign : ID EQUAL exp
            | ID LEFTSQR exp RIGHTSQR EQUAL exp
    '''            

def p_CALLFUNCTION(p):
    '''
    callFunction : ID LEFTPAR exp RIGHTPAR
    '''            

def p_READING(p):
    '''
    reading : READ LEFTPAR reading1 RIGHTPAR
    '''            

def p_READING1(p):
    '''
    reading1 : ID reading2
    '''            

def p_READING2(p):
    '''
    reading2 : COMMA reading1
            | empty
    '''            

def p_WRITING(p):
    '''
    writing : WRITE LEFTPAR writing1 RIGHTPAR
    '''            

def p_WRITING1(p):
    '''
    writing1 : writing2 COMMA writing2
            | writing2
    '''            

def p_WRITING2(p):
    '''
    writing2 : CTESTRING
            | CTEINT
            | CTEFLOAT
            | exp
    '''            

def p_MEDIA(p):
    '''
    media : MEDIA LEFTPAR array RIGHTPAR SEMICOLON
    '''            

####### DECISIONS  #########

def p_IF(p):
    '''
    if : IF LEFTPAR exp RIGHTPAR THEN LEFTBR statutes RIGHTBR else
    '''            

def p_ELSE(p):
    '''
    else : ELSE LEFTBR statutes RIGHTBR
            | empty
    '''            

#### CYCLES AND REPETITIONS####

def p_FOR(p):
    '''
    for : FOR assign TO CTEINT DO LEFTBR statutes RIGHTBR
    '''            

def p_WHILE(p):
    '''
    while : WHILE LEFTPAR exp RIGHTPAR DO LEFTBR statutes RIGHTBR
    '''            

###ARITHMETIC, EXPRESSIONS AND THE LIKE ####

def p_EXP(p):
    '''
    exp : ID expression exp
        | array expression exp
        | constants expression exp
        | ID
        | callFunction
        | ID LEFTSQR exp RIGHTSQR
        | constants
    '''            

def p_CONSTANTS(p):
    '''
    constants : CTEINT
            | CTEFLOAT
    '''            

def p_EXPRESSION(p):
    '''
    expression : PLUS
            | REST
            | TIMES
            | DIVIDE
            | GREATER
            | GREATERAND
            | LESSER
            | LESSERAND
    '''            

##VARS, VARIABBLES AND THEIR DECLARATION WITH CAVEATS ####

def p_VARS(p):
    '''
    vars : VARS vars1
        | empty
    '''            

def p_VARS1(p):
    '''
    vars1 : typing COLON ID variables SEMICOLON vars2
    '''            

def p_VARS2(p):
    '''
    vars2 : vars1
        | empty
    '''            

def p_VARIABLES(p):
    '''
    variables : COMMA ID variables
            | COMMA ID LEFTSQR CTEINT RIGHTSQR variables
            | empty
    '''            

def p_TYPING(p):
    '''
    typing : INT
            | CHAR
            | FLOAT
    '''            

def p_ARRAY(p):
    '''
    array : LEFTSQR exp RIGHTSQR
            | LEFTSQR CTEINT RIGHTSQR
    '''            

### FUNCTION, VOIDS AND TYPED RESULTS ON RETURNS #####

def p_FUNCTIONS(p):
    '''
    functions : FUNCTION VOID voidfunction functions
                | FUNCTION typing typefunction functions
                | empty
    '''            

def p_VOIDFUNCTION(p):
    '''
    voidfunction : ID LEFTPAR args RIGHTPAR vars LEFTBR statutes RIGHTBR
    '''            

def p_TYPEFUNCTION(p):
    '''
    typefunction : ID LEFTPAR args RIGHTPAR vars LEFTBR statutes return SEMICOLON RIGHTBR
    '''            

def p_ARGS(p):
    '''
    args : typing COLON ID argsplural
        | empty
    '''            

def p_ARGSPLURAL(p):
    '''
    argsplural : COMMA args
                | empty
    '''            

def p_RETURN(p):
    '''
    return : RETURN LEFTPAR exp RIGHTPAR SEMICOLON
            | RETURN LEFTPAR exp RIGHTPAR
    '''            


#EXCEPTIONS HANDLING#####

def p_error(p):
    print ("Syntax Error with: ", p)

def p_empty(p):
    '''
    empty : 
    '''     
    p[0] = None       

parser = yacc.yacc()

def main():
    try:
        fileName = 'D:\\Documents\\Trabajo\\Semestre 17\\Compiladores\\ProyectoCompiladoresNotas\\Avancex pruebas\\Compiladores2021-main\\test1.txt'
        currentFile = open(fileName, 'r')
        print("Current File is: " + fileName)
        info = currentFile.read() 
        currentFile.close()
        lexer.input(info)
        while True: 
            tok = lexer.token() 
            if not tok: 
                break 
            print(tok)
        if(parser.parse(info, tracking=True) == 'Compiled check'): 
            print("CORRECT SYNTAX")
        else: 
            print("SYNTAX ERROR")
    
    except EOFError: 
        print(EOFError)

main()
