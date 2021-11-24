#Tests by Andres Carlos Barrera A00815749
import ply.lex as lex
import ply.yacc as yacc
import sys

from myLexer import *
from myParser import *

# create objects MY LEXER and MY PARSER
myLex = MyLexer()
myPars = MyParser(myLex)

lex = myLex.lexer
parser = myPars.parser

# reading INPUT FILE
##ALTERNATIVE FILEHANDLER
arch = input("Nombre del archivo para compilar: ")
import ply.yacc as yacc
parser = yacc.yacc()
f = open ("./"+arch, "r")
input = f.read
parser.parse(input,debug = 0)
output = open("Quads.mir","w")
for x in QUADRUPLESlist:
    output.write(str(x.QUADcounter)+ "~" + str(x.operator) + "~" + str(x.LeftOperand)+ "~" + str(x.RightOperand) + "~" + str(x.result) + "\n")
output.close()