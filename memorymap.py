class Memorymap:
    def _init_(self):
        self.GlobalVars = {}
        self.LocalVars = {}
        self.ConstantVars = {}
        self.TempVars = {}
        #My quadfunctions, ie operators numbers are simple, arent they?
        self.operators = {
            '+' : 1,
            '-' : 2,
            '*' : 3,
            '/' : 4,
            '<' : 5,
            '<=' : 6,
            '>' : 7,
            '>=' : 8,
            '==' : 9,
            '<>' : 10,
            '&' : 11,
            '|' : 12,
            '=' : 13,
            'for' : 14,
            'while' : 15,
            'read' : 16,
            'write' : 17,
            'GOTOMAIN' : 18,
            'ERA' : 19,
            'PARAM' : 20,
            'ENDPROC' : 21,
            'GOSUB' : 22,
            'VER' : 23,
            'GOTO' :  24,
            'GOTOF' : 25,
            'GOTOV' :  26,
        }
        self.blocks = {
            'GlobalVars' : {
                'Int' : 1000,
                'Float' : 2000,
                'Char' : 3000,
            },
            'LocalVars' : {
                'Int' : 4000,
                'Float' : 5000,
                'Char' : 6000,
            },
            'TempVars' : {
                'Int' : 7000,
                'Float' : 8000,
                'Char' : 9000,
                'Bool' : 10000,
            },
            'ConstantVars' : {
                'Int' : 11000,
                'Float' : 12000,
                'Char' : 13000,
            }
        }
        self.StackOverflow = {
            'GlobalVars' : {
                'Int' : 2000,
                'Float' : 3000,
                'Char' : 4000,
            },
            'LocalVars' : {
                'Int' : 5000,
                'Float' : 6000,
                'Char' : 7000,
            },
            'TempVars' : {
                'Int' : 8000,
                'Float' : 9000,
                'Char' : 10000,
                'Bool' : 11000,
            },
            'ConstantVars' : {
                'Int' : 12000,
                'Float' : 13000,
                'Char' : 14000,
            }
        }
        
    def getOper(self,operator):
        return self.operators[operator]

    def assignVirtualMemory(self,scope,type):
        if self.blocks[scope][type] < self.StackOverflow[scope][type]:
            self.blocks[scope][type] += 1
            return self.blocks[scope][type]
        else:
            print("Stack overflowed you dingus")

    def resetLocalMemory(self): # Our function memory reutilization
        self.TempVars = {}
        self.blocks['LocalVars']['Int'] = 4000
        self.blocks['LocalVars']['Float'] = 5000
        self.blocks['LocalVars']['Char'] = 6000
        self.blocks['TempVars']['Int'] = 7000
        self.blocks['TempVars']['Float'] = 8000
        self.blocks['TempVars']['Char'] = 9000
        self.blocks['TempVars']['Bool'] = 10000

class VirtualMemory:
    def _init_(self):
        self.memory = {
            'GlobalVars' : {},
            'LocalVars' : {},
            'TemporalVars' : {},
            'ConstantVars' : {},
            'Pointers' : {}
        }
        self.Globallower = 1000
        self.Globalupper = 3999
        self.Locallower = 4000
        self.Localupper = 6999
        self.Templower = 7000
        self.Tempupper = 10999
        self.Constantlower = 11000
        self.ConstantUpper = 14999
        self.localcache = {}
        self.counter = 1000
        self.memorybacker = {
            'LocalVars' : [],
            'TempVars' : []
        }

    def changeaddr(self,virtualaddr,scope,val):
        self.memory[scope][virtualaddr] = val

    def getValinMemory(self,virtualaddr,scope):
        if virtualaddr in self.memory[scope]:
            return self.memory[scope][virtualaddr]
        else:
            print ("Memory not used")

    def getVal(self,virtualaddr):
        if self.Globallower <= virtualaddr <= self.Globalupper:
            return self.getValinMemory(virtualaddr,'GlobalVars')
        if self.Locallower <= virtualaddr <= self.Localupper:
            return self.getValinMemory(virtualaddr,'LocalVars')
        if self.Templower <= virtualaddr <= self.Tempupper:
            return self.getValinMemory(virtualaddr,'TemporalVars')
        if self.Constantlower <= virtualaddr <= self.ConstantUpper:
            return self.getValinMemory(virtualaddr,'ConstantVars')

    def renewLocalMemory(self):
        self.memorybacker = {}
        self.counter = 1000

    def backupLocalMemory(self):
        self.memorybacker['LocalVars'].append(self.memory['LocalVars'])
        self.memorybacker['TempVars'].append(self.memory['TemporalVars'])

    def restoreLocalMemory(self):
        self.memory['LocalVars'] = self.memorybacker['LocalVars'].pop()
        self.memory['TemporalVars'] = self.memorybacker['TempVars'].pop()
    
    def updateLocalMemory(self):
        self.memory['LocalVars'] = self.localcache
        self.memory['TemporalVars'] = {}
    
    def updateMemory(self,virtualaddr,val):
        if self.Globallower <= virtualaddr <= self.Globalupper:
            return self.changeaddr(virtualaddr,'GlobalVars',val)
        if self.Locallower <= virtualaddr <= self.Localupper:
            return self.changeaddr(virtualaddr,'LocalVars',val)
        if self.Templower <= virtualaddr <= self.Tempupper:
            return self.changeaddr(virtualaddr,'TemporalVars',val)
        if self.Constantlower <= virtualaddr <= self.ConstantUpper:
            return self.changeaddr(virtualaddr,'ConstantVars',val)

    def insertArg(self,val):
        self.localcache[self.counter] = val
        self.counter += 1