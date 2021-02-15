# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:04:25 2021

@author: guims
"""


import ply.lex as lex

class VsopLexer():
	def __init__(self):
		print('Lexer constructor called.')
		self.lexer = lex.lex(module=self)
		
	def __del__(self):
		print('Lexer destructor called.')
		

	tokens = [
	    'INTEGER_LITERAL',
	    'TYPE_IDENTIFIER',
	    'OBJECT_IDENTIFIER',
	    'STRING_LITERAL',
	    'ASSIGN',
	    'LBRACE',
	    'RBRACE',
	    'LPAR',
	    'RPAR',
	    'COLON',
	    'SEMICOLON',
	    'COMMA',
	    'DOT',
	    'PLUS',
	    'MINUS',
	    'TIMES',
	    'DIV',
	    'POW',
	    'LOWER_EQUAL',
	    'EQUAL',
	    'LOWER',
		'SPACES',
		'COMMENTS'
	   ]

# Regular expression rules for tokens


	t_ASSIGN = r'\<-'
	
	t_LBRACE = r'\{'
	t_RBRACE = r'\}'
	
	t_LPAR = r'\('
	t_RPAR = r'\)'
	
	t_COLON = r':'
	t_SEMICOLON =  r';'
	t_COMMA = r','
	t_DOT = r'\.'
	        
	
	t_PLUS = r'\+'
	t_MINUS = r'\-' 
	t_TIMES =  r'\*'
	t_DIV = r'/'
	t_POW = r'/^'
	
	
	t_LOWER_EQUAL = r'\<='
	t_EQUAL = r'\='
	t_LOWER = r'\<'
	
	
	
	def t_INTEGER_LITERAL(self, t):
	    r'(0x[0-9a-fA-F]+|\d+)'
	    return t
	
	def t_TYPE_IDENTIFIER(self, t):
	    r'[A-Z]([a-zA-Z]|\d+|_)*'
	    return t
	
	def t_OBJECT_IDENTIFIER(self, t):
	    r'[a-z]([a-zA-Z]|\d+|_)*'
	    return t
	
	def t_STRING_LITERAL(self, t):
	    r"\"([a-zA-Z0-9 ]|\\(b|t|n|r|\"|\\|x[0-9a-fA-F][0-9a-fA-F]|\s)*)*\""
	    return t
	    
	def t_newline(self, t):
	     r'\n+'
	     t.lexer.lineno += len(t.value)
	     
	def find_column(self, input, token):
	     line_start = input.rfind('\n', 0, token.lexpos) + 1
	     return (token.lexpos - line_start) + 1
	 
	t_ignore  = ' \t'
	
#	def t_COMMENTS(self, t):
#	    r'(//.*|\(\*(?s).*\*\))'
#	    pass
	
	def t_error(self, t):
	     print("Illegal character '%s'" % t.value[0])
	     t.lexer.skip(1)

        
        