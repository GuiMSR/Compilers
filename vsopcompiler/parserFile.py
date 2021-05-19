# -*- coding: utf-8 -*-
"""
Created on We Feb  24 18:41:25 2021

@author: Guilherme Madureira & Julien Carion
"""

import ply.yacc as yacc
from lexer import VsopLexer
import re
import sys
import syntax_tree as st


class VsopParser():


    def __init__(self, lexer, file_name, string_text):
        self.parser = yacc.yacc(module=self, debug=False)
        self.file_name = file_name
        self.string_text = string_text
        self.methods = []
        self.fields = []
        self.classes = []
        self.args = []
        self.blocks = []
        self.formals = []
        self.current_class = ""

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

    def p_init(self, p):
        'init : program'
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("program", self.classes, [], pos)

    def p_program(self, p):
        '''program : program class
                    | class'''
        p[0] = None

    def p_field_method_error(self, p):
        '''class : field
                | method'''
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        lineno = p.lineno(1) + 1
        sys.stderr.write("{0}:{1}:{2}: syntax error: field or method outside of class".format(self.file_name, lineno, colno))
        sys.exit(1)

    def p_class_error(self, p):
        'class : CLASS error'
        sys.stderr.write("{0} is an invalid class identifier\n".format(str(p[2])))
        sys.exit(1)

    def p_general_class_error(self,p):
        '''class : expression
                | TYPE_IDENTIFIER
                | block'''
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        lineno = p.lineno(1) + 1
        sys.stderr.write("{0}:{1}:{2}: syntax error: expected class keyword".format(self.file_name, lineno, colno))
        sys.exit(1)

    def p_class(self, p):
        '''class : CLASS new_class_scope class-body
                | CLASS new_class_scope EXTENDS TYPE_IDENTIFIER class-body'''
        pos = self.find_position(p, 1)
        if len(p) == 4:
            p[0] = st.Tree_node("class", [st.Tree_node("fields", self.fields, [], pos, self.current_class), st.Tree_node("methods", self.methods, [], pos, self.current_class)], [p[2]], pos, self.current_class)
        else: 
            p[0] = st.Tree_node("class", [st.Tree_node("fields", self.fields, [], pos, self.current_class), st.Tree_node("methods", self.methods, [], pos, self.current_class)], [p[2], p[4]], pos, self.current_class)
        self.fields = []
        self.methods = []
        self.classes.append(p[0])
        self.current_class = ""

    def p_new_class_scope(self, p):
        "new_class_scope : TYPE_IDENTIFIER"
        p[0] = p[1]
        self.current_class = p[1]

    def p_class_body(self, p):
        'class-body : LBRACE class-body-in RBRACE'
        p[0] = None

    def p_class_braces_error(self, p):
        'class-body : LBRACE class-body-in error'
        sys.stderr.write("right brace is missing\n")
        sys.exit(1)

    def p_class_body_field(self, p):
        'class-body-in : class-body-in field'
        p[0] = None
        self.fields.append(p[2])
    
    def p_class_body_method(self, p):
        'class-body-in : class-body-in method'
        p[0] = None
        self.methods.append(p[2])

    def p_class_body_empty(self, p):
        'class-body-in : '
        p[0] = None

    def p_field(self, p):
        '''field : OBJECT_IDENTIFIER COLON type SEMICOLON
                | OBJECT_IDENTIFIER COLON type ASSIGN expression SEMICOLON'''
        pos = self.find_position(p, 1)
        if len(p) == 5:
            p[0] = st.Tree_node("field", [st.Tree_node("object identifier", [], [p[1]], pos, self.current_class, p[3])], [], pos, self.current_class, p[3])
        else:
            p[0] = st.Tree_node("field", [st.Tree_node("object identifier", [], [p[1]], pos, self.current_class, p[3]), p[5]], [], pos, self.current_class, p[3])


    def p_method(self, p):
        'method : method_identifier LPAR formals RPAR COLON type block'
        pos = self.find_position(p, 2)
        p[0] = st.Tree_node("method", [st.Tree_node("object identifier", [], [p[1]], pos, self.current_class, p[6]), st.Tree_node("formals", self.formals[-1], [], self.find_position(p, 4), self.current_class), p[7]], [], pos, self.current_class, p[6])
        del self.formals[-1]

    def p_method_identifier(self, p):
        'method_identifier : OBJECT_IDENTIFIER'
        p[0] = p[1]
        self.formals.append([])

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
            p[0] = None
            self.formals[-1].append(p[1])
        elif len(p) == 4:
            p[0] = None
            self.formals[-1].append(p[3])
        else:
            p[0] = None

    def p_formal(self, p):
        'formal : OBJECT_IDENTIFIER COLON type'
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("formal", [], [p[1]], pos, self.current_class, p[3])

    def p_block(self, p): 
        '''block : block_lbrace inblock RBRACE
                | block_lbrace RBRACE'''
        pos = self.find_position(p, 3)
        block_type = "unit"
        if self.blocks[-1]:
            block_type = self.blocks[-1][-1].type
        p[0] = st.Tree_node("block", self.blocks[-1], [], pos, self.current_class, block_type)
        del self.blocks[-1]

    def p_block_lbrace(self, p):
        'block_lbrace : LBRACE'
        p[0] = None
        self.blocks.append([])

    def p_block_inside(self, p):
        '''inblock : inblock SEMICOLON expression
                | expression'''
        if len(p) == 2:
            p[0] = None
            self.blocks[-1].append(p[1])
        elif len(p) == 4:
            p[0] = None
            self.blocks[-1].append(p[3])

    def p_block_error(self,p):
        '''inblock : inblock error '''
        sys.stderr.write("semicolon is missing after block element\n")
        sys.exit(1)

    def p_if(self, p):
        '''expression : IF expression THEN expression
                    | IF expression THEN expression ELSE expression'''
        pos = self.find_position(p, 1)
        ex_type1 = p[2].type
        ex_type2 = p[4].type
        if len(p) == 5:
            p[0] = st.Tree_node("if", [p[2], p[4]], [], pos, self.current_class, ex_type2)
        else: 
            ex_type3 = p[6].type
            if ex_type2 == ex_type3:
                p[0] = st.Tree_node("if", [p[2], p[4], p[6]], [], pos, self.current_class, ex_type2)
            else:
                p[0] = st.Tree_node("if", [p[2], p[4], p[6]], [], pos, self.current_class, "unit")

    def p_while(self, p):
        'expression : WHILE expression DO expression'
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("while", [p[2], p[4]], [], pos, self.current_class, "unit")

    def p_let(self, p):
        '''expression : LET OBJECT_IDENTIFIER COLON type IN expression
                    | LET OBJECT_IDENTIFIER COLON type ASSIGN expression IN expression'''
        pos = self.find_position(p, 1)
        if len(p) == 7:
            p[0] = st.Tree_node("let", [st.Tree_node("object identifier", [], [p[2]], self.find_position(p, 2), self.current_class, p[4]), p[6]], [], pos, self.current_class, p[6].type)
        else:
            p[0] = st.Tree_node("let", [st.Tree_node("object identifier", [], [p[2]], self.find_position(p, 2), self.current_class, p[4]), p[6], p[8]], [], pos, self.current_class, p[8].type)

    def p_assign(self, p):
        'expression : OBJECT_IDENTIFIER ASSIGN expression'
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("assign", [st.Tree_node("object identifier", [], [p[1]], pos, self.current_class), p[3]], [], pos, self.current_class, p[3].type)

    def p_unary_not(self, p):
        'expression : NOT expression'
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("unop", [p[2]], [p[1]], pos, self.current_class, "bool")

    def p_unary_minus(self, p):
        'expression : MINUS expression %prec UMINUS'
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("unop", [p[2]], [p[1]], pos, self.current_class, "int32")

    def p_unary_isnull(self, p):
        "expression : ISNULL expression"
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("unop", [p[2]], [p[1]], pos, self.current_class, "bool")

    def p_binary_equal(self, p):
        'expression : expression EQUAL expression'
        pos = self.find_position(p, 2)
        p[0] = st.Tree_node("binop", [p[1], p[3]], [p[2]], pos, self.current_class, "bool")


    def p_binary_and(self, p):
        'expression : expression AND expression'
        pos = self.find_position(p, 2)
        p[0] = st.Tree_node("binop", [p[1], p[3]], [p[2]], pos, self.current_class, "bool")

    def p_binary_int_operators(self, p):
        '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIV expression
                  | expression POW expression'''
        pos = self.find_position(p, 2)
        p[0] = st.Tree_node("binop", [p[1], p[3]], [p[2]], pos, self.current_class, "int32")

    def p_binary_comp_operators(self, p):
        '''expression : expression LOWER_EQUAL expression
                    | expression LOWER expression'''
        pos = self.find_position(p, 2)
        p[0] = st.Tree_node("binop", [p[1], p[3]], [p[2]], pos, self.current_class, "bool")  


    def p_object_call(self, p):
        '''expression : call_identifier LPAR args RPAR
                    | expression DOT call_identifier LPAR args RPAR'''
        pos = self.find_position(p, 2)
        if len(p) == 5:
            p[0] = st.Tree_node("call", [st.Tree_node("self", [], ["self"], pos, self.current_class, self.current_class), st.Tree_node("object identifier", [], [p[1]], pos, self.current_class), st.Tree_node("args", self.args[-1], [], self.find_position(p, 4), self.current_class)], [], pos, self.current_class)
        else: 
            p[0] = st.Tree_node("call", [p[1], st.Tree_node("object identifier", [], [p[3]], self.find_position(p, 4), self.current_class), st.Tree_node("args", self.args[-1], [], self.find_position(p, 6), self.current_class)], [], pos, self.current_class) 
        del self.args[-1]

    def p_call_identifier(self, p):
        'call_identifier : OBJECT_IDENTIFIER'
        p[0] = p[1]
        self.args.append([]) 

    def p_new_type(self, p):
        'expression : NEW TYPE_IDENTIFIER'
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("new type", [], [p[2]], pos, self.current_class, p[2])

    def p_expression_object(self, p):
        'expression : OBJECT_IDENTIFIER'
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("object identifier", [], [p[1]], pos, self.current_class)

    def p_expression_self(self, p):
        'expression : SELF'
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("self", [], [p[1]], pos, self.current_class, self.current_class)

    def p_expression_literal(self, p):
        'expression : literal'
        p[0] = p[1]

    def p_par_alone(self,p):
        'expression : LPAR RPAR'
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("par alone", [], ["()"], pos, self.current_class, "unit")

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
        '''expression : error'''
        sys.stderr.write("invalid expression: {0}\n".format(str(p[1])))
        sys.exit(1)
    
    def p_args(self, p):
        '''args : args COMMA expression
                | expression
                |'''
        if len(p) == 4:
            p[0] = None
            self.args[-1].append(p[3])
        elif len(p) == 2:
            p[0] = None
            self.args[-1].append(p[1])
        else:
            p[0] = None

    def p_string_literal(self, p):
        '''literal : string_literal'''
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("string literal", [], [p[1]], pos, self.current_class, "string")
    
    def p_integer_literal(self, p):
        '''literal : INTEGER_LITERAL'''
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("integer literal", [], [p[1]], pos, self.current_class, "int32")

    def p_boolean_literal(self, p):
        '''literal : TRUE 
                    | FALSE'''
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("boolean literal", [], [p[1]], pos, self.current_class, "bool")

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


    # Returns tuple with line and column positions 
    def find_position(self, p, i):
        colno = p.lexpos(i) - self.string_text.rfind('\n', 0, p.lexpos(i))
        lineno = 1 if p.lineno(i) == 0 else p.lineno(i)
        return (lineno, colno)
