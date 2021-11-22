from memorymap import VirtualMemory
from myStack import myStack
import json

class QuadOps:
    def __init__(self):
        self.virtualmemory = VirtualMemory()
        self.jumps = myStack()
    
    def loadConstants(self,constants):
        for x in constants:
            actualconstant = json.loads(x)
            print(str(actualconstant['Constant']))
            print(str(actualconstant['VirtualAddress']))
            self.virtualmemory.updateMemory(actualconstant['VirtualAddress'],actualconstant['Constant'])

    def assign(self,quad):
        leftoperand = quad['LeftOperand']
        result = quad['Result']
        print(str(quad))
        print("assign to => ",self.virtualmemory.getVal(leftoperand))
        self.virtualmemory.updateMemory(result,self.virtualmemory.getVal(leftoperand))

    def write(self,quad):
        print("Write quadruple => ",quad)
        value = self.virtualmemory.getVal(quad['Result'])

    def read(self,quad):
        val = input()
        try:
            finalvalue = int(val)
        except ValueError:
            try:
                finalvalue = float(val)
            except:
                finalvalue = val
        result = quad['Result']
        self.virtualmemory.updateMemory(result,val)
    
    def goto(self,quad):
        return quad['Result']

    def gotof(self,quad):
        if not self.virtualmemory.getVal(quad['LeftOperand']):
            return quad['Result']
        return None

    def gotot(self,quad):
        if self.virtualmemory.getVal(quad['LeftOperand']):
            return quad['Result']
        return None

    def plusOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand + rightOperand)

    def restOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand - rightOperand)

    def timesOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand * rightOperand)
    
    def divideOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand / rightOperand)

    def sameOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand == rightOperand)

    def andOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand and rightOperand)

    def orOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand or rightOperand)
    
    def notsameOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand != rightOperand)

    def greaterOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand > rightOperand)

    def greaterandOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand >= rightOperand)

    def lesserOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand < rightOperand)

    def lesserandOp(self,quad):
        leftOperand = self.virtualmemory.getVal(quad['LeftOperand'])
        rightOperand = self.virtualmemory.getVal(quad['RightOperand'])
        self.virtualmemory.updateMemory(quad['Result'],leftOperand <= rightOperand)

    def eraOp(self,quad):
        self.virtualmemory.renewLocalMemory()
        return None

    def verOp(self,quad):
        arrayPos = self.virtualmemory.getVal(quad['LeftOperand'])
        arraylower = self.virtualmemory.getVal(quad['RightOperand'])
        arrayupper = self.virtualmemory.getVal(quad['Result'])
        if arrayPos < arraylower or arrayPos >= arrayupper:
            print ("Dynamic error, Array index out of bounds")

    def endprocOp(self,quad):
        backup = self.jumps.pop() + 1
        self.virtualmemory.restoreLocalMemory()
        return backup
    
    def paramOp(self,quad):
        self.virtualmemory.insertArg(self.virtualmemory.getVal(quad['RightOperand']))
        return None
    
    def gosubOp(self,quad):
        self.virtualmemory.backupLocalMemory()
        self.virtualmemory.updateLocalMemory()
        self.jumps.push(quad['QuadrupleNumber'])
        return quad ['Result']

    def returnOp(self,quad):
        self.virtualmemory.updateMemory(quad['LeftOperand'],self.virtualmemory.getVal(quad['Result']))
        return None







