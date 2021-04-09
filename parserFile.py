# -*- coding: utf-8 -*-
"""
Created on We Feb  24 18:41:25 2021

@author: Guilherme Madureira & Julien Carion
"""

import ply.yacc as yacc
from lexer import VsopLexer
import re
import sys


class VsopParser():


    def __init__(self, lexer, file_name, string_text):
        self.parser = yacc.yacc(module=self)
        self.file_name = file_name
        self.string_text = string_text
        self.methods = []
        self.fields = []
        self.classes = []
        self.variables_list = []
        self.current_class = ""
        self.expressions_stack = []

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
        'LOWER'
   	   ]

    precedence = (
    ('right','ASSIGN'),
    ('left', 'AND'),
    ('right','NOT'),
    ('nonassoc', 'LOWER', 'EQUAL', 'LOWER_EQUAL'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIV'),
    ('right','ISNULL','UMINUS'),
    ('right','POW'),
    ('left', 'DOT'),
    )

    start = 'init'

    def add_variable(self, identifier, type_id):
        self.variables_list[-1].update({identifier: type_id})

    def search_type(self, identifier):
        for d in self.variables_list:
            if(d.get(identifier) != None):
                return d[identifier]
        return None

    def p_init(self, p):
        'init : program'
        p[0] = str(self.classes).replace("'", '').replace('\\\\','\\')

    def p_program(self, p):
        '''program : program class
                    | class'''
        if len(p) == 3:
            p[0] = str(str(p[1]) + str(p[2]))
        else:
            p[0] = str(str(p[1]))

    def p_field_method_error(self, p):
        '''class : field
                | method'''
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        sys.stderr.write("{0}:{1}:{2}: syntax error: field or method outside of class".format(self.file_name, p.lineno(1) + 1, colno))
        sys.exit(1)

    def p_class_error(self, p):
        'class : CLASS error'
        sys.stderr.write("{0} is an invalid class identifier\n".format(str(p[2].value)))
        sys.exit(1)

    def p_general_class_error(self,p):
        '''class : expression
                | TYPE_IDENTIFIER
                | block'''
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        sys.stderr.write("{0}:{1}:{2}: syntax error: expected class keyword".format(self.file_name, p.lineno(1) + 1, colno))
        sys.exit(1)

    def p_class(self, p):
        '''class : CLASS new_class_scope class-body
                | CLASS new_class_scope EXTENDS TYPE_IDENTIFIER class-body'''
        if len(p) == 4:
            p[0] = "Class(" + p[2] + ", Object, " + str(self.fields).replace("'", '').replace('\\\\','\\') + ", " + str(self.methods).replace("'", '').replace('\\\\','\\') + ")"
        else: 
            p[0] = "Class(" + p[2] + ", " + p[4] + ", " + str(self.fields).replace("'", '').replace('\\\\','\\') + ", " + str(self.methods).replace("'", '').replace('\\\\','\\') + ")"
        self.fields = []
        self.methods = []
        self.classes.append(p[0])
        self.current_class = ""
        self.variables_list.pop()

    def p_new_class_scope(self, p):
        "new_class_scope : TYPE_IDENTIFIER"
        p[0] = p[1]
        s = { }
        self.variables_list.append(s)
        self.current_class = p[1]


    def p_class_body(self, p):
        'class-body : LBRACE class-body-in RBRACE'
        p[0] = p[1] + p[2] + p[3]

    def p_class_braces_error(self, p):
        'class-body : LBRACE class-body-in error'
        sys.stderr.write("right brace is missing\n")
        sys.exit(1)

    def p_class_body_field(self, p):
        'class-body-in : class-body-in field'
        p[0] = p[1] + p[2]
        self.fields.append(p[2])
    
    def p_class_body_method(self, p):
        'class-body-in : class-body-in method'
        p[0] = p[1] + p[2]
        self.methods.append(p[2])

    def p_class_body_empty(self, p):
        'class-body-in : '
        p[0] = ''

    def p_field(self, p):
        '''field : OBJECT_IDENTIFIER COLON type SEMICOLON
                | OBJECT_IDENTIFIER COLON type ASSIGN expression SEMICOLON'''
        if len(p) == 5:
            p[0] = "Field(" + p[1] + ", " + p[3] + ")"
        else:
            p[0] = "Field(" + p[1] + ", " + p[3] + ", " + p[5] +")"
        self.add_variable(p[1], p[3])


    def p_method(self, p):
        'method : OBJECT_IDENTIFIER new_variables_scope LPAR formals RPAR COLON type block'
        p[0] = "Method(" + p[1] + ", [" + p[4] + "], " + p[7] + ", " + p[8] + ")"
        self.variables_list.pop()

    def p_new_variables_scope(self, p):
        "new_variables_scope :"
        p[0] = ''
        s = { }
        self.variables_list.append(s)

    def p_type(self, p):
        '''type : TYPE_IDENTIFIER
                | INT32
                | BOOL
                | STRING
                | UNIT '''
        p[0] = p[1]

    def p_formals(self, p):
        '''formals : formal
                | formals COMMA formal
                | '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[1] + ", " + p[3]
        else:
            p[0] = ''

    def p_formal(self, p):
        'formal : OBJECT_IDENTIFIER COLON type'
        p[0] = p[1] + " " + p[2] + " " + p[3]
        self.add_variable(p[1], p[3])

    def p_block(self, p): 
        'block : LBRACE new_variables_scope inblock RBRACE'
        result = "[" + p[3] + "]"
        p[0] = result.replace(';', ', ')
        self.variables_list.pop()

    def p_block_inside(self, p):
        '''inblock : inblock SEMICOLON expression
                | expression
                |'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[1] + p[2] + p[3]
        else:
            p[0] = ''

    def p_block_error(self,p):
        '''inblock : inblock error '''
        sys.stderr.write("semicolon is missing after {0}\n".format(str(p[1])))
        sys.exit(1)

    def p_if(self, p):
        '''expression : new_variables_scope IF expression THEN expression
                    | new_variables_scope IF expression THEN expression ELSE expression'''
        if len(p) == 5:
            p[0] = "If(" + p[2] + ", " + p[4] + ")"
        else: 
            p[0] = "If(" + p[2] + ", " + p[4] + ", " + p[6] + ")"

    def p_while(self, p):
        'expression : WHILE expression DO expression'
        p[0] = "While(" + p[2] + ", " + p[4] + ")"

    def p_let(self, p):
        '''expression : LET let_type IN expression
                    | LET let_type ASSIGN expression IN expression'''
        if len(p) == 5:
            p[0] = "Let(" + p[2] + ", " + p[4] + ")"
        else:
            p[0] = "Let(" + p[2] + ", " + p[4] + ", " + p[6] +")"

    def p_let_type(self, p):
        "let_type : OBJECT_IDENTIFIER COLON type"
        p[0] = p[1] + ", " + p[3] 
        self.add_variable(p[1], p[3])


    def p_assign(self, p):
        'expression : OBJECT_IDENTIFIER ASSIGN get_type expression'
        p[0] = "Assign(" + p[1] + ", " + p[4] + ")"
        self.add_variable(p[1], self.expressions_stack.pop())

    def p_get_type(self, p):
        "get_type :"
        self.expressions_stack.append("")

    def p_unary_operators(self, p):
        '''expression : NOT expression
                    | MINUS expression %prec UMINUS
                    | ISNULL expression'''
        p[0] = "UnOp(" + p[1] + ", " + p[2] + ")"

    def p_binary_operators(self, p):
        '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIV expression
                  | expression EQUAL expression
                  | expression LOWER_EQUAL expression
                  | expression LOWER expression
                  | expression POW expression
                  | expression AND expression'''
        p[0] = "BinOp("+ p[2] +", " + p[1] + ", " + p[3] +")"


    def p_object_call(self, p):
        '''expression : OBJECT_IDENTIFIER LPAR args RPAR
                    | expression DOT OBJECT_IDENTIFIER LPAR args RPAR'''
        if len(p) == 5:
            p[0] = "Call(self : " + self.current_class + ", " + p[1] + ", [" + p[3] + "])"
        else: 
            p[0] = "Call("+ p[1] + ", " + p[3] + ", [" + p[5] + "])"    

    def p_new_type(self, p):
        'expression : NEW TYPE_IDENTIFIER'
        p[0] = "New(" + p[2] + ") : " + p[2]

    def p_expression_object(self, p):
        'expression : OBJECT_IDENTIFIER'
        print(self.variables_list)
        t = self.search_type(p[1])
        print(p[1])
        print(t)
        if t is None:
            colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
            sys.stderr.write("{0}:{1}:{2}: semantic error: an identifier is used that is not defined in the scope".format(self.file_name, p.lineno(1) + 1, colno))
            sys.exit(1)
        p[0] = p[1] + " : " + t
        if len(self.expressions_stack) > 0:
            self.expressions_stack[-1] = t

    def p_expression_self(self, p):
        'expression : SELF'
        p[0] = p[1]

    def p_expression_literal(self, p):
        'expression : literal'
        p[0] = p[1]

    def p_par_alone(self,p):
        'expression : LPAR RPAR'
        p[0] = ("()")

    def p_par_expression(self, p): 
        'expression : LPAR expression RPAR'
        p[0] = p[2]

    def p_par_error(self,p):
        '''expression : LPAR expression error
                    | error expression RPAR'''
        sys.stderr.write("missing parenthesis \n")
        sys.exit(1)

    def p_expression_block(self, p):
        'expression : block'
        p[0] = p[1]

    def p_expression_error(self, p):
        '''expression : error
                    | IF expression THEN expression SEMICOLON error'''
        if(len(p) > 2 and p[6].type == 'ELSE'):
            sys.stderr.write("bad syntax for if statement: unneeded semicolon\n")
        else:
            sys.stderr.write("invalid expression: {0}\n".format(str(p[1].value)))
        sys.exit(1)
    
    def p_args(self, p):
        '''args : args COMMA expression
                | expression
                |'''
        if len(p) == 4:
            p[0] = p[1] + p[2] + " " + p[3]
        elif len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ''

    def p_literal(self, p):
        '''literal : literal_integer
                | literal_string
                | boolean-literal'''
        p[0] = p[1]

    def p_literal_string(self, p):
        "literal_string : string_literal"
        p[0] = p[1] + " : string"
        if len(self.expressions_stack) > 0:
            self.expressions_stack[-1] = "string"

    def p_literal_integer(self, p):
        "literal_integer : INTEGER_LITERAL"
        p[0] = p[1] + " : int32"
        if len(self.expressions_stack) > 0:
            self.expressions_stack[-1] = "int32"

    def p_boolean_literal(self, p):
        '''boolean-literal : TRUE 
                        | FALSE'''
        p[0] = p[1] + " : bool"
        if len(self.expressions_stack) > 0:
            self.expressions_stack[-1] = "bool"

    # Find column number at the begin of a token
    def find_column(self, input, token):
	     line_start = input.rfind('\n', 0, token.lexpos) + 1
	     return (token.lexpos - line_start) + 1

    # Error rule for syntax errors
    def p_error(self, p):
        if not p:
            nlines = len(self.string_text.split('\n'))
            try:
                lastline = self.string_text.splitlines()[nlines-1]
            except:
                lastline = [1]
            colno = len(lastline)
            sys.stderr.write("{0}:{1}:{2}: syntax error: end of file reached without closing braces".format(self.file_name, nlines, colno))
            sys.exit(1)
        else:
            colno = self.find_column(self.string_text, p)
            nlines = len(self.string_text.split('\n')) - 1
            sys.stderr.write("{0}:{1}:{2}: syntax error: ".format(self.file_name, p.lineno - nlines, colno))
