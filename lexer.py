# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:04:25 2021

@author: guims
"""


from rply import LexerGenerator

class Lexer():
    
    def __init__(self):
        self.lexer = LexerGenerator()
        
    
    def _add_tokens(self):
        
       
        # Integer literal
        self.lexer.add('integer-literal', r'(0x[0-9a-fA-F]+|\d+)')
        
        # Type identifier
        self.lexer.add('type-identifier', r'[A-Z]([a-zA-Z]|\d+|_)*')
        
        # Object identifier
        self.lexer.add('object-identifier', r'[a-z]([a-zA-Z]|\d+|_)*')
        
        # String literal
#        regular_char = '[a-zA-Z0-9 ]'
#        hex_digit = '[0-9a-fA-F]'
#        escape_sequence = '(b|t|n|r|\"|\\|x'+hex_digit+hex_digit+'|\n( |\t)*)'
#        escape_char = '\\'+escape_sequence
        
        #self.lexer.add('string-literal', r"\"("+regular_char+"|"+escape_char+")*\"")
        self.lexer.add('string-literal', r"\"([a-zA-Z0-9 ]|\\(b|t|n|r|\"|\\|x[0-9a-fA-F][0-9a-fA-F]|\n( |\t)*))*\"")
        
        # Operators
        
        # Assignment
        self.lexer.add('assign', r'\<-')
        
        # Braces
        self.lexer.add('lbrace', r'\{')
        self.lexer.add('rbrace', r'\}')
        
        # Parenthesis
        self.lexer.add('lpar', r'\(')
        self.lexer.add('rpar', r'\)')
        
        # Ponctuation
        self.lexer.add('colon', r':')
        self.lexer.add('semicolon', r';')
        self.lexer.add('comma', r',')
        self.lexer.add('dot', r'\.')
        
        # Operations
        self.lexer.add('plus', r'\+')
        self.lexer.add('minus', r'\-')
        self.lexer.add('times', r'\*')
        self.lexer.add('div', r'/')
        self.lexer.add('pow', r'/^')
        
        # Boolean
        self.lexer.add('lower-equal', r'\<=')
        self.lexer.add('equal', r'\=')
        self.lexer.add('lower', r'\<')
        
        
        
        
        # Ignore whitespaces (spaces, horizontal tabs, line feed(new line) carriage return, form feed and vertical feed)
        self.lexer.ignore(r'\s+')
        
        # Ignore comments
        self.lexer.ignore(r'//.*')
        self.lexer.ignore(r'\(\*(?s).*\*\)')
        
        
    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
        
        
        
        
        