#Parser by Andres Carlos Barrera A00815749
#Parser using Lexer and PLY
from re import split
from typing import Match
from myLexer import *
import ply.yacc as yacc
from Vartables import Variable, Vartables, TemporalVar
from Semanticcube import Semanticcube
from Quadruples import Quadruples as altQuads
from myStack import myStack
from DirectoryofFunctions import DirectoryFunctions
from memorymap import Memorymap, VirtualMemory
from time import sleep
import sys
import os

##################-------GLOBAL VARIABLES AND METHODS ------------##########################

##### PYTHON SETS, MUTABLE, ORDER OF ELEMENTS NOT IMPORTANT#############

THETABLEoffunctions = {}
THEGLOBALVARset = {}
THELOCALVARset = {}
THEPARAMETERSset = {}
THECONSTANTSset = {}
#BASEMATHsymbols = {'+','-','*','/'}
#BOOLMATHsymbols = {'>','>=','<','<=','==','<>'}
#LOGICMATHsymbols = {'and','or'}
HASHOFOPERATORSINquads = {
    '+' : 1,
    '-' : 2,
    '*' : 3,
    '/' : 4,
    '>' : 5,
    '>=' : 6,
    '<' : 7,
    '<=' : 8,
    '==' : 9,
    '<>' : 10,
    '=' : 11,
    'READ' : 12,
    'WRITE' : 13,
    'AND' : 14,
    'OR' : 15,
    'GOTO' : 16,
    'GOTOF' : 17,
    'GOTOV' : 18,
    'ERA' : 19,
    'VER' : 20,
    'ENDPROC' : 21,
    'PARAM' : 22,
    'GOSUB' : 23,
    'MEDIA' : 24,
    'MEDIANA' : 25,
    'MODA' : 26,
    'STDEV' : 27,
    'VARIANZA' : 28,
    'PLOTXY' : 29,
}

##### PYTHON LISTS, MUTABLE, ORDER OF ELEMENTS INHERENT IN THEIR APPLICATION #############

GLOBALNAMESlist = []
LOCALNAMESlist = []
QUADRUPLESlist = []
CONSTANTSlist= []
CONSTANTPARAMETERSlist = []
PARAMETERSTABLElist = []
PARAMETERDIMlist = []
PARAMETERQUEUElist = []
SPECIALMETHODSlist = []
SPECIALMETHODSaux = []


###MY STACKS, I discovered way to late that the pop() in python lists simulate stacks dammit all ########

STACKOFoperands = []
STACKOFoperatorssymb = []
STACKOFtypes = []
STACKOFPENDINGjumps = []

#### SENSORS, CHECKING THE SCOPE (CONTEXT) OF THE VARIABLE  , & COUNTERS
#Arraysensor = False
INITIALVARINfor = 0
FINALVARINfor = 0
temporalsCounter = 0
SPECIALMETHODScounter = -1
CURRENTcontext = 'g'
CURRENTtype = ''
CURRENTfuncname = ''

################ MEMORY MAP FOR VARIABLE, CONSTANT, FUNCTION, TEMPORAL, PARAMETERS AND POINTERS STORAGE ###########
#WHEN a memory block is used, it adds 1 to the counter.
GLOBALINTcounter = 1000 - 1  # BLOCK of 2000 spaces 
GLOBALFLOATcounter = 3000 - 1
GLOBALCHARcounter = 5000 - 1
LOCALINTcounter = 7000 - 1
LOCALFLOATcounter = 9000 - 1
LOCALCHARcounter = 11000 - 1
TEMPINTcounter = 13000 - 1
TEMPFLOATcounter = 15000 - 1
TEMPCHARcounter = 17000 - 1
TEMPBOOLcounter = 19000 - 1
CONSTINTcounter = 21000 - 1
CONSTFLOATcounter = 23000 - 1
CONSTCHARcounter = 25000 - 1
FUNCTIONVIRADDRcounter = 27000 - 1 # BLOCK of 3000 spaces 
PARAMSINTcounter = 30000 - 1
PARAMSFLOATcounter = 33000 - 1
PARAMSCHARcounter = 36000 - 1 # BLOCK of 4000 spaces 
POINTERScounter = 40000 - 1 # LAST BLOCK

############### QUADRUPLE CLASS FOR STORING THE COMPILER OPERATIONS ############

class Quadruple :
    def __init__(self, operator,LeftOperand,RightOperand,result):
        global QUADRUPLESlist
        self.QUADcounter = len(QUADRUPLESlist) + 1 # The number of the quadruple, so that we can have GOTO and derived functions
        self.operator = operator
        self.LeftOperand = LeftOperand
        self.RightOperand = RightOperand
        self.result = result

