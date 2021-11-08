#Parser by Andres Carlos Barrera A00815749
#Parser using Lexer and PLY
from myLexer import *
import ply.yacc as yacc
import sys
import os

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

    ########### GRAMMAR START DEFINITION###############
    ##Outer shell grammar#####
    def p_PROGRAM(self,p):
        '''
        program : PROGRAM ID SEMICOLON program1
        '''   
        p[0] = 'Compiled check' 

    def p_program1(self,p):
        '''
        program1 : vars functions principal
                | vars functions 
                | program2
        '''   

    def p_program2(self,p):
        '''
        program2 : principal
        '''   

    def p_PRINCIPAL(self,p):
        '''
        principal : PRINCIPAL LEFTPAR RIGHTPAR LEFTBR statutes RIGHTBR
        '''   

    #####SIMPLE STATUTES GRAMMAR####
    def p_STATUTES(self,p):
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

    def p_ASSIGN(self,p):
        '''
        assign : ID EQUAL exp
                | ID LEFTSQR exp RIGHTSQR EQUAL exp
        '''            

    def p_CALLFUNCTION(self,p):
        '''
        callFunction : ID LEFTPAR exp RIGHTPAR
        '''            

    def p_READING(self,p):
        '''
        reading : READ LEFTPAR reading1 RIGHTPAR
        '''            

    def p_READING1(self,p):
        '''
        reading1 : ID reading2
        '''            

    def p_READING2(self,p):
        '''
        reading2 : COMMA reading1
                | empty
        '''            

    def p_WRITING(self,p):
        '''
        writing : WRITE LEFTPAR writing1 RIGHTPAR
        '''            

    def p_WRITING1(self,p):
        '''
        writing1 : writing2 COMMA writing2
                | writing2
        '''            

    def p_WRITING2(self,p):
        '''
        writing2 : CTESTRING
                | CTEINT
                | CTEFLOAT
                | exp
        '''            

    def p_MEDIA(self,p):
        '''
        media : MEDIA LEFTPAR array RIGHTPAR SEMICOLON
        '''            

    ####### DECISIONS  #########

    def p_IF(self,p):
        '''
        if : IF LEFTPAR exp RIGHTPAR THEN LEFTBR statutes RIGHTBR else
        '''            

    def p_ELSE(self,p):
        '''
        else : ELSE LEFTBR statutes RIGHTBR
                | empty
        '''            

    #### CYCLES AND REPETITIONS####

    def p_FOR(self,p):
        '''
        for : FOR assign TO CTEINT DO LEFTBR statutes RIGHTBR
        '''            

    def p_WHILE(self,p):
        '''
        while : WHILE LEFTPAR exp RIGHTPAR DO LEFTBR statutes RIGHTBR
        '''            

    ###ARITHMETIC, EXPRESSIONS AND THE LIKE ####

    def p_EXP(self,p):
        '''
        exp : ID expression exp
            | array expression exp
            | constants expression exp
            | ID
            | callFunction
            | ID LEFTSQR exp RIGHTSQR
            | constants
        '''            

    def p_CONSTANTS(self,p):
        '''
        constants : CTEINT
                | CTEFLOAT
        '''            

    def p_EXPRESSION(self,p):
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

    def p_VARS(self,p):
        '''
        vars : VARS vars1
            | empty
        '''            

    def p_VARS1(self,p):
        '''
        vars1 : typing COLON ID variables SEMICOLON vars2
        '''            

    def p_VARS2(self,p):
        '''
        vars2 : vars1
            | empty
        '''            

    def p_VARIABLES(self,p):
        '''
        variables : COMMA ID variables
                | COMMA ID LEFTSQR CTEINT RIGHTSQR variables
                | empty
        '''            

    def p_TYPING(self,p):
        '''
        typing : INT
                | CHAR
                | FLOAT
        '''            

    def p_ARRAY(self,p):
        '''
        array : LEFTSQR exp RIGHTSQR
                | LEFTSQR CTEINT RIGHTSQR
        '''            

    ### FUNCTION, VOIDS AND TYPED RESULTS ON RETURNS #####

    def p_FUNCTIONS(self,p):
        '''
        functions : FUNCTION VOID voidfunction functions
                    | FUNCTION typing typefunction functions
                    | empty
        '''            

    def p_VOIDFUNCTION(self,p):
        '''
        voidfunction : ID LEFTPAR args RIGHTPAR vars LEFTBR statutes RIGHTBR
        '''            

    def p_TYPEFUNCTION(self,p):
        '''
        typefunction : ID LEFTPAR args RIGHTPAR vars LEFTBR statutes return SEMICOLON RIGHTBR
        '''            

    def p_ARGS(self,p):
        '''
        args : typing COLON ID argsplural
            | empty
        '''            

    def p_ARGSPLURAL(self,p):
        '''
        argsplural : COMMA args
                    | empty
        '''            

    def p_RETURN(self,p):
        '''
        return : RETURN LEFTPAR exp RIGHTPAR SEMICOLON
                | RETURN LEFTPAR exp RIGHTPAR
        '''            


    #EXCEPTIONS HANDLING#####

    def p_error(self,p):
        print ("Syntax Error with: ", p)

    def p_empty(self,p):
        '''
        empty : 
        '''     
        p[0] = None   