# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 17:53:55 2021

@author: guims
"""

import argparse
import sys
from lexer import Lexer


parser = argparse.ArgumentParser()
parser.add_argument("-lex", "-lex", dest='source_file', help="Path to the VSOP source code", required=True)
args = parser.parse_args()

text_file = open(args.source_file, "r")
string_text = text_file.read()
text_file.close()

if len(string_text) == 0 :
    sys.stdout.write("Source code file is empty")

keywords = {
    'and': 'and',
    'bool':'bool',
    'class':'class',
    'do':'do',
    'else':'else',
    'extends':'extends',
    'false':'false',
    'if':'if',
    'in':'in',
    'int32':'int32',
    'isnull':'isnull',
    'let':'let',
    'new':'new',
    'not':'not',
    'self':'self',
    'string':'string',
    'then':'then',
    'true':'unit',
    'while':'while'
    }

lexer = Lexer().get_lexer()
tokens = lexer.lex(string_text)

for token in tokens:
    
    if token.value in keywords:
        token.name = token.value # Replace TOKEN_CLASS by keyword
    
    if any(token.name == TOKEN_CLASS for TOKEN_CLASS in ('integer-literal', 'type-identifier', 'object-identifier', 'type-identifier', 'string-literal')):
        sys.stdout.write("{0},{1},{2},{3}\n".format(token.source_pos.lineno, token.source_pos.colno, token.name, token.value))
    
    else:
        sys.stdout.write("{0},{1},{2}\n".format(token.source_pos.lineno, token.source_pos.colno, token.name))