#### SEMANTIC CUBE CLASS OBJECT, A SENSOR THAR CHECKS OPERATIONS BETWEEN SIMPLEE DATATYPES #############
semantics = Semanticcube()

###### GLOBAL AUXILIAR METHODS FOR NEURALGIC POINTS MANIPULATION ################

def getandsetVirtualAddrFunc(): # SET THE VIRTUAL ADDRESS FOR THE FUNCTION 
    global FUNCTIONVIRADDRcounter
    FUNCTIONVIRADDRcounter += 1
    return FUNCTIONVIRADDRcounter

def ENDANDRESETFunc(): #RESET EVERY LOCAL AND TEMPORAL VARIABLES, INCLUDING POINTERS AND PARAMETERS
    global LOCALCHARcounter,LOCALFLOATcounter,LOCALINTcounter
    global TEMPINTcounter, TEMPFLOATcounter, TEMPCHARcounter, TEMPBOOLcounter, POINTERScounter
    global PARAMSINTcounter, PARAMSFLOATcounter, PARAMSCHARcounter, temporalsCounter
    global CURRENTcontext, THELOCALVARset, LOCALNAMESlist, THEPARAMETERSset,PARAMETERSTABLElist
    LOCALINTcounter = 7000 - 1
    LOCALFLOATcounter = 9000 - 1
    LOCALCHARcounter = 11000 - 1
    TEMPINTcounter = 13000 - 1
    TEMPFLOATcounter = 15000 - 1
    TEMPCHARcounter = 17000 - 1
    TEMPBOOLcounter = 19000 - 1
    PARAMSINTcounter = 30000 - 1
    PARAMSFLOATcounter = 33000 - 1
    PARAMSCHARcounter = 36000 - 1 
    POINTERScounter = 40000 - 1 
    CURRENTcontext = 'g' # RETURN TO THE GLOBAL SCOPE TILL NEXT LOCAL CHANGE
    THELOCALVARset = {} # EMPTY THE LOCAL VARIABLES
    LOCALNAMESlist = [] # EMPTY THE ORDERED USED NAMES
    temporalsCounter = 0 # RESET OUR COUNTER FOR TEMPORALS USED

def getandsetVirtualAddrCTE(value): # VIRTUAL ADDRESS SETER FOR CTES
    global CONSTINTcounter,CONSTFLOATcounter,CONSTCHARcounter
    constanttype = type(value)
    if constanttype == int:
        CONSTINTcounter += 1
        return CONSTINTcounter
    elif constanttype == float:
        CONSTFLOATcounter += 1
        return CONSTFLOATcounter
    elif constanttype == str:
        CONSTCHARcounter += 1
        return CONSTCHARcounter
    else: 
        ERRORHANDLER("type error", str(value)) # SEND THE VALUE THAT WE TRIED TO CONSTANT

def getandsetVirtualAddrVars(type, context): # VIRTUAL ADDRESS SETER FOR VARIABLES
    global GLOBALINTcounter, GLOBALFLOATcounter, GLOBALCHARcounter
    global LOCALINTcounter, LOCALFLOATcounter, LOCALCHARcounter
    if context == 'g':
        if type == 'int':
            GLOBALINTcounter += 1
            return GLOBALINTcounter
        elif type == 'float':
            GLOBALFLOATcounter += 1
            return GLOBALFLOATcounter
        elif type == 'char':
            GLOBALCHARcounter += 1
            return GLOBALCHARcounter
    else:
        if type == 'int':
            LOCALINTcounter += 1
            return LOCALINTcounter
        elif type == 'float':
            LOCALFLOATcounter += 1
            return LOCALFLOATcounter
        elif type == 'char':
            LOCALCHARcounter += 1
            return LOCALCHARcounter


def getandsetVirtualAddrTemp(type): # GET THE VIRTUAL ADDRESS OF OUR TEMPORALS AND POINTERS
    global TEMPINTcounter, TEMPFLOATcounter, TEMPCHARcounter, TEMPBOOLcounter
    global temporalsCounter, POINTERScounter
    temporalsCounter += 1
    if type == 'int':
        TEMPINTcounter += 1
        return TEMPINTcounter
    elif type == 'float':
        TEMPFLOATcounter += 1
        return TEMPFLOATcounter
    elif type == 'char':
        TEMPCHARcounter += 1
        return TEMPCHARcounter
    elif type == 'bool':
        TEMPBOOLcounter += 1
        return TEMPBOOLcounter
    elif type == 'pointer':
        POINTERScounter += 1
        return POINTERScounter

