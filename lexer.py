# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:04:25 2021

@author: Guilherme Madureira & Julien Carion
"""


import ply.lex as lex
import sys
import re
from collections import deque


class VsopLexer():

    def __init__(self, file_name, string_text):
        self.lexer = lex.lex(module=self, errorlog=lex.NullLogger())
        self.file_name = file_name
        self.string_text = string_text
        self.tokens = []

        # multi-line comment variables
        self.op_commentNb = 0
        self.cl_commentNb = 0
        self.comment_pos = deque()
        self.lexer.begin('INITIAL')

        # string literal variables
        self.double_quoteNB = 0
        self.string_pos = (0,0)
        self.string_empty = True

    def __del__(self):
        pass

    tokens = [
        'AND',
        'BOOL',
        'CLASS',
        'DO',
        'ELSE',
        'EXTENDS',
        'FALSE',
        'IF',
        'IN',
        'INT32',
        'ISNULL',
        'LET',
        'NEW',
        'NOT',
        'SELF',
        'STRING',
        'THEN',
        'TRUE',
        'UNIT',
        'WHILE',
        'INTEGER_LITERAL',
        'Lexicalerror',
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

    def t_AND(self, t):
        r'\band\b'
        return t

    def t_UNIT(self, t):
        r'\bunit\b'
        return t

    def t_ISNULL(self, t):
        r'\bisnull\b'
        return t
    
    def t_NOT(self, t):
        r'not'
        return t

    def t_IF(self, t):
        r'\bif\b'
        return t

    def t_BOOL(self, t):
        r'\bbool\b'
        return t

    def t_CLASS(self, t):
        r'\bclass\b'
        return t

    def t_DO(self, t):
        r'\bdo\b'
        return t

    def t_ELSE(self, t):
        r'\belse\b'
        return t

    def t_EXTENDS(self, t):
        r'\bextends\b'
        return t

    def t_FALSE(self, t):
        r'\bfalse\b'
        return t

    def t_IN(self, t):
        r'\bin\b'
        return t

    def t_INT32(self, t):
        r'\bint32\b'
        return t

    def t_LET(self, t):
        r'\blet\b'
        return t

    def t_NEW(self, t):
        r'\bnew\b'
        return t

    def t_SELF(self, t):
        r'\bself\b'
        return t

    def t_STRING(self, t):
        r'\bstring\b'
        return t

    def t_THEN(self, t):
        r'\bthen\b'
        return t

    def t_TRUE(self, t):
        r'\btrue\b'
        return t

    def t_WHILE(self, t):
        r'\bwhile\b'
        return t

    def t_INTEGER_LITERAL(self, t):
        r'(0x[0-9a-fA-F]+|\d+)([a-zA-Z]|\d+|_)*'

        # Changing hexadecimal to decimal
        if t.value.startswith('0x'):
            try: 
                t.value = str(int(t.value, 16))
            except:
                # Incorrect hexadeciaml values
                colno = self.find_column(self.string_text, t)
                sys.stderr.write("{0}:{1}:{2}: lexical error: {3} is not a valid integer literal\n".format(self.file_name, t.lineno, colno, t.value))
                t.type = "Lexicalerror"

        elif not t.value == "0":
            t.value = re.sub(r'^0*', '', t.value)
            # Detect wrong literal-integers (eg. 42g, 56t,...)
            if len(re.sub("[0-9]", "", t.value)) != 0:
                colno = self.find_column(self.string_text, t)
                sys.stderr.write("{0}:{1}:{2}: lexical error: {3} is not a valid integer literal\n".format(self.file_name, t.lineno, colno, t.value))
                t.type = "Lexicalerror"
        return t

    def t_TYPE_IDENTIFIER(self, t):
	    r'[A-Z]([a-zA-Z]|\d+|_)*'
	    return t

    def t_OBJECT_IDENTIFIER(self, t):
	    r'[a-z]([a-zA-Z]|\d+|_)*'
	    return t

    t_ignore  = ' \t'

    # Increment line number after line feed
    def t_newline(self, t):
	     r'\n+'
	     t.lexer.lineno += len(t.value)
    
    # Find column number at the begin of a token
    def find_column(self, input, token):
	     line_start = input.rfind('\n', 0, token.lexpos) + 1
	     return (token.lexpos - line_start) + 1

    # Detecting line comments
    def t_lineComment(self,t):
        r'(//.*(\n|\Z))'
        t.lexer.lineno += 1
        pass

    # Detecting invalid VSOP characters    
    def t_error(self, t):
        colno = self.find_column(self.string_text, t)
        sys.stderr.write("{0}:{1}:{2}: lexical error: {3} is not a valid VSOP character\n".format(self.file_name, t.lineno, colno, t.value[0]))
        t.type = "Lexicalerror"
        return t


    # Detecting string-literal with states
    def t_INITIAL_string(self,t):
        r'\"'
        self.string_empty = True
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
        if self.string_empty is True:
            t.type = "string_literal"
            t.value = '""'
            return t
        
    def t_STRING_string_literal(self,t):
        r'((?!\\|\").|(\\(b|t|n|r|\"|\\|x[0-9a-fA-F][0-9a-fA-F]|([ \t])*\n)))+'

        # Eliminating unecessary line feed and horizontal tabulations
        returns = sum(1 for m in re.finditer(r"\\([ \t])*\n", t.value))
        if returns > 0:
            t.value = re.sub(r"\\([ \t])*\n([ \t])*", '', t.value)
            t.lexer.lineno += returns
       
        # Replaces character escape sequences with ASCII values
        t.value = '\"' + t.value + '\"'
        t.value = t.value.replace('\\t', '\\x09')
        t.value = t.value.replace('\\n', '\\x0a')
        t.value = t.value.replace('\\b', '\\x08')
        t.value = t.value.replace('\\r', '\\x0d')
        t.value = t.value.replace('\\\\', '\\x5c')
        t.value = t.value.replace('\\"', '\\x22')
        self.string_empty = False
        return t
    

    # Invalid string-literal detection
    def t_STRING_invalid(self,t):
        r'\\((?!\").)* '
        pos = (t.lineno, self.find_column(self.string_text, t))
        sys.stderr.write("{0}:{1}:{2}: lexical error: invalid escape sequence {3}\n".format(self.file_name, pos[0], pos[1], t.value))
        t.type = "Lexicalerror"
        return t
    
    # EOF string-literal not ended
    def t_STRING_eof(self,t):
        if self.double_quoteNB%2 !=0:
            pos = self.string_pos
            sys.stderr.write("{0}:{1}:{2}: lexical error: string literal is not terminated when end-of-file is reached\n".format(self.file_name, pos[0], pos[1]))
            t.type = "Lexicalerror"
            return t
            
    # Invalid line feed inside a string-literal  
    def t_STRING_return(self,t):
        r'\n'
        pos = (t.lineno, self.find_column(self.string_text, t))
        sys.stderr.write("{0}:{1}:{2}: lexical error: raw line feed not permitted inside a string\n".format(self.file_name, pos[0], pos[1]))
        t.type = "Lexicalerror"
        return t

    #t_STRING_ignore = ""

    def t_STRING_error(self,t):
        pass
    
    # Detecting multi-line comments with states
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
    
    # Increments line number if new line inside comment
    def t_COMMENT_nl(self,t):
        r'(\n|\r|\r\n)|\s|\t'
        if(t.value == "\n" or t.value == "\r\n"):
            t.lexer.lineno += 1
        pass

    t_COMMENT_ignore = " \t"

    # Multi-line eof error
    def t_COMMENT_eof(self, t):
        pos = self.comment_pos.pop()
        sys.stderr.write("{0}:{1}:{2}: lexical error: multi-line comment is not terminated when end-of-file is reached\n".format(self.file_name, pos[0], pos[1]))
        t.type = "Lexicalerror"
        return t

    def t_COMMENT_error(self,t):
        r'.'
        print("ERROR:", t.value)
        return t
