import sys
from MyLexerParser import QUADRUPLESlist, THETABLEoffunctions
from MyLexerParser import THECONSTANTSset,SPECIALMETHODSlist
import statistics, matplotlib.pyplot as plt # SHORTCUTS FOR THE WIN

#### MY QUADS SHORTCUT OPERATORS GUIDE
###HASHOFOPERATORSINquads = {
###    '+' : 1,
###    '-' : 2,
###    '*' : 3,
###    '/' : 4,
###    '>' : 5,
###    '<' : 7,
###    '<=' : 8,
###    '==' : 9,
###    '<>' : 10,
###    '=' : 11,
###    'READ' : 12,
###    'WRITE' : 13,
###    'and' : 14,
###    'OR' : 15,
###    'GOTO' : 16,
###    'GOTOF' : 17,
###    'GOTOV' : 18,
###    'ERA' : 19,
###    'VER' : 20,
###    'ENDPROC' : 21,
###    'PARAM' : 22,
###    'GOSUB' : 23,
###   'MEDIA' : 24,
###   'MEDIANA' : 25,
###    'MODA' : 26,
###    'STDEV' : 27,
###    'VARIANZA' : 28,
###    'PLOTXY' : 29,
###   'RETURN' : 30,
###    '' : -1
###}

### READING MY QUADRUPLES
file = open("Quads.mir","r")
Quads = file.read()
Quads =  Quads.split("\n") # GIVE ME THE SEPARATED LINES
Quads = Quads[:-1] # GET RID OF THE LAST CHAR

##### STACK OF MEMORY HANDLERS, GLOBAL VARIABLES, MEMORY CLASS AND MISC #####
STACKofexecs = []
PROCList = []
PROCCOUNTER = 0
globalsensor = True

class Memory:
    def __init__(self):
        self.memor = {} ### A SET FOR OUR MEMORY####

#UNIVERSAL METHODS FOR THE VM ###############
# ERROR HANDLER
def ERROR(type,location = ""):
    print("ERROR: ", type , " at ===>", location)
    sys.exit()

# GET THE CONSTANT VALUE
def gettheCTE(value):
    global THECONSTANTSset
    for key, value2 in THECONSTANTSset.items():
        if value == value2: ### IF FOUND IN THE CONSTANT TABLE
            return key

def nonesensor(value,quadruple): ## CHECKING IF A QUADRUPLE OPERATION HAS A NONE VALUE
    global globalsensor
    if value is None:
        ERROR("NONE IN HERE", quadruple)

def isReadable(Varia, value):# CHECK IF IT CAN BE READ AS VARIABLE
    global globalsensor
    if globalsensor:
        if Varia < 3000 and Varia >= 1000:
            try:
                value = int(value)
            except:
                ERROR("TYPE MISMATCH", value)
        elif Varia < 5000 and Varia >= 3000:
            try:
                value = float(value)
            except: 
                ERROR("TYPE MISMATCH", value)
        elif Varia < 7000 and Varia >= 5000:
            if len(value) > 1:
                ERROR("NOT A CHAR", value)
            value = str(value)
        else:
            ERROR("TYPE MISMATCH", value)

def loadvirtualmemory(processname): # LOAD THE MEMORY WE ARE WORKING WITH
    for element in THETABLEoffunctions[processname]['variables']:
        virtualaddr = THETABLEoffunctions[processname]['variables'][element]['virtualaddress'] # GET THE VIRTUAL ADDRESS
        actualmemory.memor[virtualaddr] = None # LIBERATE

def vectorsensor(value): # FAST ARRAY SENSOR FOR THE ADDRESS
    return value >= 30000


def fromVector(indexz): # HANDLE THE VECTORS WITH THE DOUBLE INDEXING
    global globalsensor
    if globalsensor:
        try: 
            return int(GLOBALmemory.memor[indexz])
        except:
            print("The index ==> ",indexz)
            print(GLOBALmemory.memor)
            return indexz
    else:
        try:
            return actualmemory.memor[indexz]
        except:
            print("The index ==> ", indexz)
            print(actualmemory.memor)
            return indexz

def localsensor(value): # AS DEFINED
    try:
        actualmemory.memor[value]
        return True
    except:
        return False

