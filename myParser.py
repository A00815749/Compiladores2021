#Parser by Andres Carlos Barrera A00815749
#Parser using Lexer and PLY
from myLexer import *
import ply.yacc as yacc
from Vartables import Variable, Vartables, TemporalVar
from Semanticcube import Semanticcube
from myStack import myStack
from DirectoryofFunctions import DirectoryFunctions
from time import sleep
import sys
import os


#Function tables and variables keeping track of their current and ongoing data
DirectoryofFunctions = DirectoryFunctions()
ongoingfunctype = ''
ongoingfuncid = ''
ongoingTypeofVar = ''
ongoingOperator = ''
global constant, t
#My Stacks 
stackofvarnames = myStack()
stackofvartypes = myStack()
stackofoperators = myStack()
stackofjumps = myStack()

#list  of quadruples, probably modded later, added the temporal variables
Quadruples = []
tvars = TemporalVar()

# Semantic Cube instantiated
semantics = Semanticcube()

#Global methods
def QuadCycle(endo,cont):
        aux = list(Quadruples[endo])
        aux[3] = len(Quadruples)
        Quadruples[endo] = tuple(aux)
        #print ("Quad cycled", quadruples[endo])

def genQuad():
    if(stackofoperators.length()> 0):
        operator = stackofoperators.pop()
        RightOperand = stackofvarnames.pop()
        RightOpType = stackofvartypes.pop()
        LeftOperand = stackofvarnames.pop()
        LeftOpType = stackofvartypes.pop()
        sensor = semantics.getType(LeftOpType,RightOpType,operator)
        if sensor != 'ERROR':
            varresult = tvars.next()
            newQuad = (operator,LeftOperand,RightOperand,varresult)
            Quadruples.append(newQuad)
            stackofvarnames.push(varresult)
            stackofvartypes.push(sensor)
        else:
            print ('Type semantic error mismatch')
    else:
        print('Operator stack is empty')

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
        ongoingfuncid = 'program'  #decided to follow advice and put the function name, which a program is a very big and important instance as their ids
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
        principal : PRINCIPAL LEFTPAR storefunction RIGHTPAR LEFTBR statutes RIGHTBR
        '''   

        
        
        #global ongoingfunctype,ongoingfuncid, DirectoryofFunctions
        #ongoingfunctype = p[1] #The type of main which we assume is the next
        #ongoingfuncid = p[1]
        #DirectoryofFunctions.addfunc(ongoingfunctype,ongoingfuncid,0,[],[],0)
        #alternative way of dealing with the main and program distinctions damn



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
        assign : ID idgetter EQUAL operatorhandler exp assignquad
                | ID idgetter array EQUAL operatorhandler exp assignquad
        '''    

    def p_idgetter(self,p):
        '''
        idgetter :
        '''        
        global varid, DirectoryofFunctions,ongoingfuncid,stackofvartypes, stackofvarnames
        varid = p[-1] #plhold and debugger
        if DirectoryofFunctions.searchVar(varid,ongoingfuncid):
            varType = DirectoryofFunctions.getVarType(varid,ongoingfuncid)
            stackofvartypes.push(varType)
            stackofvarnames.push(varid)
        else:
            print("Uh Oh in adding variables inf function")
            sleep(5)
            sys.exit


    def p_assignquad(self,p):
        '''
        assignquad :
        '''
        global stackofvarnames, stackofvartypes, stackofoperators, Quadruples
        if(stackofoperators.length() > 0):
            if (stackofoperators.top() == '='):
                actualoperator = stackofoperators.pop()
                RightOperand = stackofvarnames.pop()
                RightOpType = stackofvartypes.pop()
                LeftOperand = stackofvarnames.pop()
                LeftOpType = stackofvartypes.pop()
                resultsensor = semantics.getType(LeftOpType,RightOpType,actualoperator)
                if resultsensor != 'ERROR':
                    newQuad = (actualoperator, RightOperand, None, LeftOperand) 
                    Quadruples.append(newQuad)
                else:
                    print ('Semantic error')
                    sleep(3)
                    sys.exit




    def p_CALLFUNCTION(self,p):
        '''
        callFunction : ID LEFTPAR exp RIGHTPAR
        '''            







    def p_READING(self,p):
        '''
        reading : READ auxreading LEFTPAR reading1 RIGHTPAR
        '''            

    def p_READING1(self,p):
        '''
        reading1 : reading2
                | empty
        '''            

    def p_READING2(self,p):
        '''
        reading2 : exp readingquad
                | exp readingquad COMMA auxreading reading2
        '''            

    def p_AUXREADING(self,p):
        '''
        auxreading : 
        '''
        stackofoperators.push('read')

    def p_READINGQUAD(self,p):
        '''
        readingquad :
        '''
        if stackofoperators.length() > 0 and stackofoperators.top() == 'read':
            actualoperator = stackofoperators.pop()
            valtoread = stackofvarnames.pop()
            stackofvartypes.pop()
            newQuad = (actualoperator, None,None,valtoread)
            Quadruples.append(newQuad)
             





    def p_WRITING(self,p):
        '''
        writing : WRITE auxwriting LEFTPAR writing1 RIGHTPAR
        '''            

    def p_WRITING1(self,p):
        '''
        writing1 : writing2
                | empty
        '''            

    def p_WRITING2(self,p):
        '''
        writing2 : exp writingquad
                | exp writingquad COMMA auxwriting writing2
        '''            

    def p_AUXWRITING(self,p):
        '''
        auxwriting : 
        '''
        stackofoperators.push('write')

    def p_WRITINGQUAD(self,p):
        '''
        writingquad : 
        '''
        if stackofoperators.length() > 0 and stackofoperators.top() == 'write':
            actualoperator = stackofoperators.pop()
            valtowrite = stackofvarnames.pop()
            stackofvartypes.pop()
            newQuad = (actualoperator, None, None, valtowrite)
            Quadruples.append(newQuad)

    def p_MEDIA(self,p):
        '''
        media : MEDIA LEFTPAR array RIGHTPAR SEMICOLON
        '''            

    # Method for cycles and decision auxiliary managing quadruples and duplication
    #def QuadCycle(endo,cont):
    #    aux = list(Quadruples[endo])
    #    aux[3] = len(Quadruples)
    #    Quadruples[endo] = tuple(aux)
    #    #print ("Quad cycled", quadruples[endo])





    ####### DECISIONS  #########

    def p_IF(self,p):
        '''
        if : IF LEFTPAR exp RIGHTPAR quadif THEN LEFTBR statutes RIGHTBR else endif
        '''            

    def p_ELSE(self,p):
        '''
        else : ELSE quadelse LEFTBR statutes RIGHTBR
                | empty
        '''            

    def p_QUADIF(self,p):
        '''
        quadif :
        '''
        typecheck = stackofvartypes.pop()
        if typecheck == 'bool':
            valtoif = stackofvarnames.pop()
            newQuad = ('GotoF', valtoif, None, -1)
            Quadruples.append(newQuad)
            stackofjumps.push(len(Quadruples) - 1)
        else:
            print('Semantic error ')
            return


    def p_ENDIF(self,p):
        '''
        endif :
        '''
        endo = stackofjumps.pop()
        QuadCycle(endo,-1)

    def p_QUADELSE(self,p):
        '''
        quadelse : 
        '''
        newQuad= ('Goto', None,None,-1)
        Quadruples.append(newQuad)
        aux = stackofjumps.pop()
        stackofjumps.push(len(Quadruples) - 1)
        QuadCycle(aux, -1)



    #### CYCLES AND REPETITIONS####
    def p_ENDOFLOOP(self,p):
        '''
        endofloop :
        '''
        endo = stackofjumps.pop()
        starto = stackofjumps.pop()
        newQuad = ('Goto', None, None, starto)
        Quadruples.append(newQuad)
        QuadCycle(endo,-1)


    def p_FOR(self,p):
        '''
        for : FOR auxfor assign TO CTEINT DO quadfor LEFTBR statutes RIGHTBR endofloop
        '''            

    def p_AUXFOR(self,p):
        '''
        auxfor :
        '''
        stackofoperators.push('for')
        stackofjumps.push(len(Quadruples))

    def p_QUADFOR(self,p):
        '''
        quadfor :
        '''
        typecheck = stackofvartypes.pop()
        if (typecheck == 'bool'):
            valtofor = stackofvarnames.pop()
            newQuad = ('GotoV',valtofor,None,-1)
            Quadruples.append(newQuad)
            stackofjumps.push(len(Quadruples)-1)
        else:
            print ("Semantic error in For")
            sys.exit


    def p_WHILE(self,p):
        '''
        while : WHILE auxwhile LEFTPAR exp RIGHTPAR DO quadwhile LEFTBR statutes RIGHTBR endofloop
        '''            

    def p_AUXWHILE(self,p):
        '''
        auxwhile :
        '''
        stackofoperators.push('while')
        stackofjumps.push(len(Quadruples))


    def p_QUADWHILE(self,p):
        '''
        quadwhile :
        '''
        typecheck = stackofvartypes.pop()
        if typecheck == 'bool':
            valtowhile = stackofvarnames.pop()
            newQuad = ('GotoF', valtowhile,None, -1)
            Quadruples.append(newQuad)
            stackofjumps.push(len(Quadruples)-1)
        else:
            print ('Semantic Error in while')
            sys.exit()

    ###ARITHMETIC, EXPRESSIONS AND THE LIKE ####
    #Following the order of precedence, from lowest to highest: OR, AND, Booleans < <= > >= <>,+ -, * / , 
    # assignments variables functions and ( expression ) 

    def p_EXP(self,p):
        '''
        exp : andexp quador
            | andexp quador OR operatorhandler andexp
        '''            

    def p_QUADOR(self,p):
        '''
        quador :
        '''
        if stackofoperators.length() > 0 and stackofoperators.top() == '|':
            genQuad()




    def p_ANDEXP(self,p):
        '''
        andexp : boolexp quadand
            | boolexp quadand AND operatorhandler boolexp
        '''      

    def p_QUADAND(self,p):
        '''
        quadand :
        '''
        if stackofoperators.length() > 0 and stackofoperators.top() == '&':
            genQuad()



    def p_BOOLEXP(self,p):
        '''
        exp : arithexp 
            | boolexp1 arithexp
        '''      

    def p_BOOLEXP1(self,p):
        '''
        boolexp1 : arithexp LESSER operatorhandler arithexp quadbool
            | arithexp LESSERAND operatorhandler arithexp quadbool
            | arithexp GREATER operatorhandler arithexp quadbool
            | arithexp GREATERAND operatorhandler arithexp quadbool
            | arithexp NOTSAME operatorhandler arithexp quadbool
        '''      

    def p_QUADBOOL(self,p):
        '''
        quadnool :
        '''
        if stackofoperators.length() > 0:
            if stackofoperators.top() == '<' or stackofoperators.top() == '<=' or stackofoperators.top() == '>' or stackofoperators.top() == '>=' or stackofoperators.top() == '==' or stackofoperators.top() == '<>':
                genQuad()



    def p_ARITHEXP(self,p):
        '''
        arithexp : geoexp
            | geoexp PLUS operatorhandler geoexp quadarith
            | geoexp REST operatorhandler geoexp quadarith
        '''  

    def p_QUADARITH(self,p):
        '''
        quadarith :
        '''
        if stackofoperators.length() > 0 and (stackofoperators.top() == '+' or stackofoperators.top() == '-'):
            genQuad()


    def p_GEOEXP(self,p):
        '''
        geoexp : assignedexp
            | assignedexp TIMES operatorhandler assignedexp quadgeo
            | assignedexp DIVIDE operatorhandler assignedexp quadgeo
        '''  

    def p_QUADGEO(self,p):
        '''
        quadgeo :
        '''
        if stackofoperators.length() > 0 and (stackofoperators.top() == '*' or stackofoperators.top() == '/'):
            genQuad()


    def p_ASSIGNEDEXP(self,p):
        '''
        assignedexp : ID idgetter
                    | CTEINT cteaux
                    | CTEFLOAT cteaux
                    | CTECHAR cteaux
                    | CTESTRING cteaux
                    | callFunction
                    | LEFTPAR exp RIGHTPAR
        '''  

    def p_CTEAUX(self,p):
        '''
        cteaux :
        '''
        global constant, t
        constant = p[-1]
        t = type(constant)
        if t == int:
            stackofvartypes.push('int')
            stackofvarnames.push(constant)
        elif t == float:
            stackofvartypes.push('float')
            stackofvarnames.push(constant)
        else:
            stackofvartypes.push('char')
            stackofvarnames.push(constant)


    def p_OPERATORHANDLER(self,p):
        '''
        saveOperator : 
        '''  
        global ongoingOperator
        ongoingOperator = p[-1] #Always the before token
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