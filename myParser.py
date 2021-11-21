#Parser by Andres Carlos Barrera A00815749
#Parser using Lexer and PLY
from myLexer import *
import ply.yacc as yacc
from Vartables import Variable, Vartables, TemporalVar
from Semanticcube import Semanticcube
from Quadruples import Quadruples as Quads
from myStack import myStack
from DirectoryofFunctions import DirectoryFunctions
from memorymap import Memorymap, VirtualMemory
from time import sleep
import sys
import os


#Function tables and variables keeping track of their current and ongoing data
DirectoryofFunctions = DirectoryFunctions()
Virtualmem = Memorymap()
ongoingfunctype = ''
ongoingfuncid = ''
parameterid = ''
callid = ''
#
ongoingTypeofVar = ''
ongoingOperator = ''
t, cte
#

#My Stacks 
stackofvarnames = myStack()
stackofvartypes = myStack()
stackofoperators = myStack()
combinedstackofvar = myStack()
stackofjumps = myStack()


#list  of quadruples, probably modded later, added the temporal variables
Quadruples = Quads()
Quads2 = []
tvars = TemporalVar()

# Semantic Cube instantiated
semantics = Semanticcube()

#Auxiliary counters and lists (memory, parameters, jumps addresses, functions)
CounterParams = 0
JumpENDPROC = 0
waiting = 0
functions = []
endprocess = []
constantstab = []
TemporalsDictionary = {}
initialparameter = 0
temporalsCounter = 0

#Global methods
def QuadCycle(endo,cont):
    global Quadruples
    auxQuad = Quadruples.getQuadAdd(endo)
    Quadruples.changeQuad(auxQuad['Operator'],auxQuad['LeftOperand'],auxQuad['RightOperand'],len(Quadruples.Quads),endo)
    #print ("Quad cycled",  Quadruples.Quads[endo])

def genQuad():
    global stackofoperators,stackofvarnames,stackofvartypes, Quadruples, temporalsCounter,TemporalsDictionary
    if(stackofoperators.length()> 0):
        operator = stackofoperators.pop()
        RightOperand = stackofvarnames.pop()
        RightOpType = stackofvartypes.pop()
        LeftOperand = stackofvarnames.pop()
        LeftOpType = stackofvartypes.pop()

        actualoperator = Virtualmem.getOper(operator)
        sensor = semantics.getType(LeftOpType,RightOpType,operator)
        if sensor != 'ERROR':
            varresult = tvars.next()
            tempaddr = Virtualmem.assignVirtualMemory('TempVars',sensor)
            temporalsCounter+=1
            newQuad = (actualoperator,LeftOperand,RightOperand,tempaddr)
            Quads2.append(newQuad)
            Quadruples.addQuad(actualoperator,LeftOperand,RightOperand,tempaddr)
            stackofvarnames.push(tempaddr)
            stackofvartypes.push(sensor)
        else:
            print ('Type semantic error mismatch')
    else:
        print('Operator stack is empty')

def searchConst(constant):
    for x in constantstab:
        if x['ConstantVar'] == constant:
            return True
    return False