def globalsensor2(value): # AS DEFINED
    try:
        GLOBALmemory.memor[value]
        return True
    except:
        ERROR("NO EXISTENCE FOR THIS VALUE ", str(value))

def changecontextlocalsensor(value): # HANDLE IF IT WAS THE LAST LOCAL VARIABLE BEFORE A CONTEXT CHANGE
    global STACKofexecs
    try:
        STACKofexecs[-1].memor[value]
        return True
    except:
        return False

for x in THETABLEoffunctions.keys(): # GET THE THE NAME OF THE FUNCTION PROGRAM
    if THETABLEoffunctions[x]['context'] == 'g':
        actualprogramname = x

######## MEMORY INITIALIZERS ########
GLOBALmemory = Memory()
actualmemory = None

for element in THETABLEoffunctions[actualprogramname]['variables']: # LOAD THE GLOBAL MEMORY
    virtualaddr = THETABLEoffunctions[actualprogramname]['variables'][element]['virtualaddress']
    GLOBALmemory.memor[virtualaddr] = None

for element2 in THECONSTANTSset: # LOAD THE CONSTANT TO THE MEMORY
    virtualaddr = THECONSTANTSset[element2]
    if virtualaddr < 23000:
        GLOBALmemory.memor[virtualaddr]=int(element2)
    elif virtualaddr < 25000:
        GLOBALmemory.memor[virtualaddr]=float(element2)
    elif virtualaddr < 27000:
        GLOBALmemory.memor[virtualaddr]=str(element2)

###DEBUGGIN GOES HERE ##########
#print("\n", THETABLEoffunctions) LOOK WHAT WE ARE WORKING WITH HERE
#print("\n", THECONSTANTSset)

