# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:04:25 2021

@author: guims
"""


import ply.lex as lex


tokens = (
    'integer-literal',
    'type-identifier',
    'object-identifier',
    'string-literal',
    'assign',
    'lbrace',
    'rbrace',
    'lpar',
    'rpar',
    'colon',
    'semicolon',
    'comma',
    'dot',
    'plus',
    'minus',
    'times',
    'div',
    'pow',
    'lower-equal',
    'equal',
    'lower'
   )

# Regular expression rules for tokens


t_assign = r'\<-'

t_lbrace = r'\{'
t_rbrace = r'\}'

t_lpar = r'\('
t_rpar = r'\)'

t_colon = r':'
t_semicolon =  r';'
t_comma = r','
t_dot = r'\.'
        

t_plus = r'\+'
t_minus = r'\-' 
t_times =  r'\*'
t_div = r'/'
t_pow = r'/^'


t_lowerequal = r'\<='
t_equal = r'\='
t_lower = r'\<'

t_ignore = r'(\s+|//.*|\(\*(?s).*\*\))'


def t_integer(t):
    r'(0x[0-9a-fA-F]+|\d+)'
    return t

def t_type(t):
    r'[A-Z]([a-zA-Z]|\d+|_)*'
    return t

def t_object(t):
    r'[a-z]([a-zA-Z]|\d+|_)*'
    return t

def t_string(t):
    r"\"([a-zA-Z0-9 ]|\\(b|t|n|r|\"|\\|x[0-9a-fA-F][0-9a-fA-F]|\s)*)*\""
    return t
    
def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
     
def find_column(input, token):
     line_start = input.rfind('\n', 0, token.lexpos) + 1
     return (token.lexpos - line_start) + 1


lexer = lex.lex()
        
        
        
        