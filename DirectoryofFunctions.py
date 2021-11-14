from Vartables import Vartables
import sys

#The Directory for functions and all that fun 
class DirectoryFunctions:
    def _init_(self):
        self.directory = {}

    def addfunc(self, type, functionID,numPar,typePar,nameofPar, numVars):
        if(functionID not in self.directory.keys()): #Is the function already in the list to not cause conflicts
            self.directory[functionID] = {
                'type' : type,
                'numPar' : numPar,
                'typePar' : typePar,
                'nameofPar' : nameofPar,
                'localvars' : Vartables(),
                #probably using a method later for the numvars
                'numberVars' : numVars 
            }
            print("Check, function ", functionID, ' ', type)

        else:
            print ("Error, function already in the directory of functions ", functionID)

    def searchFunc(self,id): #Search method
        return id in self.directory

    def searchVar(self,Varid,functionid):
        if (self.directory[functionid]['localvars'].searchvar(Varid)):
            return True
        else:
            print ("Var ", Varid, " not found")

    def getVarType(self, Varid,functionid):
        if self.directory[functionid]['localvars'].searchvar(Varid):
            return self.directory[functionid]['localvars'].getType(Varid)
        else:
            print("Variable: ", Varid, " cant be accessed to get typing")

    def addVar(self,functionID, type, currentID):
        if (self.directory[functionID]['localvars'].searchvar(currentID)):
            print("This variable is already in the function ", currentID)
        else:
            self.directory[functionID]['localvars'].add(currentID, type)
            print("Var added to function local table ", functionID)
            

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