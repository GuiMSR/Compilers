# -*- coding: utf-8 -*-
"""
Created on We Feb  24 18:41:25 2021

@author: Guilherme Madureira & Julien Carion
"""

import ply.yacc as yacc
from lexer import *

class VsopParser():


    def __init__(self, lexer):
        self.parser = yacc.yacc(module=self)
        self.lexer = lexer

    def __del__(self):
        pass

    tokens = VsopLexer.tokens


    def p_binary_operators(p):
        '''expression : expression PLUS term
                  | expression MINUS term
        term       : term TIMES factor
                  | term DIVIDE factor'''
        
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]

    def p_expression_term(p):
        'expression : term'
        p[0] = p[1]

    def p_term_factor(p):
        'term : factor'
        p[0] = p[1]

    def p_factor_num(p):
        'factor : NUMBER'
        p[0] = p[1]

    def p_factor_expr(p):
        'factor : LPAR expression RPAR'
        p[0] = p[2]

    # Error rule for syntax errors
    def p_error(p):
        print("Syntax error in input!")