def ERRORHANDLER(errortype,location = ""): # GET THE VARIOUS ERROR MESSAGES HANDLED
    errormessage = ""
    #I could match case here, but I dont want to change python versions midproject
    if errortype == "funcrepetida":
        errormessage = "FUNCION EXISTENTE REPETIDA"
    elif errortype == "nombreusado":
        errormessage = "ID DE VARIABLE Y/O PROGRAMA REPETIDA"
    elif errortype == "invalidoperator":
        errormessage = "OPERACION INVALIDA, MISMATCH DE TIPOS"
    elif errortype == "varrepetida":
        errormessage = "VARIABLE DECLARADA MULTIPLES VECES"
    elif errortype == "tiposdif":
        errormessage = "MISMATCH DE TIPOS"
    elif errortype == "tiposhuh":
        errormessage = "TIPO DE DATO NO ACEPTADO"
    elif errortype == "notype":
        errormessage = "VARIABLE SIN TIPO"
    elif errortype == "noval":
        errormessage = "VARIABLE SIN VALOR"
    elif errortype == "notthere":
        errormessage = "NO EXISTE LA VARIABLE QUE SE BUSCA "
    elif errortype == "type error":
        errormessage = "ERROR EN TIPO DE DATO CONSTANTE"
    elif errortype == "INVALIDOP":
        errormessage = "OPERACION INVALIDA"
    elif errortype == "funcwithparamhuh":
        errormessage = "FUNCION ESPERABA NO PARAMETROS"
    elif errortype == "invalidnumparams":
        errormessage = "FUNCION CON NUMERO DE PARAMETROS ERRONEO"
    elif errortype == "dimshuh":
        errormessage = "VARIABLE VECTOR SIN DIMENSIONES"
    print("ERROR " + errormessage + " at ===> " + str(location))
    sys.exit()

def insertinFunctable(id,type,context, variables): #INSERT THE FUNCTION INTO A UNORDERED SET
    global THETABLEoffunctions, GLOBALNAMESlist, LOCALNAMESlist
    if id in THETABLEoffunctions:
        ERRORHANDLER("funcrepetida") # FUNCTION ALREADY USED 
    elif id in GLOBALNAMESlist:
        ERRORHANDLER("nombreusado") # NAME ALREADY USED
    else:
        THETABLEoffunctions[id] = {'type' : type, 'context' : context, 'variables' : variables}
        GLOBALNAMESlist.append(id)

def insertinVartable(id,virtualaddr,type): #INSERT OUR FORMATTED VAR INSIDE A TABLE SET
    if virtualaddr < 7000:
        if id in GLOBALNAMESlist:
            ERRORHANDLER("nombreusado", str(id + " " + type))
        if id in THEGLOBALVARset:
            ERRORHANDLER("varrepetida",id)
        THEGLOBALVARset[id] = {'virtualaddress': virtualaddr, 'type' : type}
        GLOBALNAMESlist.append(id)
    else:
        if id in LOCALNAMESlist:
            ERRORHANDLER("nombreusado", str(id + " " + type))
        if id in THELOCALVARset:
            ERRORHANDLER("varrepetida",id)
        THELOCALVARset[id] = {'virtualaddress': virtualaddr, 'type' : type}
        LOCALNAMESlist.append(id)

def typechecker(type1,type2): # CHEKCIK IF OUR TYPES ARE ACTUALLY THE SAME, USED IN ASSIGNING, CYCLES AND LOOPS
    if type1 != type2:
        ERRORHANDLER("tiposdif",str(type1 + " ====== " + type2))

def getValtype(val): # RETURN THE VALUE OF THE VARIABLE, FUNCTION... THINGY WE ARE ACCESSING
    if val in THELOCALVARset:
        return THELOCALVARset[val]['type']
    if val in THEGLOBALVARset:
        return THEGLOBALVARset[val]['type']
    if val in THETABLEoffunctions:
        return THETABLEoffunctions[val]['type']
    if type(val) == int:
        return 'int'
    if type(val) == float:
        return 'float'
    if type(val) == str:
        return 'char'