def getConstantAddress(constant):
    for x in constantstab:
        if x['ConstantVar'] == constant:
            return x['VirtualAddr']
    print("Error")

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
        p[0] = 'Compiled check' # Test revision

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
            DirectoryofFunctions.addfunc(ongoingfunctype,ongoingfuncid,0,[],[],0,-1,0)
            print("Function ", ongoingfuncid, " added, with typing ",ongoingfunctype)

    def p_program1(self,p):
        '''
        program1 : vars mainquad functions jumpprogram principal
                | vars mainquad functions 
                | principal
        '''   

    def p_PRINCIPAL(self,p):
        '''
        principal : PRINCIPAL LEFTPAR storefunction RIGHTPAR LEFTBR vars statutes RIGHTBR
        '''   
        #global ongoingfunctype,ongoingfuncid, DirectoryofFunctions
        #ongoingfunctype = p[1] #The type of main which we assume is the next
        #ongoingfuncid = p[1]
        #DirectoryofFunctions.addfunc(ongoingfunctype,ongoingfuncid,0,[],[],0)
        #alternative way of dealing with the main and program distinctions damn

    def p_MAINQUAD(self,p):
        '''
        mainquad :
        '''
        global stackofjumps, Quadruples
        actualoperator = Virtualmem.getOper('GOTOMAIN')
        newQuad = (actualoperator,'PRINCIPAL', -1, None)
        Quadruples.addQuad(newQuad)
        Quads2.append(newQuad)
        stackofjumps.push(len(Quadruples)-1)

    def p_JUMPPROGRAM(self,p):
        '''
        jumpprogram :
        '''
        endo = stackofjumps.pop()
        QuadCycle(endo,-1)

    
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

    def p_IDGETTER(self,p):
        '''
        idgetter :
        '''        
        global varid, DirectoryofFunctions,ongoingfuncid,stackofvartypes, stackofvarnames
        varid = p[-1] #The previous token
        varaddr = DirectoryofFunctions.getaddID(ongoingfuncid,varid)
        if DirectoryofFunctions.searchVar(varid,ongoingfuncid) and not varid == None:
            varType = DirectoryofFunctions.getVarType(varid,ongoingfuncid)
            stackofvartypes.push(varType)
            stackofvarnames.push(varaddr)
        else:
            print("Uh Oh in adding variables inf function")
            sleep(5)
            sys.exit

    def p_IDGETTERARRAY(self,p): #Array token handler
        '''
        idgetterarray :
        '''        
        global varid, DirectoryofFunctions,ongoingfuncid,stackofvartypes,stackofvarnames
        varid = p[-2] #The previous previous token only handle a dimension
        if DirectoryofFunctions.searchVar(varid,ongoingfuncid) and not varid == None:
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
        global stackofvarnames, stackofvartypes, stackofoperators, Quadruples, ongoingfuncid

        if(stackofoperators.length() > 0):
            if (stackofoperators.top() == '='):
                actualoperator = stackofoperators.pop()
                RightOperand = stackofvarnames.pop()
                RightOpType = stackofvartypes.pop()
                LeftOperand = stackofvarnames.pop()
                LeftOpType = stackofvartypes.pop()
                resultsensor = semantics.getType(LeftOpType,RightOpType,actualoperator)
                if resultsensor != 'ERROR':
                    quadoperator = Virtualmem.getOper(actualoperator)
                    newQuad = (quadoperator, RightOperand, None, LeftOperand) 
                    Quadruples.addQuad(quadoperator,RightOperand,None,LeftOperand)
                    Quads2.append(newQuad)
                else:
                    print ('Semantic error')
                    sleep(3)
                    sys.exit


    # FUNCTIONS SECTIONS

    def p_CALLFUNCTION(self,p):
        '''
        callFunction : ID checkid eraquad LEFTPAR paramexp checkparam RIGHTPAR quadgosub
        ''' 
        global callid
        callid = p[1]           

    def p_CHECKID(self,p):
        '''
        checkid:
        '''
        global callid
        callid = p[-1]
        ongoingfuncid= p[-1]
        if DirectoryofFunctions.searchFunc(ongoingfuncid):
            print("Function found")
        else:
            print("Function not found or does not exist")
            sleep(3)
            sys.exit()

    def p_ERAQUAD(self,p):
        '''
        eraquad :
        '''
        global Quadruples, CounterParams
        nameofVar = p[-2]
        actualoperator = Virtualmem.getOper('ERA')
        newQuad = (actualoperator,None,None,nameofVar)
        Quadruples.append(newQuad)

    def p_PARAMEXP(self,p): #Auxiliar exp handler for parameters
        '''
        paramexp : exp paramquad paramaux
                | exp paramquad COMMA paramaux paramexp
                | empty
        '''

    def p_PARAMAUX(self,p):
        '''
        paramaux :
        '''
        global CounterParams
        CounterParams += 1

    def p_PARAMQUAD(self,p):
        '''
        paramquad : 
        '''
        global Quadruples,ongoingfuncid,callid, CounterParams
        actualname = stackofvarnames.pop()
        actualtype = stackofvartypes.pop()
        typeparameters = DirectoryofFunctions.getTypePar(callid)
        #nameparameters = DirectoryofFunctions.getnameofPar(callid)
        criterion = DirectoryofFunctions.getaddID(ongoingfuncid,actualname)
        if CounterParams >= len(typeparameters):
            print("Function parameter length does not match")
            sleep(3)
            sys.exit()
        if actualtype != typeparameters[CounterParams]:
            print("Function parameter type does not match")
            sleep(3)
            sys.exit()
        actualoperator = Virtualmem.getOper('PARAM')
        newQuad = (actualoperator, criterion,actualname,'PARAM'+ str(CounterParams+1))
        stackofoperators.push('PARAM')
        Quadruples.addQuad(actualoperator,criterion,actualname,'PARAM'+str(CounterParams+1))
        Quads2.append(newQuad)

    def p_CHECKPARAM(self,p):
        '''
        checkparam :
        '''
        global CounterParams, callid
        numberofparams = DirectoryofFunctions.getnumPar(callid)
        if numberofparams != CounterParams :
            print ("Error in number of parameters handled")
            sleep(3)
            sys.exit()
        CounterParams = 0

    def p_QUADGOSUB(self,p):
        '''
        quadgosub :
        '''
        global Quadruples, callid, functions
        actualoperator = Virtualmem.getOper('GOSUB')
        newquad = (actualoperator,callid,None,DirectoryofFunctions.getaddstart(callid))
        Quads2.append(newquad)
        Quadruples.addQuad(actualoperator,callid,None,DirectoryofFunctions.getaddstart(callid))

    #def p_ENDPROCLOG(self,p):
    #    '''
    #    endproclog :
    #    '''
    #    global endprocess, JumpENDPROC
    #    endo = endprocess.pop()
    #    aux = list(Quadruples[endo])
    #    aux[3] = JumpENDPROC
    #    Quadruples [endo] = tuple(aux)

    #def p_FUNCERA(self,p):
    #    '''
    #    funcera :
    #    '''
    #    global Quadruples, CounterParams, nameofvar, paramsk
    #    nameofvar= p[-2]
    #    actualoperator = Virtualmem.getOper('ERA')
    #    newQuad = (actualoperator,None,None,nameofvar)
    #    Quadruples.addQuad(actualoperator,None,None,nameofvar)
    #    Quads2.append(newQuad)

    #Reading section

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
        global stackofoperators
        stackofoperators.push('read')

    def p_READINGQUAD(self,p):
        '''
        readingquad :
        '''
        global stackofoperators
        if stackofoperators.length() > 0 and stackofoperators.top() == 'read':
            actualoperator = stackofoperators.pop()
            addressoperator = Virtualmem.getOper(actualoperator)
            valtoread = stackofvarnames.pop()
            stackofvartypes.pop()
            newQuad = (addressoperator, None,None,valtoread)
            Quads2.append(newQuad)
            Quadruples.addQuad(addressoperator,None,None,valtoread)
             
    #Write section

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
        global stackofoperators
        stackofoperators.push('write')

    def p_WRITINGQUAD(self,p):
        '''
        writingquad : 
        '''
        global stackofoperators
        if stackofoperators.length() > 0 and stackofoperators.top() == 'write':
            actualoperator = stackofoperators.pop()
            addressoperator = Virtualmem.getOper(actualoperator)
            valtowrite = stackofvarnames.pop()
            stackofvartypes.pop()
            newQuad = (addressoperator, None, None, valtowrite)
            Quads2.append(newQuad)
            Quadruples.addQuad(addressoperator,None,None,valtowrite)

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
        global stackofvarnames,stackofvartypes, Quadruples,stackofjumps
        typecheck = stackofvartypes.pop()
        if typecheck == 'bool':
            valtoif = stackofvarnames.pop()
            actualoperator = Virtualmem.getOper('GOTOF')
            newQuad = (actualoperator, valtoif, None, -1)
            Quads2.append(newQuad)
            Quadruples.addQuad(actualoperator,valtoif,None,-1)
            stackofjumps.push(len(Quadruples.Quads) - 1)
        else:
            print('Semantic error ')
            return


    def p_ENDIF(self,p):
        '''
        endif :
        '''
        global stackofjumps
        endo = stackofjumps.pop()
        QuadCycle(endo,-1)

    def p_QUADELSE(self,p):
        '''
        quadelse : 
        '''
        global Quadruples, stackofjumps
        actualoperator = Virtualmem.getOper('GOTO')
        newQuad= (actualoperator, None,None,-1)
        Quads2.append(newQuad)
        Quadruples.addQuad(actualoperator,None,None,-1)
        aux = stackofjumps.pop()
        stackofjumps.push(len(Quadruples.Quads) - 1)
        QuadCycle(aux, -1)



    #### CYCLES AND REPETITIONS####
    def p_ENDOFLOOP(self,p):
        '''
        endofloop :
        '''
        global stackofvarnames, stackofvartypes, Quadruples,stackofjumps
        endo = stackofjumps.pop()
        starto = stackofjumps.pop()
        actualoperator = Virtualmem.getOper('GOTO')
        newQuad = (actualoperator, None, None, starto)
        Quads2.append(newQuad)
        Quadruples.addQuad(actualoperator,None,None,starto)
        QuadCycle(endo,-1)


    def p_FOR(self,p):
        '''
        for : FOR auxfor assign TO CTEINT DO quadfor LEFTBR statutes RIGHTBR endofloop
        '''            

    def p_AUXFOR(self,p):
        '''
        auxfor :
        '''
        global stackofoperators, Quadruples, stackofjumps
        stackofoperators.push('for')
        stackofjumps.push(len(Quadruples.Quads))

    def p_QUADFOR(self,p):
        '''
        quadfor :
        '''
        global stackofoperators, Quadruples, stackofjumps
        typecheck = stackofvartypes.pop()
        if (typecheck == 'bool'):
            valtofor = stackofvarnames.pop()
            actualoperator = Virtualmem.getOper('GOTOV')
            newQuad = (actualoperator,valtofor,None,-1)
            Quads2.append(newQuad)
            Quadruples.addQuad(actualoperator,valtofor,None,-1)
            stackofjumps.push(len(Quadruples.Quads)-1)
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
        global stackofoperators,Quadruples,stackofjumps
        stackofoperators.push('while')
        stackofjumps.push(len(Quadruples.Quads))


    def p_QUADWHILE(self,p):
        '''
        quadwhile :
        '''
        global stackofvarnames, stackofvartypes, Quadruples, stackofjumps
        typecheck = stackofvartypes.pop()
        if typecheck == 'bool':
            valtowhile = stackofvarnames.pop()
            actualoperator = Virtualmem.getOper('GOTOF')
            newQuad = (actualoperator, valtowhile,None, -1)
            Quads2.append(newQuad)
            Quadruples.addQuad(actualoperator,valtowhile,None,-1)
            stackofjumps.push(len(Quadruples.Quads)-1)
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
        global stackofoperators
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
        global stackofoperators
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
        quadbool :
        '''
        global stackofoperators
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
        global stackofoperators
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
        global stackofoperators
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
                    | ID array idgetterarray
                    | empty
        '''  

    def p_CTEAUX(self,p):
        '''
        cteaux :
        '''
        global cte, t
        cte = p[-1]
        t = type(cte)
        if t == int:
            stackofvartypes.push('Int')
            if not searchConst(cte):
                virtualaddr = Virtualmem.assignVirtualMemory('ConstantVars','Int')
                constantstab.append({
                    'ConstantVar' : cte,
                    'VirtualAddr' : virtualaddr
                })
            else:
                virtualaddr = getConstantAddress(cte)
            stackofvarnames.push(virtualaddr)
        elif t == float:
            stackofvartypes.push('Float')
            if not searchConst(cte):
                virtualaddr = Virtualmem.assignVirtualMemory('ConstantVars','Float')
                constantstab.append({
                    'ConstantVar' : cte,
                    'VirtualAddr' : virtualaddr
                })
            else:
                virtualaddr = getConstantAddress(cte)
            stackofvarnames.push(virtualaddr)
        else:
            stackofvartypes.push('Char')
            if not searchConst(cte):
                virtualaddr = Virtualmem.assignVirtualMemory('ConstantVars','Char')
                constantstab.append({
                    'ConstantVar' : cte,
                    'VirtualAddr' : virtualaddr
                })
            else:
                virtualaddr = getConstantAddress(cte)
            stackofvarnames.push(virtualaddr)


    def p_OPERATORHANDLER(self,p):
        '''
        operatorhandler : 
        '''  
        global stackofoperators
        actualoperator = p[-1] #Always the before token
        stackofoperators.push(actualoperator)
        print(stackofoperators.top())


    ##VARS, VARIABBLES AND THEIR DECLARATION WITH CAVEATS ####

    def p_VARS(self,p):
        '''
        vars : vars0
            | empty
        '''            

    def p_VARS0(self,p): #Some errors at an empty vars or not declaration
        '''
        vars0 : VARS vars1
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
        if (ongoingfuncid == 'program'):
            virtualaddr = Virtualmem.assignVirtualMemory('GlobalVars',ongoingTypeofVar)
        else:
            virtualaddr = Virtualmem.assignVirtualMemory('LocalVars',ongoingTypeofVar)
        if not varid == None:
            if DirectoryofFunctions.searchFunc(ongoingfuncid):
                DirectoryofFunctions.addVar(ongoingfuncid,ongoingTypeofVar,varid,virtualaddr)
                Data=Variable(ongoingTypeofVar,varid)
                combinedstackofvar.push(Data)
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
        functions : FUNCTION VOID functions1 funcend functions
                    | FUNCTION INT functions1 funcend functions
                    | FUNCTION FLOAT functions1 funcend functions
                    | FUNCTION CHAR functions1 funcend functions
                    | empty
        '''            

    def p_FUNCTIONS1(self,p):
        '''
        functions1 : ID storefunct LEFTPAR args RIGHTPAR vars LEFTBR setaddstart statutes RIGHTBR 
                    | empty
        '''            
   
    def p_SETADDSTART(self,p):
        '''
        setaddstart : 
        '''
        global ongoingfuncid
        DirectoryofFunctions.setAddstart(ongoingfuncid,len(Quadruples.Quads))

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
        args : args1
            | empty
        '''            

    def p_ARGS1(self,p):
        '''
        args1 : INT saveTypeofVar COLON ID mulParam nextParam
                | FLOAT saveTypeofVar COLON ID mulParam nextParam
                | CHAR saveTypeofVar COLON ID mulParam nextParam
        '''            

    def p_NEXTPARAM(self,p):
        '''
        nextParam : COMMA args1
                | empty
        '''

    def p_MULPARAM(self,p):
        '''
        mulParam :
        '''
        global DirectoryofFunctions, parameterid, initialparameter, ongoingTypeofVar
        parameterid = p[-1]
        initialparameter = 1
        if not parameterid == None:
            if DirectoryofFunctions.searchFunc(ongoingfuncid):
                virtualaddr = Virtualmem.assignVirtualMemory('LocalVars', ongoingTypeofVar)
                DirectoryofFunctions.addPar(ongoingfuncid,parameterid,ongoingTypeofVar)
                DirectoryofFunctions.addVar(ongoingfuncid,ongoingTypeofVar,parameterid,virtualaddr)
            else:
                print("Uh oh in managin function parameters")
                sleep(3)
                sys.exit()

    def p_FUNCEND(self,p):
        '''
        funcend :
        '''
        global Quadruples,temporalsCounter, ongoingfuncid,DirectoryofFunctions
        actualoperator = Virtualmem.getOper('ENDPROC')
        newQuad = (actualoperator,None,None,-1)
        Quads2.append(newQuad)
        Quadruples.addQuad(actualoperator,None,None,-1)
        actualvars = DirectoryofFunctions.getnumPar(ongoingfuncid)
        DirectoryofFunctions.setMagnitude(ongoingfuncid, actualvars + temporalsCounter)
        Virtualmem.resetLocalMemory()
        tvars.reset()
        temporalsCounter = 0

    def p_STOREFUNCT(self,p):
        '''
        storefunct :
        '''
        global ongoingfunctype, ongoingfuncid, DirectoryofFunctions
        ongoingfunctype = p[-2]
        ongoingfuncid = p[-1]
        DirectoryofFunctions.addfunc(ongoingfunctype,ongoingfuncid,0,[],[],0,-1,0)
        
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