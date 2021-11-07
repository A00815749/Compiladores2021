#Lexer by Andres Carlos Barrera A00815749
#Lexer using PLY

import ply.lex as lex
import ply.yacc as yacc
import sys
from ply.lex import TOKEN

class MyLexer():
    # CONSTRUCTOR
    def __init__(self):
        print('Lexer constructor called.')
        self.lexer = lex.lex(module=self)

    # DESTRUCTOR
    def __del__(self):
        print('Lexer destructor called.')

    #ID Types 
    reserved = {
    'Program' : 'PROGRAM',  # program reserved word
    'function' : 'FUNCTION', # function reserved word 
    'VARS' : 'VARS', # VARS reserved word
    'void' : 'VOID', # void reserved word
    'int' : 'INT', # int reserved word
    'float' : 'FLOT', # flot reserved word
    'char' : 'CHAR', # char reserved word
    'principal' : 'PRINCIPAL', # main reserved word
    'if' : 'IF', # if reserved word
    'then' : 'THEN', # then reserved word
    'else' : 'ELSE', # else reserved word
    'read' : 'READ',# read reserved word
    'write' : 'WRITE', # write reserved word
    'return' : 'RETURN', # return reserved word
    'end' : 'END', # special symbol reserved
    'for' : 'FOR', # for reserved word
    'from' : 'FROM', # from reserved word
    'while' : 'WHILE', # while reserved word
    'to' : 'TO', # to reserved word
    'media' : 'MEDIA', # special function average
    'moda' : 'MODA', # special function mode
    'varianza' : 'VARIANZA', # special function variance
    'regresionsimple' : 'REGRESIONSIMPLE', # special function simple regression
    'plotxy' : 'PLOTXY', # special function plot two data columns
    'do' : 'DO' # do reserved word
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
        'CTE_INT', # constant int
        'CTE_FLOT', # constant float
        'CTE_STRING', # constant string
        'CTE_CHAR', # constant char
        'nl', # end symbol
    ] + list(reserved.values())

    
    # Tokens DEFINITION
    #Symbols

    def t_PLUS(self,t):
        r'\+'
        return t

    def t_REST(self,t):
        r'\-'
        return t

    def t_TIMES(self,t):
        r'\*'
        return t

    def t_DIVIDE(self,t):
        r'\/'
        return t    

    def t_AND(self,t):
        r'\&'
        return t

    def t_OR(self,t):
        r'\|'
        return t

    def t_GREATER(self,t):
        r'\>'
        return t

    def t_GREATERAND(self,t):
        r'\>='
        return t

    def t_LESSER(self,t):
        r'\<'
        return t

    def t_LESSERAND(self,t):
        r'\<='
        return t

    def t_SAME(self,t):
        r'\=\='
        return t

    def t_NOTSAME(self,t):
        r'\<>'
        return t

    def t_EQUAL(self,t):
        r'\='
        return t

    def t_LEFTBR(self,t):
        r'\{'
        return t

    def t_RIGHTBR(self,t):
        r'\}'
        return t

    def t_LEFTPAR(self,t):
        r'\('
        return t

    def t_RIGHTPAR(self,t):
        r'\)'
        return t

    def t_LEFTSQR(self,t):
        r'\['
        return t

    def t_RIGHTSQR(self,t):
        r'\]'
        return t

    def t_COLON(self,t):
        r'\:'
        print(":")
        return t

    def t_SEMICOLON(self,t):
        r'\;'
        return t

    def t_COMMA(self,t):
        r'\,'
        return t

    def t_DOT(self,t):
        r'\.'
        return t
    
    def t_QUOT(self,t):
        r'\"' 
        return t

    
    #Complex Definitions 
    #def t_CTE_CHAR(self,t):
     #   r'[a-zA-Z0-9]'
      #  t.value = str(t.value)
       # return t

    def t_CTE_STRING(self,t):
        r'\"[\w\d\s\,. ]*\"|\'[\w\d\s\,. ]*\'' # taking note of both "string" and 'string'
        t.value = str(t.value)
        return t

    def t_PROGRAM(self,t):
        r'Program'
        return t

    def t_MAIN(self,t):
        r'main'
        return t

    def t_VARS(self,t):
        r'VARS'
        return t

    def t_INT(self,t):
        r'int'
        return t

    def t_FLOT(self,t):
        r'flot'
        return t

    def t_CHAR(self,t):
        r'char'
        return t

    def t_PRINCIPAL(self,t):
        r'principal'
        return t

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z0-9]*'
        reserved = {
        'Program' : 'PROGRAM',  # program reserved word
        'function' : 'FUNCTION', # function reserved word 
        'VARS' : 'VARS', # VARS reserved word
        'void' : 'VOID', # void reserved word
        'int' : 'INT', # int reserved word
        'float' : 'FLOT', # flot reserved word
        'char' : 'CHAR', # char reserved word
        'principal' : 'PRINCIPAL', # main reserved word
        'if' : 'IF', # if reserved word
        'then' : 'THEN', # then reserved word
        'else' : 'ELSE', # else reserved word
        'read' : 'READ',# read reserved word
        'write' : 'WRITE', # write reserved word
        'return' : 'RETURN', # return reserved word
        'end' : 'END', # special symbol reserved
        'for' : 'FOR', # for reserved word
        'from' : 'FROM', # from reserved word
        'while' : 'WHILE', # while reserved word
        'to' : 'TO', # to reserved word
        'media' : 'MEDIA', # special function average
        'moda' : 'MODA', # special function mode
        'varianza' : 'VARIANZA', # special function variance
        'regresionsimple' : 'REGRESIONSIMPLE', # special function simple regression
        'plotxy' : 'PLOTXY', # special function plot two data columns
        'do' : 'DO' # do reserved word
        }
        t.type = reserved.get(t.value, 'ID')
        return t
    
    def t_FUNCTION(self,t):
        r'function'
        return t

    def t_RETURN(self,t):
        r'return'
        return t

    def t_READ(self,t):
        r'read'
        return t

    def t_WRITE(self,t):
        r'write'
        return t

    def t_IF(self,t):
        r'if'
        return t

    def t_THEN(self,t):
        r'then'
        return t

    def t_ELSE(self,t):
        r'else'
        return t

    def t_WHILE(self,t):
        r'while'
        return t

    def t_DO(self,t):
        r'do'
        return t

    def t_FOR(self,t):
        r'for'
        return t

    def t_TO(self,t):
        r'to'
        return t

    def t_VOID(self,t):
        r'void'
        return t

    def t_MEDIA(self,t):
        r'media'
        return t

    def t_MODA(self,t):
        r'moda'
        return t

    def t_VARIANZA(self,t):
        r'varianza'
        return t

    def t_REGRESIONSIMPLE(self,t):
        r'regresionsimple'
        return t

    def t_PLOTXY(self,t):
        r'plotxy'
        return t

    def t_CTE_INT(self,t):
        r'0|[-+]?[1-9][0-9]*' # taking account if sign symbol is present
        t.value = int(t.value)
        return t

    def t_CTE_FLOT(self,t):
        r'[-+]?\d*\.\d+' # able to accept sign symbols, and .97 (numbers without the integer part)
        t.value = float(t.value)
        return t

    # every symbol that doesn't match with almost one of the previous tokens is considered an error
    #modification so that all errors can be processed and debugged
    def t_error(self,t):
        print("ERROR at: '%s'" % t.value)
        t.lexer.skip(1)

    def t_nl(self,t):
        r'(\n|\r|\r\n)|\s'
        pass
