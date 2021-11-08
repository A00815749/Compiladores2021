import sys

class Vartables:
    def _init_(self):
        self.variablelist = {} #The constructor of the dictionary for variables storage

    def add(self, id, type):
        self.variablelist[id] = { # Adding type variable so we can do semantic checks later
            'type' : type

    }

    def searchvar(self, id):
        return id in self.variablelist

    def printvar(self):
        for x in self.variablelist:
            print(x, ' Var in the list ')