def virtualaddrfetcher(val): #VIRTUAL ADDRESS FETCHER, CHECKING THE APPROPIATE SETS
    global THEGLOBALVARset,THELOCALVARset, THECONSTANTSset
    if val in THELOCALVARset: #IS IT IN THE LOCAL VARS?
        return THELOCALVARset[val]['virtualaddress']
    elif val in THEGLOBALVARset: # IS IT IN THE GLOBAL VARS?
        return THEGLOBALVARset[val]['virtualaddress']
    else: # ASSUMING CONSTANTS
        if type(val) == int:
            return THECONSTANTSset[int(val)]
        if type(val) == float:
            return THECONSTANTSset[float(val)]
        if type(val) == str:
            return THECONSTANTSset[str(val)]

#def asignersets(val1,val2): # METHOD FOR ASIGNING VALUES IN QUADRUPLES, ||||DEPRECATED||||
    #return None

#def isVarsensor(val): #DOES IT EXIST IN OUR VARIABLES SETS |||DEPRECATED||||
    #if val in THEGLOBALVARset or val in THELOCALVARset:
    #    return True
    #else: 
    #    return False

#def getVal(val): # METHOD TO ACCESS VARIABLES SOTRED IN THE SETS ||||DEPRECATED||||
    #return None

def getType(val): #GETTING THE TYPE IN THE FOR NEURALGIC POINTS
    if val in THELOCALVARset: 
        try:
            return THELOCALVARset[val]['type']
        except:
            ERRORHANDLER("notype",val)
    elif val in THEGLOBALVARset:
        try:
            return THEGLOBALVARset[val]['type']
        except:
            ERRORHANDLER("notype",val)
    else:
        ERRORHANDLER("notthere",val) # IF ITS NOT THERE, THEN IT DOES NOT EXIST
        

def existencesensor(id): # METHOD TO CHECK IF THE DATA OF THE CONSTANT IS SAVED
    global THELOCALVARset,THEGLOBALVARset,THECONSTANTSset,THETABLEoffunctions
    if id not in THECONSTANTSset and id not in THEGLOBALVARset and id not in THELOCALVARset and id not in THETABLEoffunctions:
        ERRORHANDLER("notthere",id)

def setvirtualaddrdimensions(context,type,size): # METHOD USED IN DIMENSION MANAGEMENT OF VECTORS
    global GLOBALINTcounter, GLOBALFLOATcounter, GLOBALCHARcounter
    global LOCALINTcounter, LOCALCHARcounter, LOCALFLOATcounter
    if context == 'g':
        if type == 'int':
            GLOBALINTcounter += size
        elif type == 'float':
            GLOBALFLOATcounter += size
        elif type == 'char':
            GLOBALCHARcounter += size
    elif context == 'l':
        if type == 'int':
            LOCALINTcounter += size
        elif type == 'float':
            LOCALFLOATcounter += size
        elif type == 'char':
            LOCALCHARcounter += size
    
def dimensionssensor(id): # METHOD THAT CHECKS IF THE VARIABLES IS ACTUALLY AN ARRAY (OR VECTOR IN THIS LANGUAGE)
    global THEGLOBALVARset, THELOCALVARset
    try:
        THELOCALVARset[id]['arraysensor']
    except:
        try: 
            THEGLOBALVARset[id]['arraysensor']
        except:
            ERRORHANDLER("dimshuh")

def isarraymethod(id): #SIMILAR METHOD TO THE ABOVE, BUT RETURNS A BOOLEAN AND HAS NO ERRORHANDLER
    global THEGLOBALVARset, THELOCALVARset
    try:
        THELOCALVARset[id]['arraysensor']
        return True
    except:
        try: 
            THEGLOBALVARset[id]['arraysensor']
            return True
        except:
            return False

#def numsensor(val): #SENSOR THAT CHECKS IF THE VALUES IS A NUMBER TYPE |||DEPRECATED||||
#    type = getValtype(val)
#    if type == 'int' or type == 'float':
#        return True
#    else:
#        return False

def setsizedims(id,context,size): # METHOD ADDING THE SIZE VALUE TO THE VARIABLE, IDENTIFYING IT AS A VECTOR
    global THEGLOBALVARset,THELOCALVARset
    if context == 'g':
        THEGLOBALVARset[id]['size'] = size
    elif context == 'l':
        THELOCALVARset[id]['size'] = size

def getdimlimits(id): # GET THE DIMENSION LIMITS OF A VECTOR
    global THEGLOBALVARset, THELOCALVARset
    try:
        return THELOCALVARset[id]['size']
    except:
        return THEGLOBALVARset[id]['size']

def fetinitialvirtualaddrvector(id): # GET THE INITIAL VIRTUAL ADDRESS OF A VECTOR
    global THEGLOBALVARset, THELOCALVARset
    try:
        return THELOCALVARset[id]['virtualaddress']
    except:
        return THEGLOBALVARset[id]['virtualaddress']




































