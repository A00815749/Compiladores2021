class VirtualMemory:
    def _init_(self):
        self.GlobalVars = {}
        self.LocalVars = {}
        self.ConstantVars = {}
        self.TempVars = {}
        
        #My quadfunctions, ie operators

        self.operators = {
            '+' : 1,
            '=' : 2,
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
            'GOTO' :  23,
            'GOTOF' : 24,
            'GOTOV' :  25,
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
            }
        }
        
    def getOper(self,operator):
        return self.operators[operator]
    def assignVirtualMemory(self,scope,type):
        # THIS IS WHERE THE ARRAY WILL CAUSE PROBLEMS noooooo
        if self.blocks[scope][type] <self.StackOverflow[scope][type]:
            self.blocks[scope][type] += 1
            return self.blocks[scope][type]
    
    def resetLocalMemory(self): # Our function memory reutilization
        self.TempVars = {}
        self.blocks['LocalVars']['Int'] = 4000
        self.blocks['LocalVars']['Float'] = 5000
        self.blocks['LocalVars']['Char'] = 6000
        self.blocks['TempVars']['Int'] = 7000
        self.blocks['TempVars']['Float'] = 8000
        self.blocks['TempVars']['Char'] = 9000
        self.blocks['TempVars']['Bool'] = 10000