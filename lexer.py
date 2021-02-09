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
        self.lexer.add('integer-literal', r'(\d+|0x[0-9a-fA-F]+)')
        
        # Type identifier
        self.lexer.add('type-identifier', r'[A-Z]([a-zA-Z]|\d+|_)*')
        
        # Object identifier
        self.lexer.add('object-identifier', r'[a-z]([a-zA-Z]|\d+|_)*')
        
        
        # Operators
        
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
        self.lexer.add('equal', r'\=')
        self.lexer.add('lower', r'\<')
        self.lexer.add('lower-equal', r'\<=')
        
        # Assignment
        self.lexer.add('assign', r'\<-')
        
        # Ignore spaces
        self.lexer.ignore('\s+')
        
        
    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
        
        
        
        
        