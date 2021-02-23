# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:04:25 2021

@author: guims
"""


import ply.lex as lex
import sys
import re
from collections import deque


class VsopLexer():

    def __init__(self, file_name, string_text):
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
        pass

    tokens = [
        'INTEGER_LITERAL',
        'error',
        'INTEGER_ERROR',
        'TYPE_IDENTIFIER',
        'OBJECT_IDENTIFIER',
        'string_literal',
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
        ('STRING', 'exclusive')
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
    t_POW = r'\^'


    t_LOWER_EQUAL = r'\<='
    t_EQUAL = r'\='
    t_LOWER = r'\<'

    def t_INTEGER_LITERAL(self, t):
        r'(0x[0-9a-fA-F][ \t]+|\d+((\n|\r|\r\n)| |\s|\t|\Z))'
        if t.value.startswith('0x'):
            t.value = str(int(t.value.replace('0x', ''), 16))
        elif not t.value == "0":
            t.value = re.sub(r'^0*', '', t.value)
            # if len(re.sub("[0-9]", "", t.value)) != 0:
            #     colno = self.find_column(self.string_text, t)
            #     sys.stderr.write("{0}:{1}:{2}: lexical error: {3} is not a valid integer literal\n".format(self.file_name, t.lineno, colno, t.value[0]))
            #     t.type = "error"
        return t

    def t_INTEGER_ERROR(self,t):
        r'(0x[0-9a-fA-F]*[g-zG-Z]+[0-9g-zG-Z]*|0x|d+.)'
        colno = self.find_column(self.string_text, t)
        sys.stderr.write("{0}:{1}:{2}: lexical error: {3} is not a valid integer literal\n".format(self.file_name, t.lineno, colno, t.value[0]))
        t.type = "error"
        return t

    def t_TYPE_IDENTIFIER(self, t):
	    r'[A-Z]([a-zA-Z]|\d+|_)*'
	    return t

    def t_OBJECT_IDENTIFIER(self, t):
	    r'[a-z]([a-zA-Z]|\d+|_)*'
	    return t

    t_ignore  = ' \t'

    def t_newline(self, t):
	     r'\n+'
	     t.lexer.lineno += len(t.value)

    def find_column(self, input, token):
	     line_start = input.rfind('\n', 0, token.lexpos) + 1
	     return (token.lexpos - line_start) + 1

    def t_lineComment(self,t):
        r'(//.*(\n|\Z))'
        t.lexer.lineno += 1
        pass

    def t_error(self, t):
        colno = self.find_column(self.string_text, t)
        sys.stderr.write("{0}:{1}:{2}: lexical error: {3} is not a valid VSOP character\n".format(self.file_name, t.lineno, colno, t.value[0]))
        t.type = "error"
        return t

    def t_INITIAL_string(self,t):
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
            self.lexer.begin('INITIAL')
        
    

    def t_STRING_string_literal(self,t):
        r'((?!\\|\"|\').|(\\(b|t|n|r|\"|\\|x[0-9a-fA-F][0-9a-fA-F]|([ \t])*\n)))+'
        returns = sum(1 for m in re.finditer(r"\\([ \t])*\n", t.value))
        if returns > 0:
            t.value = re.sub(r"\\([ \t])*\n([ \t])*", '', t.value)
            t.lexer.lineno += returns
        t.value = '\"' + t.value + '\"'
        t.value = t.value.replace('\\t', '\\x09')
        t.value = t.value.replace('\\n', '\\x0a')
        t.value = t.value.replace('\\b', '\\x08')
        t.value = t.value.replace('\\r', '\\x0d')
        t.value = t.value.replace('\\\\', '\\x5c')
        t.value = t.value.replace('\\"', '\\x22')
        return t
    
    def t_STRING_invalid(self,t):
        r'\\((?!\").)* '
        pos = (t.lineno, self.find_column(self.string_text, t))
        sys.stderr.write("{0}:{1}:{2}: lexical error: invalid escape sequence {3}\n".format(self.file_name, pos[0], pos[1], t.value))
        t.type = "error"
        return t
    
    def t_STRING_eof(self,t):
        
        if self.double_quoteNB%2 !=0:
            pos = self.string_pos
            sys.stderr.write("{0}:{1}:{2}: lexical error: string literal is not terminated when end-of-file is reached\n".format(self.file_name, pos[0], pos[1]))
            t.type = "error"
            return t
        
    def t_STRING_return(self,t):
        r'\n'
        pos = (t.lineno, self.find_column(self.string_text, t))
        sys.stderr.write("{0}:{1}:{2}: lexical error: raw line feed not permitted inside a string\n".format(self.file_name, pos[0], pos[1]))
        t.type = "error"
        return t

    t_STRING_ignore = ""

    def t_STRING_error(self,t):
        pass

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
        if(t.value == "\n" or t.value == "\r\n"):
            t.lexer.lineno += 1
        pass

    t_COMMENT_ignore = " \t"


    def t_COMMENT_eof(self, t):

        # multi-line eof error

        pos = self.comment_pos.pop()
        sys.stderr.write("{0}:{1}:{2}: lexical error: multi-line comment is not terminated when end-of-file is reached\n".format(self.file_name, pos[0], pos[1]))
        t.type = "error"
        return t


    def t_COMMENT_error(self,t):
        r'.'
        print("ERROR:", t.value)
        return t
