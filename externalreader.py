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

myFile = open(sys.argv[1])
parser.parse(myFile.read())