#### THE GREAT CYCLE OF PROCESSING THE QUADRUPLES READED######
while PROCCOUNTER <= len(Quads):
    # DEFRAG THE READ FILE INTO ELEMENTS
    (indexz,operat,leftoperd,rightoperd,result) = Quads[PROCCOUNTER].split("~")
    #DEBUG
    #print(PROCCOUNTER+1, "<=== QUADRUPLE WE ARE GOING TO WORK WITH")

    # GOTO
    if int(operat) == 16:
        PROCCOUNTER = int(result) - 2 # LOAD THE JUMP, ADJUSTING WITH THE OFFSET
    # EQUAL = 
    elif int(operat) == 11:
        if vectorsensor(int(result)): # LOAD THE ACTUAL ARRAY VALUE
            result = fromVector(int(result))
        if globalsensor:
            nonesensor(GLOBALmemory.memor[int(leftoperd)],int(leftoperd)) # DONT GET NONES
            GLOBALmemory.memor[int(result)] = GLOBALmemory.memor[int(leftoperd)] # ASSIGN THE VAL
        else:
            try:
                nonesensor(actualmemory.memor[int(leftoperd)],int(leftoperd)) # DONT GET NONES
                actualmemory.memor[int(result)] = actualmemory.memor[int(leftoperd)] # ASSIGN THE VAL
            except:
                nonesensor(GLOBALmemory.memor[int(leftoperd)],int(leftoperd)) # DONT GET NONES
                actualmemory.memor[int(result)] = GLOBALmemory.memor[int(leftoperd)] # ASSIGN THE VAL, ACCOUNTING FOR CHANGE CONTEXT
    # SUM +
    elif int(operat) == 1:
        if vectorsensor(int(leftoperd)):
            leftoperd = fromVector(int(leftoperd))
        if vectorsensor(int(rightoperd)):
            rightoperd = fromVector(int(rightoperd))
        if globalsensor:
            nonesensor(GLOBALmemory.memor[int(leftoperd)],1)
            nonesensor(GLOBALmemory.memor[int(rightoperd)],1)
            GLOBALmemory.memor[int(result)] = GLOBALmemory.memor[int(leftoperd)] + GLOBALmemory.memor[int(rightoperd)]
        else:
            if localsensor(int(leftoperd)) and localsensor(int(rightoperd)):
                actualmemory.memor[int(result)] = actualmemory.memor[int(leftoperd)] + actualmemory.memor[int(rightoperd)]
            elif localsensor(int(leftoperd)) and globalsensor2(int(rightoperd)):
                actualmemory.memor[int(result)] = actualmemory.memor[int(leftoperd)] + GLOBALmemory.memor[int(rightoperd)]
            elif globalsensor2(int(leftoperd)) and localsensor(int(rightoperd)):
                actualmemory.memor[int(result)] = GLOBALmemory.memor[int(leftoperd)] + actualmemory.memor[int(rightoperd)]
            elif globalsensor2(int(leftoperd)) and globalsensor2(int(rightoperd)):
                actualmemory.memor[int(result)] = GLOBALmemory.memor[int(leftoperd)] + GLOBALmemory.memor[int(rightoperd)] # ACCOUNT FOR CONTEXT CHANGES
            else:
                ERROR("TRYING NONES IN THE SUM QUADS")
    elif int(operat) == 3:
        if vectorsensor(int(leftoperd)):
            leftoperd = fromVector(int(leftoperd))
        if vectorsensor(int(rightoperd)):
            rightoperd = fromVector(int(rightoperd))
        if globalsensor:
            nonesensor(GLOBALmemory.memor[int(leftoperd)],3)
            nonesensor(GLOBALmemory.memor[int(rightoperd)],3)
            GLOBALmemory.memor[int(result)] = GLOBALmemory.memor[int(leftoperd)] * GLOBALmemory.memor[int(rightoperd)]
        else:
            if localsensor(int(leftoperd)) and localsensor(int(rightoperd)):
                actualmemory.memor[int(result)] = actualmemory.memor[int(leftoperd)] * actualmemory.memor[int(rightoperd)]
            elif localsensor(int(leftoperd)) and globalsensor2(int(rightoperd)):
                actualmemory.memor[int(result)] = actualmemory.memor[int(leftoperd)] * GLOBALmemory.memor[int(rightoperd)]
            elif globalsensor2(int(leftoperd)) and localsensor(int(rightoperd)):
                actualmemory.memor[int(result)] = GLOBALmemory.memor[int(leftoperd)] * actualmemory.memor[int(rightoperd)]
            elif globalsensor2(int(leftoperd)) and globalsensor2(int(rightoperd)):
                actualmemory.memor[int(result)] = GLOBALmemory.memor[int(leftoperd)] * GLOBALmemory.memor[int(rightoperd)] # ACCOUNT FOR CONTEXT CHANGES
            else:
                ERROR("TRYING NONES IN THE TIMES QUADS")
    elif int(operat) == 2:
        if vectorsensor(int(leftoperd)):
            leftoperd = fromVector(int(leftoperd))
        if vectorsensor(int(rightoperd)):
            rightoperd = fromVector(int(rightoperd))
        if globalsensor:
            nonesensor(GLOBALmemory.memor[int(leftoperd)],2)
            nonesensor(GLOBALmemory.memor[int(rightoperd)],2)
            GLOBALmemory.memor[int(result)] = GLOBALmemory.memor[int(leftoperd)] - GLOBALmemory.memor[int(rightoperd)]
        else:
            if len(STACKofexecs) > 0:
                if changecontextlocalsensor(int(leftoperd)) and changecontextlocalsensor(int(rightoperd)):
                    STACKofexecs[-1].memor[int(result)] = STACKofexecs[-1].memor[int(leftoperd)] - STACKofexecs[-1].memor[int(rightoperd)]
                elif changecontextlocalsensor(int(leftoperd)) and globalsensor2(int(rightoperd)):
                    actualmemory.memor[int(result)] = actualmemory.memor[int(leftoperd)] - GLOBALmemory.memor[int(rightoperd)]
                elif globalsensor2(int(leftoperd)) and localsensor(int(rightoperd)):
                    actualmemory.memor[int(result)] = GLOBALmemory.memor[int(leftoperd)] - actualmemory.memor[int(rightoperd)]
                elif globalsensor2(int(leftoperd)) and globalsensor2(int(rightoperd)):
                    actualmemory.memor[int(result)] = GLOBALmemory.memor[int(leftoperd)] - GLOBALmemory.memor[int(rightoperd)] # ACCOUNT FOR CONTEXT CHANGES
                else:
                    ERROR("TRYING NONES IN THE REST QUADS")