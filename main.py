# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 17:53:55 2021

@author: guims
"""

from lexer import Lexer


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
tokens = lexer.lex('My_ass s : test {} <- ifthen 5 // This is a. comment (* Here is a comment. (* Valid nested comment. *) Still commented. *) ')

for token in tokens:
    
    if token.value in keywords:
        token.name = token.value # Replace TOKEN_CLASS by keyword
    
    if any(token.name == TOKEN_CLASS for TOKEN_CLASS in ('integer-literal', 'type-identifier', 'object-identifier', 'type-identifier', 'string-literal')):
        print("{0},{1},{2},{3}".format(token.source_pos.lineno, token.source_pos.colno, token.name, token.value))
    
    else:
        print("{0},{1},{2}".format(token.source_pos.lineno, token.source_pos.colno, token.name))