# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 17:53:55 2021

@author: guims
"""

from lexer import Lexer



lexer = Lexer().get_lexer()
tokens = lexer.lex('My_ass')

for token in tokens:
    print(token)