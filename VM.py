from QuadrupleOps import QuadOps
import json

QuadOperations = QuadOps()
operators = {
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

operationindexer = {
            1 : QuadOperations.plusOp,
            2 : QuadOperations.restOp,
            3 : QuadOperations.timesOp,
            4 : QuadOperations.divideOp,
            5 : QuadOperations.lesserOp,
            6 : QuadOperations.lesserandOp,
            7 : QuadOperations.greaterOp,
            8 : QuadOperations.greaterandOp,
            9 : QuadOperations.sameOp,
            10 : QuadOperations.notsameOp,
            11 : QuadOperations.andOp,
            12 : QuadOperations.orOp,
            13 : QuadOperations.assign,
            14 : None,
            15 : None,
            16 : QuadOperations.read,
            17 : QuadOperations.write,
            18 : QuadOperations.goto,
            19 : QuadOperations.eraOp,
            20 : QuadOperations.paramOp,
            21 : QuadOperations.endprocOp,
            22 : QuadOperations.gosubOp,
            23 : QuadOperations.verOp,
            24 : QuadOperations.goto,
            25 : QuadOperations.gotof,
            26 : QuadOperations.gotot,
}
quadruples = []
quadcounter = 0