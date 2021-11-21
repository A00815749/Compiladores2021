from Vartables import Vartables

#The Directory for functions and all that fun 
class DirectoryFunctions:
    def _init_(self):
        self.directory = {}

    def addfunc(self, type, functionID,numPar,typePar,nameofPar,numVars,addstart,magnitude):
        if(functionID not in self.directory.keys()): #Is the function already in the list to not cause conflicts
            self.directory[functionID] = {
                'type' : type,
                'numPar' : numPar,
                'typePar' : typePar,
                'nameofPar' : nameofPar,
                'localvars' : Vartables(),
                #probably using a method later for the numvars
                'numberVars' : numVars, 
                'addstart' : addstart,
                'magnitude' :magnitude
            }
            print("Check, function ", functionID, ' ', type)

        else:
            print ("Error, function already in the directory of functions ", functionID)

    #Initialize values
    def setMagnitude(self,functionid,magnitude):
        self.directory[functionid]['magnitude'] = magnitude

    def setAddstart(self,functionid,addstart):
        self.directory[functionid]['addstart'] = addstart


    #Search things
    def searchFunc(self,funcid): #Search method
        return funcid in self.directory

    def searchVar(self,Varid,functionid):
        if self.directory[functionid]['localvars'].searchvar(Varid) or self.directory['program']['localvars'].searchvar(Varid):
            return True
        else:
            print ("Var ", Varid, " not found")

    #Getters
    def getVarType(self, Varid,functionid):
        if self.directory[functionid]['localvars'].searchvar(Varid):
            return self.directory[functionid]['localvars'].getType(Varid)
        elif self.directory['program']['localvars'].searchvar(Varid):
            return self.directory['program']['localvars'].getType(Varid)
        else:
            print("Variable: ", Varid, " cant be accessed to get typing")

    def getnumPar(self,functionid):
        return self.directory[functionid]['numPar']

    def getTypePar(self,functionid):
        return self.directory[functionid]['typePar']

    def getaddstart(self,functionid):
        return self.directory[functionid]['addstart']

    def getnameofPar(self,functionid):
        return self.directory[functionid]['nameofPar']

    def getaddID(self,functionid,Varid):
        if self.searchVar('program',Varid):
            return self.directory['program']['localvars'].getViraddress(Varid) #The globalprogram exception
        elif(self.searchVar(functionid,Varid)):
            return self.directory[functionid]['localvars'].getViraddress(Varid)
        else:
            print("Error at getting variable, probably not declared")

    #Misc methods
    def addVar(self,functionID, type, currentID, virtualaddress):
        if self.directory[functionID]['localvars'].searchvar(currentID) or self.directory['program']['localvars'].searchvar(currentID):
            print("This variable is already in the function ", currentID)
        else:
            self.directory[functionID]['localvars'].add(currentID, type,virtualaddress)
            print("Var added to function local table ", functionID)
            

    def addPar(self,functionid, functionType, functionName):
        self.directory[functionid]['numPar'] += 1
        self.directory[functionid]['typePar'].append(functionType)
        self.directory[functionid]['nameofPar'].append(functionName)

    def printfuncvariables(self,functionID):
        if functionID in self.directory:
            self.directory[functionID]['localvars'].printvar()

    def printfunc(self,functionID):
        print("ID " + functionID)
        print("Type " + self.directory[functionID]['type'])
        print("Number of Parameters " + self.directory[functionID]['numPar'])
        print("type of Parameters : ")
        print(self.directory[functionID]['typePar'])
        print("Name of Parameters : ")
        print(self.directory[functionID]['nameofPar'])
        print("Name Of Variables : ")
        self.printfuncvariables(functionID)
        print("Number Of Variables: " + self.directory[functionID]['numberVars'])