Quadruples = altQuads()

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
#

#My Stacks 
stackofvarnames = myStack()
stackofvartypes = myStack()
stackofoperators = myStack()
combinedstackofvar = myStack()
stackofjumps = myStack()


#list  of quadruples, probably modded later, added the temporal variables

Quads2 = []
tvars = TemporalVar()

# Semantic Cube instantiated


#Auxiliary counters and lists (memory, parameters, jumps addresses, functions)
CounterParams = 0
JumpENDPROC = 0
waiting = 0
functions = []
endprocess = []
constantstab = []
TemporalsDictionary = {}
initialparameter = 0


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
    def p_PROGRAM(self,p): #PROGRAM SHELL LOGIC
        '''
        program : PROGRAM neuraladdfuncstable varsgl functions PRINCIPAL LEFTPAR RIGHTPAR LEFTBR neuralprinjump statutes RIGHTBR
        '''   
        print('Llego al final de la gramatica, aceptado')
        global GLOBALINTcounter,GLOBALFLOATcounter,GLOBALCHARcounter
        global LOCALINTcounter,LOCALFLOATcounter,LOCALCHARcounter
        global TEMPINTcounter,TEMPFLOATcounter,TEMPCHARcounter,TEMPBOOLcounter
        global CONSTINTcounter,CONSTFLOATcounter,CONSTCHARcounter,POINTERScounter
        global FUNCTIONVIRADDRcounter
        actualfuncname = p[2] #THE NEXT TOKEN
        THETABLEoffunctions[actualfuncname]['Intnumbers'] = (GLOBALINTcounter-(1000-1)) + (TEMPINTcounter - (13000-1))
        THETABLEoffunctions[actualfuncname]['Floatnumbers'] = (GLOBALFLOATcounter - (3000 - 1)) + (TEMPFLOATcounter - (15000-1))
        THETABLEoffunctions[actualfuncname]['Charnumbers'] = (GLOBALCHARcounter-(5000-1)) + (TEMPCHARcounter - (17000-1))
        THETABLEoffunctions[actualfuncname]['Boolnumbers'] = (TEMPBOOLcounter-(19000-1))
        THETABLEoffunctions[actualfuncname]['Pointernumbers'] = (POINTERScounter-(40000-1))
        #STORING THE VARIABLE NUMBERS BY SUBSTRACTING THE INITIAL MEMORY ALLOCATIONS TO THE FINAL VARIABLES COUNTERS

    def p_NEURALADDFUNCSTABLE(self,p): #NEURALGIC POINT THAT SAVES THE MAIN PROGRAM, AND STORES ITS QUADRUPLE PLACEMENT
        '''
        neuraladdfuncstable : ID SEMICOLON
        '''
        global CURRENTcontext,THEGLOBALVARset,QUADRUPLESlist,HASHOFOPERATORSINquads,STACKOFPENDINGjumps,THECONSTANTSset
        p[0] = p[1] # SKIP THE TOKEN
        insertinFunctable(p[1],'VOID',CURRENTcontext,THEGLOBALVARset)
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['GOTO'],-1,-1,-999))
        STACKOFPENDINGjumps.append(len(QUADRUPLESlist))
        THECONSTANTSset[0] = getandsetVirtualAddrCTE(0)
        THECONSTANTSset[0] = getandsetVirtualAddrCTE(1) # ADDING THE INITIAL CONSTANT VALUES OF 0 AND 1


    def p_NEURALPRINJUMP(self,p):
        '''
        neuralprinjump : 
        '''   
        global QUADRUPLESlist, STACKOFPENDINGjumps
        if STACKOFPENDINGjumps: # CHECK IF THERE ARE NECESSARY JUMPS
            endo = STACKOFPENDINGjumps.pop()
            newQuad = QUADRUPLESlist[endo-1]
            newQuad.result = len(QUADRUPLESlist) + 1 # GET THE QUADcounter FOR THE PENDIND GOTO


    #### VARIABLES LOGIC SECTION ####


    def p_VARSGL(self,p): # GETTING THE VARS TOKEN OUTTA WAY
        '''
        varsgl : VARS vars
                | empty
        '''

    def p_VARS(self,p): # GET THE TYPE OF VARIABLE, AND CHECK FOR VECTORS AND MULTIPLE TYPES DECLARATIONS
        '''
        vars : typing COLON neuralinsertvar varsarr varsmul vars
            | empty
        '''

    def p_NEURALINSERTVAR(self,p): # INSERT THE VARIABLE DATA WITH ADDRESS AND TYPE
        '''
        neuralinsertvar : ID
        '''
        global CURRENTcontext, CURRENTtype # CURRENTTYPE MODIFIED BY TYPING TOKEN BEFORE
        p[0] = p[1] #SKIPPING
        newaddr = getandsetVirtualAddrVars(CURRENTtype,CURRENTcontext)
        insertinVartable(p[1],newaddr,CURRENTtype) # ADDING THE VARIABLE

    def p_VARSMUL(self,p): #MULTIPLE VARIABLE LOGIC
        '''
        varsmul : SEMICOLON
                | COMMA neuralinsertvar varsarr varsmul
        '''

    def p_VARSARR(self,p): # LOGIC FOR GETTING VECTOR VARIABLES
        '''
        varsarr : neuralinitdim CTEINT neuralenddim
                | empty
        '''

    def p_NEURALINITDIM(self,p): # MAKE THE STORED VARIABLE VECTOR HAVE AN ARRAYSENSOR SET TO TRU
        '''
        neuralinitdim : LEFTSQR
        '''
        global THELOCALVARset, THEGLOBALVARset, CURRENTcontext
        id = p[-1] # GET THE NAME WE ARE LOOKING FOR
        if CURRENTcontext == 'g':
            THEGLOBALVARset[id]['arraysensor'] = True 
        elif CURRENTcontext == 'l':
            THELOCALVARset[id]['arraysensor'] = True
    
    def p_NEURALENDDIM(self,p):
        '''
        neuralenddim : RIGHTSQR
        '''
        global CURRENTcontext, CURRENTtype, THECONSTANTSset
        sizedim = int(p[-1]) # THE PREVIOUS TOKEN VALUE IS TAKEN AS INT
        id = p[-3] # GET THE IDENTIFIER
        if not p[-1] in THECONSTANTSset: # IF THE VALUE USED HERE ISNT ALREADY STORED AS A CONSTANT, STORE IT
            THECONSTANTSset[sizedim] = getandsetVirtualAddrCTE(sizedim)
        setsizedims(id,CURRENTcontext,sizedim) # SET THE DIMS IN THE APPROPIATE CONTEXT VARIABLE SET
        setvirtualaddrdimensions(CURRENTcontext,CURRENTtype,sizedim) # SET THE LIMITS OF MEMORY USED



    #### FUNCTIONS LOGIC SECTION ####
    # IN THE FORM OF function void/type FunctionName (int: id, float: id[val])

    def p_FUNCTIONS(self,p): # LOGIC TO GET THE FUNCTIONS SAVED
        '''
        functions : FUNCTION functype neuralinsertfuncs funcparam
                    | empty
        '''

    def p_NEURALINSERTFUNCS(self,p): #
        '''
        neuralinsertfuncs : ID
        '''
        global CURRENTcontext,CURRENTtype,THELOCALVARset,THEGLOBALVARset,CURRENTfuncname
        CURRENTfuncname = p[1] # GET THE ID WE LOOK FOR
        p[0] = p[1]
        CURRENTcontext = 'l' # CHANGE THE CONTEXT
        newaddr = getandsetVirtualAddrFunc() # GET THE NEW FUNCTION ADDRESS
        THEGLOBALVARset[CURRENTfuncname]={'virtualaddress': newaddr, 'type': CURRENTtype} # SAVE THE FUNCNAME AS RECOMMENDED
        insertinFunctable(CURRENTfuncname,CURRENTtype,CURRENTcontext,THELOCALVARset) # SAVE THE DATA TO INSERT INTO THE FUNCTION TABLES

    def p_FUNCPARAM(self,p): # LOGIC TO GET ALL THE PARAMETRS, AND NEURALGIC POINTS RELATING TO FUNCTION MAINTENANCE
        '''
        funcparam : LEFTPAR parameters RIGHTPAR neuralupdateparamtable SEMICOLON varsgl LEFTBR neuralinitfuncs statutes RIGHTBR neuralfuncsize neuralendfuncs functions
        '''
        global CURRENTcontext
        CURRENTcontext = 'l' # YEP, WE ARE INSEDE A FUNCTION ALLRIGHT

    def p_NEURALUPDATEPARAMTABLE(self,p): # ALTERNATIVE CHANGETHEPARAMETER TABLE |||| DEPRECATED ||||
        '''
        neuralupdateparamtable : 
        '''
        global PARAMETERSTABLElist, THEPARAMETERSset
        id = p[-4]

    def p_NEURALENDFUNCS(self,p): # THE NEURALGIC POINT THAT PROCESS THE ENDPROC QUADRUPLE AND RESETS THE LOCALS MEMORY COUNTERS 
        '''
        neuralendfuncs : 
        '''
        global THETABLEoffunctions, QUADRUPLESlist, HASHOFOPERATORSINquads, CURRENTfuncname,temporalsCounter
        id = CURRENTfuncname
        THETABLEoffunctions[id]['Tempsnumber'] = temporalsCounter # SAVE THE FUNCTION DATA
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['ENDPROC'],-1,-1,-1)) # SAVE THE QUADRUPLE
        ENDANDRESETFunc()

    def p_NEURALFUNCSIZE(self,p): # THE NEURALGIC POINT THE HANDLES THE VARIABLE SIZES OF THE FUNCTION INVOLVED
        '''
        neuralfuncsize :
        '''
        global THEPARAMETERSset, THETABLEoffunctions, THELOCALVARset, QUADRUPLESlist, CURRENTfuncname
        global LOCALINTcounter,LOCALFLOATcounter, LOCALCHARcounter, TEMPINTcounter, TEMPFLOATcounter, TEMPCHARcounter, TEMPBOOLcounter, POINTERScounter
        actualfuncname = CURRENTfuncname
        THETABLEoffunctions[actualfuncname]['Paramnumbers'] = len(THELOCALVARset)
        THETABLEoffunctions[actualfuncname]['Intnumbers'] = (LOCALINTcounter-(7000-1)) + (TEMPINTcounter - (13000-1))
        THETABLEoffunctions[actualfuncname]['Floatnumbers'] = (LOCALFLOATcounter - (9000 - 1)) + (TEMPFLOATcounter - (15000-1))
        THETABLEoffunctions[actualfuncname]['Charnumbers'] = (LOCALCHARcounter-(11000-1)) + (TEMPCHARcounter - (17000-1))
        THETABLEoffunctions[actualfuncname]['Boolnumbers'] = (TEMPBOOLcounter-(19000-1))
        THETABLEoffunctions[actualfuncname]['Pointernumbers'] = (POINTERScounter-(40000-1))
        # ALL THE SAVING OF ACTUAL VARIABLE NUMBERS, SAME AS THE PROGRAM VERSION

    def p_NEURALINITFUNCS(self,p): #NEURALGIC POINT THAT GENERATES THE QUADRUPLE AND SAVES THE FUNCTION ADDRES IN THE TABLE OF FUNCTIONS
        '''
        neuralinitfuncs :
        '''
        global CURRENTfuncname,QUADRUPLESlist
        actualfuncname = CURRENTfuncname
        THETABLEoffunctions[actualfuncname]['Initialfuncpoint'] = len(QUADRUPLESlist) + 1

    def p_FUNCTYPE(self,p): # DEALING WITH THE TYPE OF THE FUNCTION RETURN
        '''
        functype : VOID
                | typing
        '''
        global CURRENTtype, CURRENTcontext
        CURRENTtype = t[1] # THE NEXT TOKEN
        CURRENTcontext = 'l'



    ####### STATUTES LOGIC SECTION ####

    def p_STATUTES(self,p): # THE MEAT LOGIC OF A PROGRAM WHERE WE HAVE ALL THE POSSIBLE STATUTES
        '''
        statutes : assign statuteaux
                | reading statuteeaux
                | writing statuteeaux
                | returning statuteeaux
                | ifing statuteeaux
                | whiling statuteeaux
                | foring statuteeaux
                | exp statuteeaux
                | media statuteeaux
                | plotxy statuteeaux
                | mediana statuteeaux
                | moda statuteeaux
                | variance statuteeaux
                | stdev statuteeaux
        '''

    def p_STATUTEAUX(self,p): # THE MULTIPLE STATUTES HANDLER
        '''
        statuteaux : statutes
                    | empty
        '''

    ##### SPECIAL FUNCTIONS OF MYRLIKELANGUAGE #######
    def p_MEDIA(self,p):
        '''
        media : MEDIA LEFTPAR specfuncnumbers RIGHTPAR specialfunclist SEMICOLON
        '''
        global QUADRUPLESlist, HASHOFOPERATORSINquads, SPECIALMETHODScounter,SPECIALMETHODSlist,SPECIALMETHODSaux
        SPECIALMETHODScounter +=1
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['MEDIA'],-1,-1,SPECIALMETHODScounter)) #ADD THE SPECIAL QUADRUPLE
        SPECIALMETHODSaux = [] # RESET THE AUXILIAR LIST

    def p_MEDIANA(self,p):
        '''
        mediana : MEDIANA LEFTPAR specfuncnumbers RIGHTPAR specialfunclist SEMICOLON
        '''
        global QUADRUPLESlist, HASHOFOPERATORSINquads, SPECIALMETHODScounter,SPECIALMETHODSlist,SPECIALMETHODSaux
        SPECIALMETHODScounter +=1
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['MEDIANA'],-1,-1,SPECIALMETHODScounter)) #ADD THE SPECIAL QUADRUPLE
        SPECIALMETHODSaux = [] # RESET THE AUXILIAR LIST

    def p_MODA(self,p):
        '''
        moda : MODA LEFTPAR specfuncnumbers RIGHTPAR specialfunclist SEMICOLON
        '''
        global QUADRUPLESlist, HASHOFOPERATORSINquads, SPECIALMETHODScounter,SPECIALMETHODSlist,SPECIALMETHODSaux
        SPECIALMETHODScounter +=1
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['MODA'],-1,-1,SPECIALMETHODScounter)) #ADD THE SPECIAL QUADRUPLE
        SPECIALMETHODSaux = [] # RESET THE AUXILIAR LIST

    def p_STDEV(self,p):
        '''
        stdev : STDEV LEFTPAR specfuncnumbers RIGHTPAR specialfunclist SEMICOLON
        '''
        global QUADRUPLESlist, HASHOFOPERATORSINquads, SPECIALMETHODScounter,SPECIALMETHODSlist,SPECIALMETHODSaux
        SPECIALMETHODScounter +=1
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['STDEV'],-1,-1,SPECIALMETHODScounter)) #ADD THE SPECIAL QUADRUPLE
        SPECIALMETHODSaux = [] # RESET THE AUXILIAR LIST

    def p_VARIANCE(self,p):
        '''
        variance : VARIANZA LEFTPAR specfuncnumbers RIGHTPAR specialfunclist SEMICOLON
        '''
        global QUADRUPLESlist, HASHOFOPERATORSINquads, SPECIALMETHODScounter,SPECIALMETHODSlist,SPECIALMETHODSaux
        SPECIALMETHODScounter +=1
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['VARIANZA'],-1,-1,SPECIALMETHODScounter)) #ADD THE SPECIAL QUADRUPLE
        SPECIALMETHODSaux = [] # RESET THE AUXILIAR LIST
    
    def p_PLOTXY(self,p):
        '''
        plotxy : PLOTXY LEFTPAR specfuncnumbers RIGHTPAR specialfunclist SEMICOLON
        '''
        global QUADRUPLESlist, HASHOFOPERATORSINquads, SPECIALMETHODScounter,SPECIALMETHODSlist,SPECIALMETHODSaux
        SPECIALMETHODScounter +=1
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['PLTOXY'],-1,-1,SPECIALMETHODScounter)) #ADD THE SPECIAL QUADRUPLE
        SPECIALMETHODSaux = [] # RESET THE AUXILIAR LIST



















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
        checkid :
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
        boolexp : arithexp 
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
            stackofvartypes.push('int')
            if not searchConst(cte):
                virtualaddr = Virtualmem.assignVirtualMemory('ConstantVars','int')
                constantstab.append({
                    'ConstantVar' : cte,
                    'VirtualAddr' : virtualaddr
                })
            else:
                virtualaddr = getConstantAddress(cte)
            stackofvarnames.push(virtualaddr)
        elif t == float:
            stackofvartypes.push('float')
            if not searchConst(cte):
                virtualaddr = Virtualmem.assignVirtualMemory('ConstantVars','float')
                constantstab.append({
                    'ConstantVar' : cte,
                    'VirtualAddr' : virtualaddr
                })
            else:
                virtualaddr = getConstantAddress(cte)
            stackofvarnames.push(virtualaddr)
        else:
            stackofvartypes.push('char')
            if not searchConst(cte):
                virtualaddr = Virtualmem.assignVirtualMemory('ConstantVars','char')
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

    def p_STOREFUNCT(self,p):
        '''
        storefunct :
        '''
        global ongoingfunctype, ongoingfuncid, DirectoryofFunctions
        ongoingfunctype = p[-2]
        ongoingfuncid = p[-1]
        DirectoryofFunctions.addfunc(ongoingfunctype,ongoingfuncid,0,[],[],0,-1,0)

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