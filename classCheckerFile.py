# -*- coding: utf-8 -*-
"""
Created on We Feb  24 18:41:25 2021

@author: Guilherme Madureira & Julien Carion
"""

import ply.yacc as yacc
from lexer import VsopLexer
import re
import sys


class ClassChecker():


    def __init__(self, lexer, file_name, string_text):
        self.parser = yacc.yacc(module=self, debug=False)
        self.file_name = file_name
        self.string_text = string_text
        self.classes = []
        self.current_class = ""
        self.current_method = ""
        self.class_dict = {"Object": (1,1)}
        self.extends = {}
        self.methods_dict = {"Object": [('print', 'Object', 1,1), ('printBool', 'Object', 1,1), ('printInt32', 'Object', 1,1), ('inputLine', 'string', 1,1), ('inputBool', 'bool', 1,1), ('inputInt32', 'int32', 1,1)]}
        self.fields_dict = {"Object": []}
        self.formals = {('Object', 'print'): [('s', 'string', 1 ,1)], ('Object', 'printBool'): [('b', 'bool', 1 ,1)], ('Object', 'printInt32'): [('i', 'int32', 1 ,1)], ('Object', 'inputLine'): [], ('Object', 'inputBool'): [], ('Object', 'inputInt32'): []}

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

    
    def search_type_in_methods(self, identifier):
        for tuple in self.methods_dict[self.current_class]:
            if tuple[0] == identifier:
                return tuple[1]     
        return None

    def search_type_in_fields(self, identifier):
        for tuple in self.fields_dict[self.current_class]:
            if tuple[0] == identifier:
                return tuple[1]     
        return None

    def check_main_exists(self):
        if "Main" in self.class_dict:
            for i in self.methods_dict["Main"]:
                if i[0] == "main":
                    if i[1] != "int32":
                        sys.stderr.write("{0}:{1}:{2}: semantic error:  main method has to be of type int32\n".format(self.file_name, i[2], i[3]))
                        sys.exit(1)
                    elif len(self.formals[("Main", "main")]) > 0:
                        sys.stderr.write("{0}:{1}:{2}: semantic error:  main method should have no arguments\n".format(self.file_name, i[2], i[3]))
                        sys.exit(1)
                    return

            sys.stderr.write("{0}:{1}:{2}: semantic error: No main method in Main\n".format(self.file_name, self.class_dict["Main"][0], self.class_dict["Main"][1]))
            sys.exit(1)
        else:
            sys.stderr.write("{0}:1:1: semantic error: No class Main\n".format(self.file_name))
            sys.exit(1) 

    def check_cycles(self):
        error = False
        for i in self.extends:
            t = i
            try:
                while(self.extends[t]):
                    t = self.extends[t]
                    if t == i:
                        error = True
                        sys.stderr.write("{0}:{1}:{2}: semantic error: class {3} cannot extend child class {4}.\n".format(self.file_name, self.class_dict[i][0], self.class_dict[i][1], i, self.extends[i]))
                        break
            except: 

                pass
        if error:
            sys.exit(1)
        return 

    def compute_line(self, p, index):
        return p.lineno(index)
    
    def method_in_class(self, method_id, class_id):
        for method in self.methods_dict[class_id]:
            if method[0] == method_id:
                return (True, method)
        
        return (False,"nope")
    
    def field_in_class(self, field_id, class_id):
        for field in self.fields_dict[class_id]:
            if field[0] == field_id:
                return (True, field)
        
        return (False,"nope")

    def check_overrides(self):
        for i in self.extends:
            for child_field in self.fields_dict[i]:
                t = i
                while(self.extends.get(t) != None):
                    fieldInParent = self.field_in_class(child_field[0], self.extends[t])
                    if fieldInParent[0]:
                        sys.stderr.write("{0}:{1}:{2}: semantic error: redefinition of field {3} (first defined at {4}:{5} in parent class {6}).\n".format(self.file_name, child_field[2], child_field[3], child_field[0], fieldInParent[1][2], fieldInParent[1][3], self.extends[t]))
                        sys.exit(1)
                    t = self.extends[t]

            for child_method in self.methods_dict[i]:
                t = i
                while(self.extends.get(t) != None):
                    methodInParent = self.method_in_class(child_method[0], self.extends[t])
                    if methodInParent[0] :
                        # check methods return types
                        if child_method[1] != methodInParent[1][1]:
                            sys.stderr.write("{0}:{1}:{2}: semantic error: overrinding method {3} with different type (first defined at {4}:{5} in parent class {6}).\n".format(self.file_name, child_method[2], child_method[3], child_method[0], methodInParent[1][2], methodInParent[1][3], self.extends[t]))
                            sys.exit(1)
                        
                        # check methods formals types and names
                        child_formals = self.formals[(i,child_method[0])]
                        parent_formals = self.formals[(self.extends[t], methodInParent[1][0])]
                        if len(child_formals) != len(parent_formals):
                            sys.stderr.write("{0}:{1}:{2}: semantic error: overrinding method {3} with different formal size (first defined at {4}:{5} in parent class {6}).\n".format(self.file_name, child_method[2], child_method[3], child_method[0], methodInParent[1][2], methodInParent[1][3], self.extends[t]))
                            sys.exit(1)
                        for index in range(0,len(child_formals)):
                            # not same name
                            if child_formals[index][0] != parent_formals[index][0]:
                                sys.stderr.write("{0}:{1}:{2}: semantic error: overrinding method {3} with different name (first defined at {4}:{5} in parent class {6}).\n".format(self.file_name, child_method[2], child_method[3], child_method[0], methodInParent[1][2], methodInParent[1][3], self.extends[t]))
                                sys.exit(1)
                            # not same type
                            elif child_formals[index][1] != parent_formals[index][1]:
                                sys.stderr.write("{0}:{1}:{2}: semantic error: overrinding method {3} with different typ (first defined at {4}:{5} in parent class {6}).\n".format(self.file_name, child_method[2], child_method[3], child_method[0], methodInParent[1][2], methodInParent[1][3], self.extends[t]))
                                sys.exit(1)
                    t = self.extends[t]
        return

    def check_extends_parents(self):
        for i in self.extends:
            try:
                self.class_dict[self.extends[i]]
            except:
                sys.stderr.write("{0}:{1}:{2}: semantic error: parent {3} doesn't exist\n".format(self.file_name, self.class_dict[i][0], self.class_dict[i][1], self.extends[i]))
                sys.exit(1)
        return 
    
    def check_fields_types(self):
        for i in self.class_dict:
            for field in self.fields_dict[i]:
                if field[1] not in self.class_dict:
                    if field[1] != "int32" and field[1] != "bool" and field[1] != "string" and field[1] != "unit":
                        sys.stderr.write("{0}:{1}:{2}: semantic error: use of undefined type {3}\n".format(self.file_name, field[2], field[3], field[1]))
                        sys.exit(1)



    def p_init(self, p):
        'init : program'
        p[0] = (self.fields_dict, self.methods_dict, self.extends, self.formals, self.class_dict)
        self.check_main_exists()
        self.check_extends_parents()
        self.check_cycles()
        self.check_overrides()
        self.check_fields_types()

    def p_program(self, p):
        '''program : program class
                    | class'''

    def p_field_method_error(self, p):
        '''class : field
                | method'''
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        sys.stderr.write("{0}:{1}:{2}: syntax error: field or method outside of class\n".format(self.file_name, self.compute_line(p, 1), colno))
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
        sys.stderr.write("{0}:{1}:{2}: syntax error: expected class keyword\n".format(self.file_name, self.compute_line(p, 1), colno))
        sys.exit(1)

    def p_class(self, p):
        '''class : CLASS new_class_scope class-body
                | CLASS new_class_scope EXTENDS TYPE_IDENTIFIER class-body'''
        if len(p) == 4:
            self.extends.update({p[2]: "Object"})
        else: 
            self.extends.update({p[2]: p[4]})
        self.classes.append(p[0])
        self.current_class = ""

    def p_new_class_scope(self, p):
        "new_class_scope : TYPE_IDENTIFIER"
        p[0] = p[1]
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        if p[1] in self.class_dict:
            sys.stderr.write("{0}:{1}:{2}: semantic error: redefinition of class {3}, first defined at {4}:{5}\n".format(self.file_name, self.compute_line(p, 1), colno, p[1], self.class_dict[p[1]][0], self.class_dict[p[1]][1]))
            sys.exit(1)
        elif p[1] == "Object":
            sys.stderr.write("{0}:{1}:{2}: semantic error: redefinition of class {3}, class Object is already predefined\n".format(self.file_name, self.compute_line(p, 1), colno, p[1]))
            sys.exit(1)

        self.current_class = p[1]
        self.class_dict.update({p[1] : (self.compute_line(p, 1), colno)})
        self.methods_dict.update({p[1] : []})
        self.fields_dict.update({p[1] : []})


    def p_class_body(self, p):
        'class-body : LBRACE class-body-in RBRACE'

    def p_class_braces_error(self, p):
        'class-body : LBRACE class-body-in error'
        sys.stderr.write("right brace is missing\n")
        sys.exit(1)

    def p_class_body_field(self, p):
        'class-body-in : class-body-in field'
    
    def p_class_body_method(self, p):
        'class-body-in : class-body-in method'
        

    def p_class_body_empty(self, p):
        'class-body-in : '

    def p_field(self, p):
        '''field : OBJECT_IDENTIFIER COLON type SEMICOLON
                | OBJECT_IDENTIFIER COLON type ASSIGN expression SEMICOLON'''
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        for i in self.fields_dict[self.current_class]:
            if i[0] == p[1]:
                colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
                sys.stderr.write("{0}:{1}:{2}: semantic error: redefinition of field {3}, first defined at {4}:{5}\n".format(self.file_name, self.compute_line(p, 1), colno, p[1], i[2], i[3]))
                sys.exit(1)
        fields_list = self.fields_dict[self.current_class]
        fields_list.append((p[1],p[3], self.compute_line(p, 1), colno))
        self.fields_dict.update({self.current_class: fields_list})


    def p_method(self, p):
        'method : new_method LPAR formals RPAR COLON type block'
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        methods_list = self.methods_dict[self.current_class]
        methods_list.append((p[1],p[6], self.compute_line(p, 2), colno))
        self.methods_dict.update({self.current_class: methods_list})

    def p_new_method(self,p):
        'new_method : OBJECT_IDENTIFIER'
        p[0] = p[1]
        
        for i in self.methods_dict[self.current_class]:
            if i[0] == p[1]:
                colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
                sys.stderr.write("{0}:{1}:{2}: semantic error: redefinition of method {3}, first defined at {4}:{5}\n".format(self.file_name, self.compute_line(p, 1), colno, p[1], i[2], i[3]))
                sys.exit(1)
        self.current_method = p[1]
        self.formals.update({(self.current_class, p[1]) : []})

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

    def p_formal(self, p):
        'formal : OBJECT_IDENTIFIER COLON type'
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        for i in self.formals[(self.current_class, self.current_method)]:
            if i[0] == p[1]:
                sys.stderr.write("{0}:{1}:{2}: semantic error: {3} method has several formal arguments with the same name,\n redefinition of formal {4}, first defined at {5}:{6}\n".format(self.file_name, self.compute_line(p, 1), colno,self.current_method ,p[1], i[2], i[3]))
                sys.exit(1)
        formals_list = self.formals[(self.current_class, self.current_method)]
        formals_list.append((p[1],p[3], self.compute_line(p, 1), colno))
        self.formals.update({(self.current_class, self.current_method): formals_list})

    def p_block(self, p): 
        '''block : LBRACE inblock RBRACE
                | LBRACE RBRACE'''
        
    def p_block_inside(self, p):
        '''inblock : inblock SEMICOLON expression
                | expression'''

    def p_if(self, p):
        '''expression : IF expression THEN expression
                    | IF expression THEN expression ELSE expression'''

    def p_while(self, p):
        'expression : WHILE expression DO expression'

    def p_let(self, p):
        '''expression : LET let_type IN expression
                    | LET let_type ASSIGN expression IN expression'''

    def p_let_type(self, p):
        "let_type : OBJECT_IDENTIFIER COLON type"


    def p_assign(self, p):
        'expression : OBJECT_IDENTIFIER ASSIGN expression'

    def p_unary_operators(self, p):
        '''expression : NOT expression
                    | MINUS expression %prec UMINUS'''


    def p_unary_isnull(self, p):
        "expression : ISNULL expression"

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

    def p_object_call(self, p):
        '''expression : OBJECT_IDENTIFIER LPAR args RPAR
                    | expression DOT OBJECT_IDENTIFIER LPAR args RPAR'''

    def p_new_type(self, p):
        'expression : NEW TYPE_IDENTIFIER'

    def p_expression_object(self, p):
        'expression : OBJECT_IDENTIFIER'

    def p_expression_self(self, p):
        'expression : SELF'

    def p_expression_literal(self, p):
        'expression : literal'

    def p_par_alone(self,p):
        'expression : LPAR RPAR'

    def p_par_expression(self, p): 
        'expression : LPAR expression RPAR'

    def p_par_error(self,p):
        '''expression : LPAR expression error
                    | error expression RPAR'''
        sys.stderr.write("missing parenthesis \n")
        sys.exit(1)

    def p_expression_block(self, p):
        'expression : block'

    def p_expression_error(self, p):
        '''expression : error'''
        sys.stderr.write("invalid expression: {0}\n".format(str(p[1].value)))
        sys.exit(1)
    
    def p_args(self, p):
        '''args : args COMMA expression
                | expression
                |'''

    def p_literal(self, p):
        '''literal : literal_integer
                | literal_string
                | boolean-literal'''

    def p_literal_string(self, p):
        "literal_string : string_literal"

    def p_literal_integer(self, p):
        "literal_integer : INTEGER_LITERAL"

    def p_boolean_literal(self, p):
        '''boolean-literal : TRUE 
                        | FALSE'''

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
            sys.stderr.write("{0}:{1}:{2}: syntax error: end of file reached without closing braces\n".format(self.file_name, nlines, colno))
            sys.exit(1)
        else:
            colno = self.find_column(self.string_text, p)
            nlines = len(self.string_text.split('\n')) - 1
            sys.stderr.write("{0}:{1}:{2}: syntax error: ".format(self.file_name, p.lineno - nlines, colno))
