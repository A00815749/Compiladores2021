from myLexer import *
import ply.yacc as yacc
import sys

class MyParser:

    # CONSTRUCTOR
    def __init__(self,lexer):
        print("Parser constructor called")
        self.parser = yacc.yacc(module=self)
        self.lexer = lexer

    # DESTRUCTOR
    def __del__(self):
        print('Parser destructor called.')

    tokens = MyLexer.tokens


    # GRAMMAR START
    def p_PROGRAMA(self,p):
        '''
        PROGRAMA : PROGRAM ID COLON BLOQUE
                    | PROGRAM ID COLON VARS BLOQUE
        '''    

    def p_VARS(self,p):
        '''
        VARS : VAR ID VARS2
        '''            

    def p_VARS2(self,p):
        '''
        VARS2 : VARS3 COLON TIPO SEMICOLON VARS2
                |
        '''          

    def p_VARS3(self,p):
        '''
        VARS3 : COMMA VARS3
                |
        '''        

    def p_TIPO(self,p):
        '''
        TIPO : INT
                | FLOAT
        '''          

    def p_BLOQUE(self,p):
        '''
        BLOQUE : LEFTBR RIGHTBR
                | LEFTBR ESTATUTO BLOQUE2 RIGHTBR
        '''    

    def p_BLOQUE2(self,p):
        '''
        BLOQUE2 : ESTATUTO BLOQUE2
                | 
        '''    

    def p_ESTATUTO(self,p):
        '''
        ESTATUTO : ASIGNACION
                | CONDICION
                | ESCRITURA
        '''    

    def p_ASIGNACION(self,p):
        '''
        ASIGNACION : ID EQUAL EXPRESION SEMICOLON
        ''' 

    def p_ESCRITURA(self,p):
        '''
        ESCRITURA : PRINT LEFTPAR CTESTRING ESCRITURA2 RIGHTPAR SEMICOLON
                    | PRINT LEFTPAR EXPRESION ESCRITURA2 RIGHTPAR SEMICOLON
        '''    

    def p_ESCRITURA2(self,p):
        '''
        ESCRITURA2 : DOT EXPRESION ESCRITURA2
                    | DOT CTESTRING ESCRITURA2
                    |
        '''    

    def p_EXPRESION(self,p):
        '''
        EXPRESION : EXP EXPRESION2
        '''    

    def p_EXPRESION2(self,p):
        '''
        EXPRESION2 : GREATER EXP
                    | LESSER EXP
                    | LESSER GREATER EXP
                    |
        '''    

    def p_CONDICION(self,p):
        '''
        CONDICION : IF LEFTPAR EXPRESION RIGHTPAR BLOQUE SEMICOLON
                    | IF LEFTPAR EXPRESION RIGHTPAR BLOQUE ELSE BLOQUE SEMICOLON
        '''    

    def p_EXP(self,p):
        '''
        EXP : TERMINO EXP2
        '''    

    def p_EXP2(self,p):
        '''
        EXP2 : PLUS TERMINO
                | REST TERMINO
                |
        '''    

    def p_TERMINO(self,p):
        '''
        TERMINO : FACTOR TERMINO2
        '''    

    def p_TERMINO2(self,p):
        '''
        TERMINO2 : TIMES FACTOR 
                    |  DIVIDE FACTOR
                    |
        ''' 

    def p_FACTOR(self,p):
        '''
        FACTOR : LEFTPAR EXPRESION RIGHTPAR
                    | VARCTE
                    | PLUS VARCTE
                    | REST VARCTE
        ''' 

    def p_VARCTE(self,p):
        '''
        VARCTE : ID
                | CTEL
                | CTEF
        ''' 

    def p_error(self,p):
        '''
        '''
