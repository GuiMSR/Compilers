# -*- coding: utf-8 -*-
"""
Created on We Feb  24 18:41:25 2021

@author: Guilherme Madureira & Julien Carion
"""

import ply.yacc as yacc
from lexer import VsopLexer
import re


class VsopParser():


    def __init__(self, lexer):
        self.parser = yacc.yacc(module=self)
        self.methods = []
        self.fields = []

    def __del__(self):
        pass

    tokens = VsopLexer.tokens

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

    start = 'program'

    def p_program(self, p):
        '''program : class program
                    | class'''
        if len(p) == 3:
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1]

    def p_class(self, p):
        '''class : CLASS TYPE_IDENTIFIER class-body
                | CLASS TYPE_IDENTIFIER EXTENDS TYPE_IDENTIFIER class-body'''
        if len(p) == 4:
            p[0] = "Class(" + p[2] + ", Object, " + str(self.fields).replace("'", '') + ", " + str(self.methods).replace("'", '') + ")"
        else: 
            p[0] = "Class(" + p[2] + ", " + p[4] + str(self.fields).replace("'", '') + ", " + str(self.methods).replace("'", '') + ")"
        self.fields = []
        self.methods = []


    def p_class_body(self, p):
        'class-body : LBRACE class-body-in RBRACE'
        p[0] = p[1] + p[2] + p[3]

    def p_class_body_field(self, p):
        'class-body-in : field class-body-in'
        p[0] = p[1] + p[2]
        self.fields.insert(0, p[0])
    
    def p_class_body_method(self, p):
        'class-body-in : method class-body-in'
        p[0] = p[1] + p[2]
        self.methods.insert(0, p[0])

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


    def p_method(self, p):
        'method : OBJECT_IDENTIFIER LPAR formals RPAR COLON type block'
        p[0] = "Method(" + p[1] + ", " + p[3] + ", " + p[6] + ", " + p[7] + ")"

    def p_type(self, p):
        '''type : TYPE_IDENTIFIER
                | INT32
                | BOOL
                | STRING
                | UNIT '''
        p[0] = p[1]

    def p_formals(self, p):
        '''formals : formal
                | formal COMMA formals
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

    def p_block(self, p): 
        'block : LBRACE inblock RBRACE'
        if ';' in p[2]:
            result = "[" + p[2] + "]"
        else:
            result = p[2]
        p[0] = result.replace(';', ', ')

    def p_block_inside(self, p):
        '''inblock : inblock SEMICOLON expression
                | expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2] + p[3]

    def p_if(self, p):
        '''expression : IF expression THEN expression
                    | IF expression THEN expression ELSE expression'''
        if len(p) == 5:
            p[0] = "If(" + p[2] + ", " + p[4] + ")"
        else: 
            p[0] = "If(" + p[2] + ", " + p[4] + ", " + p[6] + ")"

    def p_while(self, p):
        'expression : WHILE expression DO expression'
        p[0] = "While(" + p[2] + ", " + p[4] + ")"

    def p_let(self, p):
        '''expression : LET OBJECT_IDENTIFIER COLON type IN expression
                    | LET OBJECT_IDENTIFIER COLON type ASSIGN expression IN expression'''
        if len(p) == 7:
            p[0] = "Let(" + p[2] + ", " + p[4] + ", " + p[6] + ")"
        else:
            p[0] = "Let(" + p[2] + ", " + p[4] + ", " + p[6] + ", " + p[8] +")"

    def p_assign(self, p):
        'expression : OBJECT_IDENTIFIER ASSIGN expression'
        p[0] = "Assign(" + p[1] + ", " + p[3] + ")"

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
            p[0] = "Call(self, " + p[1] + ", [" + p[3] + "])"
        else: 
            p[0] = "Call("+ p[1] + ", " + p[3] + ", [" + p[5] + "])"

    def p_new_type(self, p):
        'expression : NEW TYPE_IDENTIFIER'
        p[0] = "New(" + p[2] + ")"

    def p_expression_object(self, p):
        'expression : OBJECT_IDENTIFIER'
        p[0] = p[1]

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

    def p_expression_block(self, p):
        'expression : block'
        p[0] = p[1]
    
    def p_args(self, p):
        '''args : expression COMMA args
                | expression
                |'''
        if len(p) == 4:
            p[0] = p[1] + p[2] + p[3]
        elif len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ''

    def p_literal(self, p):
        '''literal : INTEGER_LITERAL
                | string_literal
                | boolean-literal'''
        p[0] = p[1]

    def p_boolean_literal(self, p):
        '''boolean-literal : TRUE 
                        | FALSE'''
        p[0] = p[1]



    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error at '%s'" % p.value)