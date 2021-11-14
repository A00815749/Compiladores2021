#Parser by Andres Carlos Barrera A00815749
#Parser using Lexer and PLY
from myLexer import *
import ply.yacc as yacc
from Vartables import Variable, Vartables
from Semanticcube import Semanticcube
from myStack import myStack
from DirectoryofFunctions import DirectoryFunctions
from time import sleep
import sys
import os

DirectoryofFunctions = DirectoryFunctions()
ongoingfunctype = ''
ongoingfuncid = ''
ongoingTypeofVar = ''
ongoingOperator = ''
#My Stacks 
stackofvarnames = myStack()
stackofvartypes = myStack()
stackofoperators = myStack()
stackofjumps = myStack()

#list  of quadruples, probably modded later
Quadruples = []

# Semantic Cube instantiated
semantics = Semanticcube()


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
        program : PROGRAM ID SEMICOLON programprep program1
        '''   
        p[0] = 'Compiled check' 

    def p_PROGRAMPREP(self,p):
        '''
        programprep :
        '''
        global ongoingfuncid
        global ongoingfunctype
        global DirectoryofFunctions

        ongoingfunctype = 'program'
        ongoingprogramid = p[-2]
        ongoingfuncid = ongoingprogramid
        if DirectoryofFunctions.searchFunc(ongoingfuncid):
            print("Function id already assigned")
        else:
            DirectoryofFunctions.addfunc(ongoingfunctype,ongoingfuncid,0,[],[],0)
            print("Function ", ongoingfuncid, " added, with typing ",ongoingfunctype)



    def p_program1(self,p):
        '''
        program1 : vars functions principal
                | vars functions 
                | principal
        '''   

    #def p_program2(self,p):
    #    '''
    #    program2 : principal
    #    '''   
    # Dunno why i putted this here

    def p_PRINCIPAL(self,p):
        '''
        principal : PRINCIPAL LEFTPAR RIGHTPAR LEFTBR statutes RIGHTBR
        '''   

        global ongoingfunctype,ongoingfuncid, DirectoryofFunctions
        ongoingfunctype = p[1] #The type of main which we assume is the next
        ongoingfuncid = p[1]
        DirectoryofFunctions.addfunc(ongoingfunctype,ongoingfuncid,0,[],[],0)



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

    def p_ASSIGN(self,p): # Si necesita [], se sobreentiende que la expresion es un arreglo
        '''
        assign : ID idgetter EQUAL exp
                | ID idgetter array EQUAL exp
        '''    

    def p_idgetter(self,p):
        '''
        idgetter :
        '''        
        global varid, DirectoryofFunctions,ongoingfuncid
        varid = p[-1]
        if DirectoryofFunctions.searchVar(varid,ongoingfuncid):
            varType = DirectoryofFunctions.getVarType(varid,ongoingfuncid)
            ongoingvar = Variable(varType,varid)
            stackofoperators.push(ongoingvar)
        else:
            print("Uh Oh in adding variables inf function")
            sleep(5)
            sys.exit

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
    #Following the order of precedence, from lowest to highest: OR, AND, Booleans < <= > >= <>,+ -, * / , 
    # assignments variables functions and ( expression ) 

    def p_EXP(self,p):
        '''
        exp : andexp
            | andexp OR andexp
        '''            

    def p_ANDEXP(self,p):
        '''
        andexp : boolexp
            | boolexp AND boolexp
        '''      

    def p_BOOLEXP(self,p):
        '''
        exp : arithexp
            | boolexp1 arithexp
        '''      

    def p_BOOLEXP1(self,p):
        '''
        boolexp1 : arithexp LESSER saveOperator arithexp
            | arithexp LESSERAND saveOperator arithexp
            | arithexp GREATER saveOperator arithexp
            | arithexp GREATERAND saveOperator arithexp
            | arithexp NOTSAME saveOperator arithexp
        '''      

    def p_ARITHEXP(self,p):
        '''
        arithexp : geoexp
            | geoexp PLUS saveOperator geoexp
            | geoexp REST saveOperator geoexp
        '''  

    def p_GEOEXP(self,p):
        '''
        geoexp : assignedexp
            | assignedexp TIMES saveOperator assignedexp
            | assignedexp DIVIDE saveOperator assignedexp
        '''  

    def p_ASSIGNEDEXP(self,p):
        '''
        assignedexp : var1
                    | CTEINT
                    | CTEFLOAT
                    | callFunction
                    | LEFTPAR exp RIGHTPAR
        '''  

    def p_SAVEOPERATOR(self,p):
        '''
        saveOperator : 
        '''  
        global ongoingOperator
        ongoingOperator = p[-1]
        stackofoperators.push(ongoingOperator)
        print(stackofoperators.top())


    ##VARS, VARIABBLES AND THEIR DECLARATION WITH CAVEATS ####

    def p_VARS(self,p):
        '''
        vars : VARS vars1
            | empty
        '''            

    def p_VARS1(self,p):
        '''
        vars1 : vars1 typing COLON vars2 SEMICOLON addVar
                | empty
        '''            

    def p_VARS2(self,p):
        '''
        vars2 : ID
                | ID array
                | ID COMMA vars2 addVar
                | ID array COMMA vars2 addVar
                | empty
        '''     
        global varid
        varid   = p[1]  # The next one   


    def p_ADDVAR(self,p):
        '''
        addVar : 
        '''       
        global DirectoryofFunctions,varid, ongoingTypeofVar
        if DirectoryofFunctions.searchFunc(ongoingfuncid):
            DirectoryofFunctions.addVar(ongoingfuncid,ongoingTypeofVar,varid)
            Data= Variable(ongoingTypeofVar,varid)
            stackofoperators.push(Data)
        else:
            print("Uh Oh in adding variables in expressions")
            sleep(3)
            sys.exit


    def p_TYPING(self,p):
        '''
        typing : INT saveTypeofVar
                | CHAR saveTypeofVar
                | FLOAT saveTypeofVar
        '''            

    def p_SAVETYPEOFVAR(self,p):
        '''
        saveTypeofVar :
        '''
        global ongoingTypeofVar
        ongoingTypeofVar = p[-1]
        #print("Type of variable is ", ongoingTypeofVar)

    def p_ARRAY(self,p):
        '''
        array : LEFTSQR exp RIGHTSQR
                | LEFTSQR CTEINT RIGHTSQR
        '''            

    ### FUNCTION, VOIDS AND TYPED RESULTS ON RETURNS #####

    def p_FUNCTIONS(self,p):
        '''
        functions : FUNCTION VOID functions1 functions
                    | FUNCTION INT functions1 functions
                    | FUNCTION FLOAT functions1 functions
                    | FUNCTION CHAR functions1 functions
                    | empty
        '''            

    def p_FUNCTIONS1(self,p):
        '''
        functions1 : ID saveFunc LEFTPAR args RIGHTPAR vars LEFTBR statutes RIGHTBR functions1
                    | empty
        '''            
   
    def p_SAVEFUNC(self,p):
        '''
        saveFunc :
        '''
        global ongoingfunctype, ongoingfuncid, DirectoryofFunctions
        ongoingfunctype = p[-2]
        ongoingfuncid = p[-1]
        DirectoryofFunctions.addfunc(ongoingfunctype,ongoingfuncid,0,[],[],0)

    def p_ARGS(self,p):
        '''
        args : typing COLON args1
            | empty
        '''            

    def p_ARGS1(self,p):
        '''
        args1 : ID
                    | ID COMMA args1
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