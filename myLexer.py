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

    # list of TOKENS
    tokens = [
        
        'DIGIT', 'DIGITS', 'LETTER',
        'ID','CTEL','CTEF','CTESTRING',
        'PROGRAM', 'VAR',
        'INT', 'FLOAT','PRINT','IF','ELSE', 
        'COLON','SEMICOLON' ,'COMMA','LEFTBR','RIGHTBR','EQUAL',
        'LEFTPAR','RIGHTPAR','DOT','GREATER','LESSER',
        'PLUS', 'REST', 'TIMES' , 'DIVIDE',
        'nl',
    ]
    # tokens DEFINITION

    def t_DIGIT(self,t):
        r'[0-9]'
        print("DIGIT")
        return t

    def t_DIGITS(self,t):
        r't_DIGIT+'
        print("DIGITS")
        return t

    def t_LETTER(self, t):
        r'[a-zA-Z]'
        print("LETTER")
        return t

    def t_ID(self,t):
        r't_LETTER(t_LETTER|t_DIGIT)'
        print("ID")
        return t

    def t_CTEL(self,t):
        r't_DIGITS'
        print("CTEL")
        return t

    def t_CTEF(self,t):
        r't_DIGITS[.]?t_DIGITS'
        print("EQUAL")
        return t

    def t_CTESTRING(self,t):
        r't_LETTER*'
        print("EQUAL")
        return t

    def t_PROGRAM(self,t):
        r'program'
        print("PROGRAM")
        return t

    def t_VAR(self,t):
        r'var'
        print("VAR")
        return t

    def t_INT(self,t):
        r'int'
        print("INT")
        return t

    def t_FLOAT(self,t):
        r'float'
        print("FLOAT")
        return t

    def t_PRINT(self,t):
        r'print'
        print("PRINT")
        return t

    def t_IF(self,t):
        r'if'
        print("IF")
        return t

    def t_ELSE(self,t):
        r'else'
        print("ELSE")
        return t

    def t_COLON(self,t):
        r'\:'
        print(":")
        return t

    def t_SEMICOLON(self,t):
        r'\;'
        print("SEMICOLON")
        return t

    def t_COMMA(self,t):
        r'\,'
        print("COMMA")
        return t

    def t_LEFTBR(self,t):
        r'\{'
        print("LEFTBRACKET")
        return t

    def t_RIGHTBR(self,t):
        r'\}'
        print("RIGHTBRACKET")
        return t

    def t_EQUAL(self,t):
        r'\='
        print("EQUAL")
        return t

    def t_LEFTPAR(self,t):
        r'\('
        print("LEFT PARENTHESIS")
        return t

    def t_RIGHTPAR(self,t):
        r'\)'
        print("RIGHT PARENTHESIS")
        return t

    def t_DOT(self,t):
        r'\.'
        print("PERIOD")
        return t

    def t_GREATER(self,t):
        r'\>'
        print("GREATER THAN")
        return t

    def t_LESSER(self,t):
        r'\<'
        print("LESSER THAN")
        return t

    def t_PLUS(self,t):
        r'\+'
        print("SUM")
        return t

    def t_REST(self,t):
        r'\-'
        print("SUBSTRACT")
        return t

    def t_TIMES(self,t):
        r'\*'
        print("MULTIPLY")
        return t

    def t_DIVIDE(self,t):
        r'\/'
        print("DIVIDE")
        return t

    # every symbol that doesn't match with almost one of the previous tokens is considered an error
    def t_error(self,t):
        r'.'
        print("ERROR:", t.value)
        return t

    def t_nl(self,t):
        r'(\n|\r|\r\n)|\s'
        pass
