# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:04:25 2021

@author: guims
"""


import ply.lex as lex
import sys
from collections import deque


class VsopLexer():

    def __init__(self, file_name, string_text):
        'Lexer constructor called.'
        self.lexer = lex.lex(module=self)
        self.file_name = file_name
        self.string_text = string_text

        # multi-line comment variables
        self.op_commentNb = 0
        self.cl_commentNb = 0
        self.comment_pos = deque()
        self.lexer.begin('INITIAL')

        # string literal variables
        self.double_quoteNB = 0
        self.string_pos = (0,0)

    def __del__(self):
        print('Lexer destructor called.')


    tokens = [
        'INTEGER_LITERAL',
        'INTEGER_ERROR',
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

    states = (
        ('COMMENT','exclusive'),
    )

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


    def t_INTEGER_ERROR(self,t):
        r'0x[0-9a-fA-F]*[g-zG-Z]+[0-9g-zG-Z]*'
        return t

    def t_INTEGER_LITERAL(self, t):
	    r'(0x[0-9a-fA-F]+|\d+)'
	    return t


    def t_TYPE_IDENTIFIER(self, t):
	    r'[A-Z]([a-zA-Z]|\d+|_)*'
	    return t

    def t_OBJECT_IDENTIFIER(self, t):
	    r'[a-z]([a-zA-Z]|\d+|_)*'
	    return t


    def t_INITIALS_string(self,t):
        r'\"'
        colno = self.find_column(self.string_text, t)
        self.double_quoteNB +=1
        self.string_pos = (t.lineno, colno)
        self.lexer.begin('STRING')
        
    def t_STRING_end(self,t):
        r'\"'
        colno = self.find_column(self.string_text, t)
        self.double_quoteNB +=1
        self.string_pos = (t.lineno, colno)
        if(self.double_quoteNB%2==0):
            self.lexer.begin('INITIALS')
            
            
    def t_STRING_body(self,t):
        r'([a-zA-Z0-9 ]|\\(b|t|n|r|\"|\\|x[0-9a-fA-F][0-9a-fA-F]|\s)*)*'
        return t
    
    
    def t_STRING_eof(self,t):
        
        if self.double_quoteNB%2 !=0:
            pos = self.string_pos
            sys.stderr.write("{0}:{1}:{2}: string literal is not terminated when end-of-file is reached\n".format(self.file_name, pos[0], pos[1]))
        
    def t_STRING_error(self,t):
        r'.'
        print("ERROR:", t.value)
        return t
    
#     def t_STRING_LITERAL(self, t):
# 	    r"\"([a-zA-Z0-9 ]|\\(b|t|n|r|\"|\\|x[0-9a-fA-F][0-9a-fA-F]|\s)*)*\""
# 	    return t

#     def t_string_quote(self,t):
#         r'\"'
#         colno = self.find_column(self.string_text, t)
#         if self.double_quoteNB%2==0:
#            self.double_quoteNB +=1
#            self.string_pos = (t.lineno, colno)
#         else:
#             self.double_quoteNB +=1



    def t_newline(self, t):
	     r'\n+'
	     t.lexer.lineno += len(t.value)

    def find_column(self, input, token):
	     line_start = input.rfind('\n', 0, token.lexpos) + 1
	     return (token.lexpos - line_start) + 1

    t_ignore  = ' \t'


    def t_lineComment(self,t):
        r'(//.*\n)'
        t.lexer.lineno += 1
        pass

    def t_error(self, t):
        colno = self.find_column(self.string_text, t)
        sys.stderr.write("{0}:{1}:{2}: {3} is not a valid VSOP character\n".format(self.file_name, t.lineno, colno, t.value[0]))
        t.lexer.skip(1)


    def t_INITIAL_comm(self,t):
        r'\(\*'
        colno = self.find_column(self.string_text, t)
        self.op_commentNb+=1
        self.comment_pos.append((t.lineno,colno))
        self.lexer.begin('COMMENT')
        pass

    def t_COMMENT_end(self,t):
        r'\*\)'
        self.cl_commentNb+=1
        self.comment_pos.pop()
        if(self.op_commentNb == self.cl_commentNb):
            self.lexer.begin('INITIAL')
        pass

    def t_COMMENT_supp(self,t):
        r'\(\*'
        colno = self.find_column(self.string_text, t)
        self.op_commentNb+=1
        self.comment_pos.append((t.lineno,colno))
        pass

    def t_COMMENT_body(self,t):
        r'.'
        pass

    def t_COMMENT_nl(self,t):
        r'(\n|\r|\r\n)|\s|\t'
        pass

    t_COMMENT_ignore = " \t"


    def t_COMMENT_eof(self, t):

        # multi-line eof error

        pos = self.comment_pos.pop()
        sys.stderr.write("{0}:{1}:{2}: multi-line comment is not terminated when end-of-file is reached\n".format(self.file_name, pos[0], pos[1]))


    def t_COMMENT_error(self,t):
        r'.'
        print("ERROR:", t.value)
        return t



    # def t_eof(self, t):

    #     if self.double_quoteNB%2 !=0:
    #         pos = self.string_pos
    #         sys.stderr.write("{0}:{1}:{2}: string literal is not terminated when end-of-file is reached\n".format(self.file_name, pos[0], pos[1]))
