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
    def p_PROGRAM(p):
        '''
        program : PROGRAM ID SEMICOLON program1
        '''   
        p[0] = 'Compiled check' 

    def p_program1(p):
        '''
        program1 : VARS functions principal
                | VARS functions 
                | program2
        '''   

    def p_program2(p):
        '''
        program2 : principal
        '''   

    def p_PRINCIPAL(p):
        '''
        principal: PRINCIPAL LEFTPAR RIGHTPAR LEFTBR statutes RIGHTBR
        '''   

    #####SIMPLE STATUTES GRAMMAR####
    def p_STATUTES(p):
        '''
        statutes: assign SEMICOLON statutes
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
        callFunction : ID LEFTPAR exp RIGHT PAR
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

<<<<<<< Updated upstream
    def p_WRITING(p):
=======
    def p_WRITING(self,p):
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
    def p_MEDIA(p):
=======
    def p_MEDIA(self,p):
>>>>>>> Stashed changes
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
        else : ELSE LEFTBR statutes RIGHT BR
                | empty
        '''            

    #### CYCLES AND REPETITIONS####

    def p_FOR(p):
        '''
        for : FOR assign TO CTEINT DO LEFTBR statutes RIGHTBR
        '''            

    def p_WHILE(p):
        '''
        while : WHILE LEFTPAR exp RIGHTPAR DO LEFTBR statutes RIGHT BR
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
                | MINUS
                | TIMES
                | DIVIDE
                | GREATER
                | GREATERAND
                | LESSER
                | LESSERTHAN
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
<<<<<<< Updated upstream
        variables : COMMA ID VARIABLES
                | COMMA ID LEFTSQR CTE_INT RIGHTSQR VARIABLES
=======
        variables : COMMA ID variables
                | COMMA ID LEFTSQR CTEINT RIGHTSQR variables
>>>>>>> Stashed changes
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

    def p_error(self,p):
        print ("Syntax Error with: ", p)

    def p_empty(p):
        '''
        empty : 
        '''     
        p[0] = None   