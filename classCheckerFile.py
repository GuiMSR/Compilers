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
        self.methods = []
        self.fields = []
        self.classes = []
        self.current_class = ""
        self.current_method = ""
        self.class_dict = {}
        self.extends = {}
        self.methods_dict = {}
        self.fields_dict = {}
        self.formals = {}

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
                        sys.stderr.write("{0}:{1}:{2}: semantic error:  main method has to be of type int32".format(self.file_name, i[2], i[3]))
                        sys.exit(1)
                    elif len(self.formals[("Main", "main")]) > 0:
                        sys.stderr.write("{0}:{1}:{2}: semantic error:  main method should have no arguments".format(self.file_name, i[2], i[3]))
                        sys.exit(1)
                    return

            sys.stderr.write("{0}:{1}:{2}: semantic error: No main method in Main".format(self.file_name, self.class_dict["Main"][0], self.class_dict["Main"][1]))
            sys.exit(1)
        else:
            sys.stderr.write("{0}:1:1: semantic error: No class Main".format(self.file_name))
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
    
    def method_in_class(self, method_id, class_id):
        for method in self.methods_dict[class_id]:
            if method[0] == method_id:
                return (True, method)
        
        return (False,"nope")

    def check_overrides(self):
        for i in self.extends:
            for child_method in self.methods_dict[i]:
                methodInParent = self.method_in_class(child_method[0], self.extends[i])
                if methodInParent[0] :
                    # check methods return types
                    if child_method[1] != methodInParent[1][1]:
                        sys.stderr.write("{0}:{1}:{2}: semantic error: overrinding method {3} with different type".format(self.file_name, child_method[2], child_method[3], child_method[0]))
                        sys.exit(1)
                    
                    # check methods formals types and names
                    child_formals = self.formals[(i,child_method[0])]
                    parent_formals = self.formals[(self.extends[i], methodInParent[1][0])]
                    if len(child_formals) != len(parent_formals):
                        sys.stderr.write("{0}:{1}:{2}: semantic error: overrinding method {3} with different formal size".format(self.file_name, child_method[2], child_method[3], child_method[0]))
                        sys.exit(1)
                    for index in range(0,len(child_formals)):
                        # not same name
                        if child_formals[index][0] != parent_formals[index][0]:
                            sys.stderr.write("{0}:{1}:{2}: semantic error: overrinding method {3} with different name".format(self.file_name, child_method[2], child_method[3], child_method[0]))
                            sys.exit(1)
                        # not same type
                        elif child_formals[index][1] != parent_formals[index][1]:
                            sys.stderr.write("{0}:{1}:{2}: semantic error: overrinding method {3} with different type".format(self.file_name, child_method[2], child_method[3], child_method[0]))
                            sys.exit(1)
        return

    def check_extends_parents(self):
        for i in self.extends:
            try:
                self.class_dict[self.extends[i]]
            except:
                sys.stderr.write("{0}:{1}:{2}: semantic error: parent {3} doesn't exist".format(self.file_name, self.class_dict[i][0], self.class_dict[i][1], self.extends[i]))
                sys.exit(1)
        return 


    def p_init(self, p):
        'init : program'
        p[0] = (self.fields_dict, self.methods_dict, self.extends, self.formals)
        self.check_main_exists()
        self.check_extends_parents()
        self.check_cycles()
        self.check_overrides()

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
            self.extends.update({p[2]: p[4]})
        self.fields = []
        self.methods = []
        self.classes.append(p[0])
        self.current_class = ""

    def p_new_class_scope(self, p):
        "new_class_scope : TYPE_IDENTIFIER"
        p[0] = p[1]
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        if p[1] in self.class_dict:
            sys.stderr.write("{0}:{1}:{2}: semantic error: redefinition of class {3}, first defined at {4}:{5}".format(self.file_name, p.lineno(1) + 1, colno, p[1], self.class_dict[p[1]][0], self.class_dict[p[1]][1]))
            sys.exit(1)
        elif p[1] == "Object":
            sys.stderr.write("{0}:{1}:{2}: semantic error: redefinition of class {3}, class Object is already predefined".format(self.file_name, p.lineno(1) + 1, colno, p[1]))
            sys.exit(1)

        self.current_class = p[1]
        self.class_dict.update({p[1] : (p.lineno(1), colno)})
        self.methods_dict.update({p[1] : []})
        self.fields_dict.update({p[1] : []})


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
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        for i in self.fields_dict[self.current_class]:
            if i[0] == p[1]:
                colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
                sys.stderr.write("{0}:{1}:{2}: semantic error: redefinition of field {3}, first defined at {4}:{5}".format(self.file_name, p.lineno(1) + 1, colno, p[1], i[2], i[3]))
                sys.exit(1)
        fields_list = self.fields_dict[self.current_class]
        fields_list.append((p[1],p[3], p.lineno(1), colno))
        self.fields_dict.update({self.current_class: fields_list})
        # print("fields dict: " + str(self.fields_dict))


    def p_method(self, p):
        'method : new_method LPAR formals RPAR COLON type block'
        p[0] = "Method(" + p[1] + ", [" + p[3] + "], " + p[6] + ", " + p[7] + ")"
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        methods_list = self.methods_dict[self.current_class]
        methods_list.append((p[1],p[6], p.lineno(1), colno))
        self.methods_dict.update({self.current_class: methods_list})
        #print("methods dict: " + str(self.methods_dict))

    def p_new_method(self,p):
        'new_method : OBJECT_IDENTIFIER'
        p[0] = p[1]
        
        for i in self.methods_dict[self.current_class]:
            if i[0] == p[1]:
                colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
                sys.stderr.write("{0}:{1}:{2}: semantic error: redefinition of method {3}, first defined at {4}:{5}".format(self.file_name, p.lineno(1) + 1, colno, p[1], i[2], i[3]))
                sys.exit(1)
        self.current_method = p[1]
        self.formals.update({(self.current_class, p[1]) : []})
        #print(self.formals)

    def p_new_variables_scope(self, p):
        "new_variables_scope :"
        p[0] = ''

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
        colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
        for i in self.formals[(self.current_class, self.current_method)]:
            if i[0] == p[1]:
                sys.stderr.write("{0}:{1}:{2}: semantic error: {3} method has several formal arguments with the same name,\n redefinition of formal {4}, first defined at {5}:{6}".format(self.file_name, p.lineno(1) + 1, colno,self.current_method ,p[1], i[2], i[3]))
                sys.exit(1)
        formals_list = self.formals[(self.current_class, self.current_method)]
        formals_list.append((p[1],p[3], p.lineno(1), colno))
        self.formals.update({(self.current_class, self.current_method): formals_list})

    def p_block(self, p): 
        'block : LBRACE check_block new_variables_scope inblock RBRACE'
        result = "[" + p[4] + "]"
        p[0] = result.replace(';', ', ')

    def p_check_block(self, p):
        'check_block :'
        p[0] = ''
        

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
        if len(p) == 6:
            p[0] = "If(" + p[3] + ", " + p[5] + ")"
        else: 
            p[0] = "If(" + p[3] + ", " + p[5] + ", " + p[7] + ")"

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


    def p_assign(self, p):
        'expression : OBJECT_IDENTIFIER ASSIGN expression'
        p[0] = "Assign(" + p[1] + ", " + p[3] + ")"

    def p_unary_operators(self, p):
        '''expression : NOT expression check_bool
                    | MINUS expression check_int %prec UMINUS'''
        p[0] = "UnOp(" + p[1] + ", " + p[2] + ")"

    def p_check_int(self, p):
        "check_int :"
        p[0] = ''

    def p_check_bool(self, p):
        "check_bool :"
        p[0] = ''

    def p_unary_isnull(self, p):
        "expression : ISNULL expression"
        p[0] = "UnOp(" + p[1] + ", " + p[2] + ") : bool"

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
            p[0] = "Call("+ p[1] +  ", " + p[3] + ", [" + p[5] + "])"
  

    def p_new_type(self, p):
        'expression : NEW TYPE_IDENTIFIER'
        p[0] = "New(" + p[2] + ") : " + p[2]

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

    def p_literal_integer(self, p):
        "literal_integer : INTEGER_LITERAL"
        p[0] = p[1] + " : int32"

    def p_boolean_literal(self, p):
        '''boolean-literal : TRUE 
                        | FALSE'''
        p[0] = p[1] + " : bool"

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
