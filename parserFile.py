# -*- coding: utf-8 -*-
"""
Created on We Feb  24 18:41:25 2021

@author: Guilherme Madureira & Julien Carion
"""

import ply.yacc as yacc
from lexer import VsopLexer

class VsopParser():


    def __init__(self, lexer):
        self.parser = yacc.yacc(module=self)

    def __del__(self):
        pass

    tokens = VsopLexer.tokens

    # precedence = (
    # ('left','PLUS','MINUS'),
    # ('left','TIMES','DIV'),
    # )

    # def p_statement_expr(self, p):
    #     'statement : expression'
    #     print(p[1])


    # def p_binary_operators(self, p):
    #     '''expression : expression PLUS expression
    #               | expression MINUS expression
    #               | expression TIMES expression
    #               | expression DIV expression'''
        
    #     if p[2] == '+':
    #         p[0] = p[1] + p[3]
    #     elif p[2] == '-':
    #         p[0] = p[1] - p[3]
    #     elif p[2] == '*':
    #         p[0] = p[1] * p[3]
    #     elif p[2] == '/':
    #         p[0] = p[1] / p[3]

    # def p_expression_group(self, p):
    #     'expression : LPAREN expression RPAREN'
    #     p[0] = p[2]

    def p_expression_plus(self, p):
        'expression : expression PLUS term'
        p[0] = p[1] + p[3]
 
    def p_expression_minus(self, p):
        'expression : expression MINUS term'
        p[0] = p[1] - p[3]
    
    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]
    
    def p_term_times(self, p):
        'term : term TIMES factor'
        p[0] = p[1] * p[3]
    
    def p_term_div(self, p):
        'term : term DIV factor'
        p[0] = p[1] / p[3]
    
    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]
    
    def p_factor_num(self, p):
        'factor : INTEGER_LITERAL'
        p[0] = p[1]
    
    def p_factor_expr(self, p):
        'factor : LPAR expression RPAR'
        p[0] = p[2]

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!")