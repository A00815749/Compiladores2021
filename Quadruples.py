class Quadruples:
    def __init__(self):
        self.Quads = []

    def addQuad(self,op,leftOperand,rightOperand, result):
        self.Quads.append(
            {
                'QuadrupleNumber' : len(self.Quads),
                'Operator' : op,
                'LeftOperand' : leftOperand,
                'RightOperand' : rightOperand,
                'Result' : result
            }
        )
    
    def changeQuad(self,op,leftOperand,rightOperand,result,address):
        self.Quads[address] = {
                'QuadrupleNumber' : self.Quads[address]['QuadrupleNumber'],
                'Operator' : op,
                'LeftOperand' : leftOperand,
                'RightOperand' : rightOperand,
                'Result' : result
        }
    
    def getQuadAdd(self,address):
        return self.Quads[address]

    def printQuad(self):
        for Quad in self.Quads:
            print (str(Quad['QuadrupleNumber'])
            + '    ' + str(Quad['Operator'])
            + '    ' + str(Quad['LeftOperand'])
            + '    ' + str(Quad['RightOperand'])
            + '    ' + str(Quad['Result']))