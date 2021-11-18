import sys

class Variable(): #Single variable class
    def _init_(self,type,id):
        self.type = type
        self.id = id

class Vartables: #Variable table types, redundancy wut the typing?
    def _init_(self):
        self.variablelist = {} #The constructor of the dictionary for variables storage

    def add(self, id, type):
        self.variablelist[id] = { # Adding type variable so we can do semantic checks later
            'type' : type

    }

    def searchvar(self, id):
        return id in self.variablelist.keys()

    def printvar(self):
        for x in self.variablelist:
            print(x, ' Var in the list ')

    def getType(self,id):
        return self.variablelist[id]['type']

class TemporalVar(object): #The datastructure/object that tracks our temporal variables in the quadruples
    def _init_(self):
        self.counter = 0
        self.tempvar = 't'

    def next(self):
        self.counter += 1
        return self.tempvar + str(self.tempvar)

    def reset(self):
        self.counter = 0