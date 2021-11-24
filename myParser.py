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

##### PYTHON LISTS, MUTABLE, ORDER OF ELEMENTS INHERENT IN THEIR APPLICATION, CAN FUNCTION AS STACKS #############

GLOBALNAMESlist = []
LOCALNAMESlist = []
QUADRUPLESlist = []
CONSTANTSlist= []
CONSTANTPARAMETERSlist = []
PARAMETERSTABLElist = []

PARAMETERQUEUElist = []
SPECIALMETHODSlist = []
SPECIALMETHODSaux = []


###MY STACKS, I discovered way to late that the pop() in python lists simulate stacks dammit all ########

STACKOFoperands = [] #Pila Operandos, PilaO en clase
STACKOFoperatorssymb = [] # Pila de operators, POper en clase
STACKOFtypes = []
STACKOFPENDINGjumps = []
STACKOFdims = []

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
        CURRENTtype = p[1] # THE NEXT TOKEN
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
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['PLOTXY'],-1,-1,SPECIALMETHODScounter)) #ADD THE SPECIAL QUADRUPLE
        SPECIALMETHODSaux = [] # RESET THE AUXILIAR LIST

    def p_SPECIALFUNCLIST(self,p):
        '''
        specialfunclist : 
        '''
        global SPECIALMETHODSlist, SPECIALMETHODSaux
        SPECIALMETHODSlist.append(SPECIALMETHODSaux) # ADD THE AUXILIAR LIST FOR SPECIAL METHODS
    
    def p_SPECFUNCNUMBERS(self,p): # METHOD TO HANDLE THE CONSTANT NUMBERS
        '''
        specfuncnumbers : CTEINT neuralnum mulnumeros
                        | CTEFLOAT neuralnum mulnumeros
        '''
        
    def p_NEURALNUM(self,p): #NEURALGIC POINT TO DEAL WITH THE PARAMETERS OF A SPECIAL METHOD
        '''
        neuralnum :
        '''
        global SPECIALMETHODSaux
        SPECIALMETHODSaux.append(p[-1]) # ADD THE PREVIOUS CONSTANT

    def p_MULNUMEROS(self,p): # MULTIPLE CONSTANTS IN THE SPECIAL METHOD
        '''
        mulnumeros : COMMA specfuncnumbers
                    | empty
        '''

    ##### TYPING OF VARIABLES SECTION #######

    def p_TYPING(self,p):
        '''
        typing : INT
                | FLOAT
                | CHAR
        '''
        global CURRENTtype
        CURRENTtype = p[1] # THE NEXT TOKEN GETS TAKEN AS THE CURRENT TYPE
        p[0] = p[1] #SKIPPING

    ####PARAMATERS AND RELATED SECTION #######

    def p_PARAMETERS(self,p): # THE LOGIC TO GET ALL THE PARAMETRS IN A FUNCTION CALL
        '''
        parameters : typing COLON neuralinsertparam idarray mulparams
                    | empty
        '''
        

    def p_NEURALINSERTPARAM(self,p): # GET AND SAVE ALL THE PARAMETER DATA
        '''
        neuralinsertparam : ID
        '''
        global CURRENTcontext,CURRENTtype, PARAMETERSTABLElist, PARAMETERQUEUElist
        CURRENTcontext = 'l'
        virtualaddr = getandsetVirtualAddrVars(CURRENTtype,CURRENTcontext) # GET TEH ADDRESS
        PARAMETERQUEUElist.append(virtualaddr) # ADD TO THE LIST THE ADDRESS
        insertinVartable(p[1],virtualaddr, CURRENTtype) # GET THE VALUE WE ARE LOOKING FOR AND ADD IT TO THE VARTABLE
        PARAMETERSTABLElist.append(CURRENTtype)

    def p_MULPARAMS(self,p): # HANDLE TEH MULTIPLE PARAMETERS
        '''
        mulparamas : COMMA parameters
                    | empty
        '''


    ###### ASSIGN LOGIC SECTION ######
    # ID = 123 ; OR ID =12.3 OR ID = VAR OR ID = VAR[1] OR ID = FUNCTION(1,1) OR ID = 'C' 

    def p_ASSIGN(self,p): # THE LOGIC THAT GETS THE ASSIGNATION OF VALUES
        '''
        assign : neuralassign idarray neuralassign2 assignexp SEMICOLON
        '''
        global STACKOFoperands, STACKOFtypes,HASHOFOPERATORSINquads
        if STACKOFoperands and STACKOFtypes : #NOT EMPTY
            result = STACKOFoperands #GET THE RESULT VALUE TO BE ASSIGNED
            righttype = STACKOFtypes 
            leftop = STACKOFoperands # GET THE VARIABLE THAT WILL RECEIVE
            lefttype = STACKOFtypes
            typechecker(lefttype,righttype)
            QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['='],result,-1,leftop))

    def p_NEURALASSIGN(self,p):
        '''
        neuralassign : ID
        '''
        global STACKOFoperands, STACKOFtypes
        p[0]=p[1] # SKIPPING
        virtualaddr = virtualaddrfetcher(p[1]) # GET THE TOKEN WE ARE LOOKING FOR
        STACKOFoperands.append(virtualaddr)
        STACKOFtypes.append(getValtype(p[1])) # GET THE TYPE OF THE VALUE WE ARE LOOKING

    def p_NEURALASSIGN2(self,p):
        '''
        neuralassign2 : EQUAL
        '''
        global STACKOFoperatorssymb, QUADRUPLESlist
        STACKOFoperatorssymb.append(p[1]) # GET THAT EQUAL TOKEN IN THAT STACK


    def p_ASSIGNEXP(self,p):
        '''
        assignexp : exp
        '''
        p[0] = p[1] # SKIPPING TOKEN


    def p_IDARRAY(self,p):
        '''
        idarray : neuralinitarray exp verify RIGHTSQR
                | empty
        '''
        global STACKOFoperands,QUADRUPLESlist,HASHOFOPERATORSINquads,THEGLOBALVARset,STACKOFtypes,STACKOFoperatorssymb, THECONSTANTSset
        if len(p) > 2 and STACKOFoperands and STACKOFoperatorssymb: # IF THE STACKS ARE NOT EMPTY AND WE HAVE A WORKING ARRAY
            aux = STACKOFoperands.pop()
            initaddr = fetinitialvirtualaddrvector(p[-1])
            if not initaddr in THECONSTANTSset: # IF NEW CONSTANT,SAVE IT
                THECONSTANTSset[initaddr] = getandsetVirtualAddrCTE(initaddr)
            actualaddr = THECONSTANTSset[initaddr] # IF ALREADY USED, GIVE US THE VIRTUALADDRESS
            pointer = getandsetVirtualAddrTemp('pointer')
            QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['+'],aux,actualaddr,pointer)) # AS SEEN IN CLASS TO DEAL WITH ARRAYS
            STACKOFoperands.append(pointer)
            STACKOFoperatorssymb.pop() #DEAL WITH THE OPERATOR

    def p_NEURALINITARRAT(self,p):
        '''
        neuralinitarray : LEFTSSQR
        '''
        global STACKOFoperatorssymb,STACKOFoperands,STACKOFdims,STACKOFtypes
        if STACKOFoperands:
            id = STACKOFoperands.pop()
            typeclearer = STACKOFtypes.pop()
            name = p[-1] # GET THE TOKEN IDENTIFIER FOR THIS VECTOR
            dimensionssensor(name)
            DIM = 1 # IN THIS LANGUAAAGE, ONLY VECTORS PASS MY LIEGE
            STACKOFdims.append((id,DIM))
            STACKOFoperatorssymb.append("~~~") # OUR FAKE BOTTOM, AS SEEN IN CLASS
    
    def p_VERIFY(self,p):
        '''
        verify : 
        '''
        global STACKOFoperands, QUADRUPLESlist, HASHOFOPERATORSINquads, THECONSTANTSset
        value = STACKOFoperands[-1] # OUR LAST ELEMENT, TOP() INHERENT IN PYTHON 
        id = p[-3] # GET THAT IDENTIFIER
        limit = getdimlimits(id)
        upperlimit = virtualaddrfetcher(limit) # GET OUR LIMITS GO GO GO
        lowerlimit = virtualaddrfetcher(0)
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['VER'],value,lowerlimit,upperlimit)) # OUR NICE VER QUADRUPLE


    #### RETURN SPECIAL QUAD ####
    def p_RETURNING(self,p): # A STATIC GRAMMAR, ONLY THE EXP IS SPECIAL
        '''
        returning : RETURN LEFTPAR exp RIGHTPAR SEMICOLON
        '''
        global STACKOFoperands,QUADRUPLESlist,HASHOFOPERATORSINquads,THEGLOBALVARset
        valtoreturn = STACKOFoperands.pop()
        STACKOFtypes.pop()
        funcviraddr = THEGLOBALVARset[CURRENTfuncname]['virtualaddress'] # GET ME THE ADDRESS FOR THE FUNCTION WE HAVE HERE
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['RETURN'],valtoreturn,-1,funcviraddr))

    ### READING LOGIC SECTION #####
    def p_READING(self,p): # OUR OUTER SHELL OF THE READ LOGIC
        '''
        reading : READ LEFTPAR neuralreadid idarray mulread RIGHTPAR SEMICOLON
        '''

    def p_NUERALREADID(self,p):
        '''
        neuralreadid : ID
        '''
        global QUADRUPLESlist,HASHOFOPERATORSINquads
        assignedvar = virtualaddrfetcher(p[1]) # THE VAR TO BE READ AND ASSIGNED VALUE, GET THEIR ADDRESS
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['READ'],-1,-1,assignedvar)) #ADD THE QUADRUPLE

    def p_MULREAD(self,p): # MANAGE THE MULTIPLE READING TO ASSIGN VALUE TO VARIABLES
        '''
        mulread : COMMA neuralreadid idarray mulread
                | empty
        '''


    ### WRITE LOGIC SECTION ###
    def p_WRITING(self,p): # WRITE ALL DATA, ARRAY EXPECTED TO BE ALREADY IN A SPECIFIC VAR WHEN ACCESSED BY EXP
        '''
        writing : WRITE LEFTPAR neuralwrite mulwrite RIGHTPAR SEMICOLON
        '''

    def p_NEURALWRITE(self,p):
        '''
        neuralwrite : writetype
                    | exp
        '''
        global STACKOFoperands,QUADRUPLESlist,HASHOFOPERATORSINquads
        result = STACKOFoperands.pop() # GET THE OPERAND THAT IS GOIN TO WRITE
        QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['WRITE'],-1,-1,result)) # ADD THE WRITE QUADRUPLE

    def p_WRITETYPE(self,p):
        '''
        writetype : STRING
                | CTECHAR
        '''
        global STACKOFoperands
        STACKOFoperands.append(p[1]) # STORE THAT OPERAND THAT IS WAITING AS A STRING OR CTECHAR

    def p_MULWRITE(self,p): #MANAGE MULTIPLE VARIABLES TO WRITE
        '''
        mulwrite : COMMA neuralwrite mulwrite
                | empty
        '''


    #### IF AND DECISION LOGIC SECTION ######
    def p_IFING(self,p):
        '''
        ifing : IF LEFTPAR exp neuralif THEN LEFTBR statutes RIGHTBR elsing
        '''
        global STACKOFPENDINGjumps, QUADRUPLESlist
        if STACKOFPENDINGjumps: #IF THER IS SOMETHING THERE
            endo = STACKOFPENDINGjumps.pop() # GET THAT VIRTUAL ADDRESS
            newQuad = QUADRUPLESlist[endo-1] # GET THE QUAD TO CHANGE PENDING ADDRESS
            newQuad.result = len(QUADRUPLESlist)+1 # THE RESULT STORES THE APPROPIATE ADDRESS

    def p_ELSING(self,p): # CHECK IF THERE IS AN ELSE AND PROCESS THE STATUES IF SO
        '''
        elsing : neuralelse LEFTBR statutes RIGHTBR
                | empty
        '''

    def p_NEURALELSE(self,p): # GETTING THE QUADRUPLE ADDED, TO GET THE GOTO FOR THE ELSE
        '''
        neuralelse : 
        '''
        global QUADRUPLESlist, STACKOFPENDINGjumps, HASHOFOPERATORSINquads
        if STACKOFPENDINGjumps:
            QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['GOTO'],-1,-1,-999))
            elseendo = STACKOFPENDINGjumps.pop() # GET THE ADDRESS FOR THE JUMP
            STACKOFPENDINGjumps.append(len(QUADRUPLESlist)) # ADD THE NUMVALUE TO BE JUMPED
            newQuad = QUADRUPLESlist[elseendo-1] # GET THE ADDRESS QUADRUPLE TO BE MODIFIED
            newQuad.result = len(QUADRUPLESlist) + 1 # STORES THE APPROPIATE ADDRESS
        
    def p_NEURALIF(self,p): # THE NEURAL POINT THAT ADDS THE QUADRUPLE OF THE IF
        '''
        neuralif : RIGHTPAR
        '''
        global STACKOFtypes, STACKOFoperands,QUADRUPLESlist,STACKOFPENDINGjumps,HASHOFOPERATORSINquads
        if STACKOFtypes and STACKOFoperands: # DO WE HAVE VALUES TO WORK WITH?
            vartype = STACKOFtypes.pop()
            typechecker(vartype,'bool') # ONLY BOOLS ARE ALLOWED HERE IN THE DECISION 
            result = STACKOFoperands.pop()
            QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['GOTOF'],result,-1,-99)) # THE QUADRUPLE, ADDRESS PENDING
            STACKOFPENDINGjumps.append(len(QUADRUPLESlist)) #  GET THE QUAD COUNTER OF THE JUMP APPENDED


    #### WHILE LOGIC SECTION ####

    def p_WHILING(self,p):
        '''
        whiling : neuralwhile LEFTPAR exp neuralwhile2 DO LEFTBR statutes RIGHTBR
        '''
        global STACKOFPENDINGjumps,QUADRUPLESlist,HASHOFOPERATORSINquads
        if STACKOFPENDINGjumps:
            endo = STACKOFPENDINGjumps.pop()
            starto = STACKOFPENDINGjumps.pop()
            QUADRUPLESlist.append(Quadruple(HASHOFOPERATORSINquads['GOTO'],-1,-1,starto+1)) # SET THE GOTO QUAD WITH THE APPROPIATE ADDRESS
            newQuad =  QUADRUPLESlist[endo - 1]
            newQuad.result = len(QUADRUPLESlist) + 1 # STORE THE APPROPIATE ADDRESS
        
    def p_NEURALWHILE(Self,p): # NEURAL POINT TO GET THE STACK OF JUMPS WITH THE QUAD COUNTER
        '''
        neuralwhile : WHILE
        '''
        global STACKOFPENDINGjumps, QUADRUPLESlist
        STACKOFPENDINGjumps.append(len(QUADRUPLESlist)) # GET THAT QUAD COUNTER

    def p_NEURALWHILE2(self,p): # NEURAL POINT CHECIN IF THE TYPE ACTUALLY WORKS, AND GET THE INITIAL GOTOF
        '''
        neuralwhile : RIGHTPAR
        '''
        global STACKOFtypes,STACKOFoperands,QUADRUPLESlist, STACKOFPENDINGjumps,HASHOFOPERATORSINquads
        if STACKOFtypes and STACKOFoperands: # DO WE HAVE VALS to WORK WITH?
            exptype = STACKOFtypes.pop()
            typechecker(exptype,'bool')



    #EXCEPTIONS HANDLING#####

    def p_error(self,p):
        print ("Syntax Error with: ", p)

    def p_empty(self,p):
        '''
        empty : 
        '''     
        p[0] = None   