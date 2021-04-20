# -*- coding: utf-8 -*-
"""
Created on We Feb  24 18:41:25 2021

@author: Guilherme Madureira & Julien Carion
"""

import ply.yacc as yacc
from lexer import VsopLexer
import re
import sys


class VsopParser2():


    def __init__(self, lexer, file_name, string_text, dictionaries):
        self.parser = yacc.yacc(module=self, debug=False)
        self.file_name = file_name
        self.string_text = string_text
        self.methods = []
        self.fields = []
        self.classes = []
        self.variables_list = []
        self.current_class = ""
        self.expressions_stack = []
        self.right_type = []
        self.left_type = []
        self.block_type = []
        self.extends = dictionaries[2]
        self.methods_dict = dictionaries[1]
        self.fields_dict = dictionaries[0]
        self.formals = dictionaries[3]
        self.args_stack = []
        self.inside_field = False

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
        for d in reversed(self.variables_list):
            if(d.get(identifier) != None):
                if self.inside_field and self.search_type_in_fields(identifier, self.current_class) != None:
                    return "error"
                return d[identifier]
        return None

    def compare_types(self, type1, type2):
        result = False
        if type1 == type2:
            return True
        if self.extends.get(type2) != None:
            result = self.compare_types(type1, self.extends[type2])
        return result

    def unordered_compare_types(self, type1, type2):
        result = False
        if type1 == type2:
            return True
        if self.extends.get(type1) != None:
            result = self.compare_types(self.extends[type1], type2)
        if result:
            return result
        if self.extends.get(type2) != None:
            result = self.compare_types(type1, self.extends[type2])
        return result

    def search_type_in_fields(self, identifier, class_id):
        for tuple in self.fields_dict[class_id]:
            if tuple[0] == identifier:
                return tuple[1]
        if self.extends.get(class_id) != None:
            return self.search_type_in_fields(identifier, self.extends[class_id])
        return None

    def type_of_method(self, class_id, method_id):
        for i in self.methods_dict[class_id]:
            if i[0] == method_id:
                if self.inside_field and self.is_extend_of(self.current_class, class_id):
                    return "error"
                return (class_id, i[1])
        if self.extends.get(class_id) != None:
            return self.type_of_method(self.extends[class_id], method_id)
        return None

    def is_extend_of(self, class1, class2):
        if class1 == class2:
            return True
        if self.extends.get(class1) != None:
            if self.extends[class1] == class2:
                return True
            return self.is_extend_of(self.extends[class1], class2)
        return False

    def check_formals(self, args_types, formals):
        for i, formal in enumerate(formals):
            if not self.unordered_compare_types(formal[1], args_types[i]):
                return i
        return -1


    def pop_stores(self):
        self.right_type.pop()
        self.left_type.pop()

    def fill_fields_of_class(self, class_id, vars):
        if self.extends.get(class_id) != None:
            vars = self.fill_fields_of_class(self.extends[class_id], vars)
        for item in self.fields_dict[class_id]:
            vars.update({item[0]: item[1]})
        return vars

    def compute_line(self, p, index):
        return p.lineno(index) - (self.string_text.count('\n') * 2)

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
        s = self.fill_fields_of_class(p[1], s)
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
                | OBJECT_IDENTIFIER COLON type ASSIGN field_inside get_type expression SEMICOLON'''
        if len(p) == 5:
            p[0] = "Field(" + p[1] + ", " + p[3] + ")"
        else:
            self.inside_field = False
            p[0] = "Field(" + p[1] + ", " + p[3] + ", " + p[7] +")"
            expr_type = self.expressions_stack.pop()
            if not self.compare_types(p[3], expr_type):
                colno = p.lexpos(3) - self.string_text.rfind('\n', 0, p.lexpos(3))
                sys.stderr.write("{0}:{1}:{2}: semantic error: expression does not conform to type {3}\n".format(self.file_name, self.compute_line(p, 1), colno, p[3]))
                sys.exit(1)
            if p[7].startswith("Assign"):
                colno = p.lexpos(4) - self.string_text.rfind('\n', 0, p.lexpos(4))
                sys.stderr.write("{0}:{1}:{2}: semantic error: use of unbound variable\n".format(self.file_name, self.compute_line(p, 1), colno))
                sys.exit(1)

    def p_field_inside(self, p):
        'field_inside :'
        p[0] = ''
        self.inside_field = True

    def p_method(self, p):
        'method : OBJECT_IDENTIFIER new_variables_scope LPAR formals RPAR COLON type block'
        p[0] = "Method(" + p[1] + ", [" + p[4] + "], " + p[7] + ", " + p[8] + ")"
        if not self.compare_types(p[7], self.expressions_stack[-1]):
            colno = p.lexpos(8) - self.string_text.rfind('\n', 0, p.lexpos(8))
            sys.stderr.write("{0}:{1}:{2}: semantic error: resulting type of this block is {3}, but expected type was {4}\n".format(self.file_name, self.compute_line(p, 1), colno, self.expressions_stack[-1], p[7]))
            sys.exit(1)
        self.variables_list.pop()

    def p_new_variables_scope(self, p):
        "new_variables_scope :"
        p[0] = ''
        s = { }
        self.variables_list.append(s)

    def p_ret_variables_scope(self, p):
        "ret_variables_scope :"
        p[0] = ''
        self.variables_list.pop()

    def p_type(self, p):
        '''type : TYPE_IDENTIFIER
                | INT32
                | BOOL
                | STRING
                | UNIT '''
        if p[1] not in ["int32", "bool", "string", "unit"] and self.fields_dict.get(p[1]) == None:
            colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
            sys.stderr.write("{0}:{1}:{2}: semantic error: use of undefined type {3}\n".format(self.file_name, self.compute_line(p, 1), colno, p[1]))
            sys.exit(1)
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
        'block : LBRACE get_type check_block new_variables_scope inblock RBRACE'
        result = "[" + p[5] + "]"
        expr_type = self.block_type.pop()
        p[0] = result.replace(';', ', ') + " : " + expr_type
        self.expressions_stack[-1] = expr_type
        self.variables_list.pop()

    def p_check_block(self, p):
        'check_block :'
        self.block_type.append("")
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
        '''expression : IF expression check_bool THEN new_variables_scope expression ret_variables_scope
                    | IF expression check_bool THEN new_variables_scope expression ret_variables_scope ELSE store_left new_variables_scope expression ret_variables_scope'''
        if len(p) == 8:
            self.expressions_stack[-1] = "unit"
            if len(self.block_type) > 0:
                self.block_type[-1] = self.expressions_stack[-1]
            p[0] = "If(" + p[2] + ", " + p[6] + ") : " + self.expressions_stack[-1]
        else:
            p[0] = ''
            if(not self.unordered_compare_types(self.left_type[-1], self.expressions_stack[-1])):
                self.expressions_stack[-1] = "unit"
            self.left_type.pop()
            if len(self.block_type) > 0:
                self.block_type[-1] = self.expressions_stack[-1]
            p[0] = "If(" + p[2] + ", " + p[6] + ", " + p[11] + ") : " + self.expressions_stack[-1]

    def p_while(self, p):
        'expression : WHILE expression check_bool DO new_variables_scope expression ret_variables_scope'
        p[0] = "While(" + p[2] + ", " + p[6] + ") : unit"
        self.expressions_stack[-1] = "unit"
        if len(self.block_type) > 0:
            self.block_type[-1] = "unit"

    def p_let(self, p):
        '''expression : LET let_type IN new_variables_scope expression ret_variables_scope
                    | LET let_type ASSIGN new_variables_scope expression store_right ret_variables_scope IN new_variables_scope expression ret_variables_scope'''
        expr_type = self.expressions_stack[-1]
        if len(p) == 7:
            p[0] = "Let(" + p[2] + ", " + p[5] + ") : " + expr_type
            self.left_type.pop()
        else:
            colno = p.lexpos(5) - self.string_text.rfind('\n', 0, p.lexpos(5))
            if not self.compare_types(self.left_type[-1], self.right_type[-1]):
                sys.stderr.write("{0}:{1}:{2}: semantic error: expected type {3} but found {4}\n".format(self.file_name, self.compute_line(p, 1), colno, self.left_type[-1], self.right_type[-1]))
                sys.exit(1)
            self.pop_stores()
            p[0] = "Let(" + p[2] + ", " + p[5] + ", " + p[10] +") : " + expr_type
        if len(self.block_type) > 0:
            self.block_type[-1] = expr_type

    def p_let_type(self, p):
        "let_type : OBJECT_IDENTIFIER COLON type"
        p[0] = p[1] + ", " + p[3]
        self.add_variable(p[1], p[3])
        self.left_type.append(p[3])

    def p_assign(self, p):
        'expression : OBJECT_IDENTIFIER ASSIGN get_type expression'
        exp_type = self.expressions_stack.pop()
        self.add_variable(p[1], exp_type)
        self.expressions_stack[-1] = exp_type
        if len(self.block_type) > 0:
            self.block_type[-1] = exp_type
        p[0] = "Assign(" + p[1] + ", " + p[4] + ") : " + exp_type

    def p_unary_not(self, p):
        'expression : NOT get_type expression'
        var_type = self.expressions_stack.pop()
        if(var_type != "bool"):
            colno = p.lexpos(0) - self.string_text.rfind('\n', 0, p.lexpos(3))
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type bool but found {3}\n".format(self.file_name, self.compute_line(p, 1), colno, var_type))
            sys.exit(1)
        p[0] = "UnOp(" + p[1] + ", " + p[3] + ") : " + var_type
        self.expressions_stack[-1] = "bool"
        if len(self.block_type) > 0:
            self.block_type[-1] = "bool"

    def p_unary_minus(self, p):
        'expression : MINUS get_type expression %prec UMINUS'
        var_type = self.expressions_stack.pop()
        if(var_type != "int32"):
            colno = p.lexpos(3) - self.string_text.rfind('\n', 0, p.lexpos(3))
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type int32 but found {3}\n".format(self.file_name, self.compute_line(p, 1), colno, var_type))
            sys.exit(1)
        p[0] = "UnOp(" + p[1] + ", " + p[3] + ") : " + var_type
        self.expressions_stack[-1] = "int32"
        if len(self.block_type) > 0:
            self.block_type[-1] = "int32"

    def p_check_bool(self, p):
        "check_bool :"
        colno = p.lexpos(0) - self.string_text.rfind('\n', 0, p.lexpos(0))
        var_type = self.expressions_stack[-1]
        if(var_type != "bool"):
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type bool but found {3}\n".format(self.file_name, p.lineno(0) + 1, colno, var_type))
            sys.exit(1)
        p[0] = ''

    def p_unary_isnull(self, p):
        "expression : ISNULL expression"
        p[0] = "UnOp(" + p[1] + ", " + p[2] + ") : bool"
        if not self.compare_types("Object", self.expressions_stack[-1]):
            colno = p.lexpos(2) - self.string_text.rfind('\n', 0, p.lexpos(2))
            sys.stderr.write("{0}:{1}:{2}: semantic error: this literal has type {3}, but expected type was Object\n".format(self.file_name, self.compute_line(p, 1), colno,self.expressions_stack[-1]))
            sys.exit(1)
        self.expressions_stack[-1] = "bool"
        if len(self.block_type) > 0:
            self.block_type[-1] = "bool"

    def p_binary_equal(self, p):
        'expression : expression store_left EQUAL expression'
        if not self.compare_types(self.left_type[-1], self.expressions_stack[-1]):
            colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type {3} but found {4}\n".format(self.file_name, self.compute_line(p, 3), colno, self.left_type[-1], self.expressions_stack[-1]))
            sys.exit(1)
        self.left_type.pop()
        self.expressions_stack[-1] = "bool"
        if len(self.block_type) > 0:
            self.block_type[-1] = "bool"
        p[0] = "BinOp("+ p[3] +", " + p[1] + ", " + p[4] +") : " + self.expressions_stack[-1]


    def p_binary_and(self, p):
        'expression : expression store_left AND expression'
        if(self.left_type[-1] != "bool"):
            colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type bool but found {3}\n".format(self.file_name, self.compute_line(p, 3), colno, self.left_type[-1]))
            sys.exit(1)
        if(self.expressions_stack[-1] != "bool"):
            colno = p.lexpos(4) - self.string_text.rfind('\n', 0, p.lexpos(4))
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type bool but found {3}\n".format(self.file_name, self.compute_line(p, 3), colno, self.expressions_stack[-1]))
            sys.exit(1)
        self.left_type.pop()
        if len(self.block_type) > 0:
            self.block_type[-1] = "bool"
        p[0] = "BinOp("+ p[3] +", " + p[1] + ", " + p[4] +") : " + self.expressions_stack[-1]

    def p_binary_int_operators(self, p):
        '''expression : expression store_left PLUS expression
                  | expression store_left MINUS expression
                  | expression store_left TIMES expression
                  | expression store_left DIV expression
                  | expression store_left POW expression'''
        if(self.left_type[-1] != "int32"):
            colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type int32 but found {3}\n".format(self.file_name, self.compute_line(p, 3), colno, self.left_type[-1]))
            sys.exit(1)
        if(self.expressions_stack[-1] != "int32"):
            colno = p.lexpos(4) - self.string_text.rfind('\n', 0, p.lexpos(4))
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type int32 but found {3}\n".format(self.file_name, self.compute_line(p, 3), colno, self.expressions_stack[-1]))
            sys.exit(1)
        self.left_type.pop()
        if len(self.block_type) > 0:
            self.block_type[-1] = "int32"
        p[0] = "BinOp("+ p[3] +", " + p[1] + ", " + p[4] +") : " + self.expressions_stack[-1]

    def p_binary_comp_operators(self, p):
        '''expression : expression store_left LOWER_EQUAL expression
                    | expression store_left LOWER expression'''
        if(self.left_type[-1] != "int32"):
            colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type int32 but found {3}\n".format(self.file_name, self.compute_line(p, 3), colno, self.left_type[-1]))
            sys.exit(1)
        if(self.expressions_stack[-1] != "int32"):
            colno = p.lexpos(4) - self.string_text.rfind('\n', 0, p.lexpos(4))
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type int32 but found {3}\n".format(self.file_name, self.compute_line(p, 3), colno, self.expressions_stack[-1]))
            sys.exit(1)
        self.left_type.pop()
        self.expressions_stack[-1] = "bool"
        if len(self.block_type) > 0:
            self.block_type[-1] = "bool"
        p[0] = "BinOp("+ p[3] +", " + p[1] + ", " + p[4] +") : " + self.expressions_stack[-1]


    def p_get_type(self, p):
        "get_type :"
        self.expressions_stack.append("")
        p[0] = ''

    def p_ret_type(self, p):
        "ret_type :"
        self.expressions_stack.pop()
        p[0] = ''

    def p_store_left(self, p):
        "store_left :"
        if len(self.left_type) == 0 or self.left_type[-1] != "":
            self.left_type.append(self.expressions_stack[-1])
        else:
            self.left_type[-1] = self.expressions_stack[-1]
        p[0] = ''

    def p_store_right(self, p):
        "store_right :"
        if len(self.right_type) == 0 or self.right_type[-1] != "":
            self.right_type.append(self.expressions_stack[-1])
        else:
            self.right_type[-1] = self.expressions_stack[-1]
        p[0] = ''

    def p_object_call(self, p):
        '''expression : OBJECT_IDENTIFIER LPAR push_args args RPAR
                    | expression DOT OBJECT_IDENTIFIER LPAR get_type push_args args ret_type RPAR'''
        args_types = self.args_stack.pop()
        if len(p) == 6:
            colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
            result = self.type_of_method(self.current_class, p[1])
            if result is None:
                sys.stderr.write("{0}:{1}:{2}: semantic error: method {3} not defined in this scope\n".format(self.file_name, self.compute_line(p, 1), colno, p[1]))
                sys.exit(1)
            if result == "error":
                sys.stderr.write("{0}:{1}:{2}: semantic error: cannot find method {3} in type <invalid-type>.\n".format(self.file_name, self.compute_line(p, 1), colno, p[1]))
                sys.stderr.write("{0}:{1}:{2}: semantic error: cannot use self in field initializer.\n".format(self.file_name, self.compute_line(p, 1), colno))
                sys.stderr.write("{0}:{1}:{2}: semantic error: use of unbound variable self.\n".format(self.file_name, self.compute_line(p, 1), colno))
                sys.exit(1)
            (class_id, method_type) = result
            formals = self.formals[(class_id, p[1])]
            if len(formals) != len(args_types):
                sys.stderr.write("{0}:{1}:{2}: semantic error: method {3} of class {4} expects {5} arguments, but {6} were provided\n".format(self.file_name, self.compute_line(p, 1), colno, p[3], class_id, len(formals), len(args_types)))
                sys.exit(1)
            index = self.check_formals(args_types, formals)
            if index >= 0:
                sys.stderr.write("{0}:{1}:{2}: semantic error: this literal has type {3}, but expected type was {4}.\n".format(self.file_name, self.compute_line(p, 1), colno, args_types[index], formals[index][1]))
                sys.exit(1)
            if len(self.expressions_stack) > 0:
                self.expressions_stack[-1] = method_type
            if len(self.block_type) > 0:
                self.block_type[-1] = method_type
            p[0] = "Call(self : " + self.current_class + ", " + p[1] + ", [" + p[4] + "]) : " + method_type
        else:
            colno = p.lexpos(3) - self.string_text.rfind('\n', 0, p.lexpos(3))
            t = self.expressions_stack[-1]
            if t is None:
                sys.stderr.write("{0}:{1}:{2}: semantic error: object {3} is not a class\n".format(self.file_name, self.compute_line(p, 3), colno, p[1]))
                sys.exit(1)
            result = self.type_of_method(t, p[3])
            if result is None:
                sys.stderr.write("{0}:{1}:{2}: semantic error: method {3} is not part of class {4}\n".format(self.file_name, self.compute_line(p, 3), colno, p[3], t))
                sys.exit(1)
            if result == "error":
                sys.stderr.write("{0}:{1}:{2}: semantic error: cannot find method {3} in type <invalid-type>.\n".format(self.file_name, self.compute_line(p, 3), colno, p[1]))
                sys.stderr.write("{0}:{1}:{2}: semantic error: cannot use self in field initializer.\n".format(self.file_name, self.compute_line(p, 3), colno))
                sys.stderr.write("{0}:{1}:{2}: semantic error: use of unbound variable self.\n".format(self.file_name, self.compute_line(p, 3), colno))
            (t, method_type) = result
            formals = self.formals[(t, p[3])]
            if len(formals) != len(args_types):
                sys.stderr.write("{0}:{1}:{2}: semantic error: method {3} of class {4} expects {5} arguments, but {6} were provided\n".format(self.file_name, self.compute_line(p, 3), colno, p[3], t, len(formals), len(args_types)))
                sys.exit(1)
            index = self.check_formals(args_types, formals)
            if index >= 0:
                sys.stderr.write("{0}:{1}:{2}: semantic error: this literal has type {3}, but expected type was {4}.\n".format(self.file_name, self.compute_line(p, 3), colno, args_types[index], formals[index][1]))
                sys.exit(1)
            if len(self.expressions_stack) > 0:
                self.expressions_stack[-1] = method_type
            if len(self.block_type) > 0:
                self.block_type[-1] = method_type
            p[0] = "Call("+ p[1] +  ", " + p[3] + ", [" + p[7] + "]) : " + method_type

    def p_push_args(self, p):
        'push_args :'
        p[0] = ''
        self.args_stack.append([])

    def p_new_type(self, p):
        'expression : NEW TYPE_IDENTIFIER'
        p[0] = "New(" + p[2] + ") : " + p[2]
        if len(self.expressions_stack) > 0:
            self.expressions_stack[-1] = p[2]
        if len(self.block_type) > 0:
            self.block_type[-1] = p[2]

    def p_expression_object(self, p):
        'expression : OBJECT_IDENTIFIER'
        t = self.search_type(p[1])
        if t is None:
            colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
            sys.stderr.write("{0}:{1}:{2}: semantic error: an identifier is used that is not defined in the scope\n".format(self.file_name, self.compute_line(p, 1), colno))
            sys.exit(1)
        if t == "error":
            colno = p.lexpos(1) - self.string_text.rfind('\n', 0, p.lexpos(1))
            sys.stderr.write("{0}:{1}:{2}: semantic error: cannot use class fields in field initializers\n".format(self.file_name, self.compute_line(p, 1), colno))
            sys.stderr.write("{0}:{1}:{2}: semantic error: use of unbound variable {3}\n".format(self.file_name, self.compute_line(p, 1), colno, p[1]))
            sys.exit(1)
        p[0] = p[1] + " : " + t
        if len(self.expressions_stack) > 0:
            self.expressions_stack[-1] = t
        if len(self.block_type) > 0:
            self.block_type[-1] = t

    def p_expression_self(self, p):
        'expression : SELF'
        p[0] = p[1] + " : " + self.current_class
        if len(self.expressions_stack) > 0:
            self.expressions_stack[-1] = self.current_class
        if len(self.block_type) > 0:
            self.block_type[-1] = self.current_class

    def p_expression_literal(self, p):
        'expression : literal'
        p[0] = p[1]

    def p_par_alone(self,p):
        'expression : LPAR RPAR'
        p[0] = "() : unit"
        if len(self.expressions_stack) > 0:
            self.expressions_stack[-1] = "unit"
        if len(self.block_type) > 0:
            self.block_type[-1] = "unit"

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
        self.block_type.append(self.expressions_stack[-1])

    def p_expression_error(self, p):
        '''expression : error'''
        sys.stderr.write("invalid expression: {0}\n".format(str(p[1].value)))
        sys.exit(1)

    def p_args(self, p):
        '''args : args COMMA expression
                | expression
                |'''
        if len(p) == 4:
            self.args_stack[-1].append(self.expressions_stack[-1])
            p[0] = p[1] + p[2] + " " + p[3]
        elif len(p) == 2:
            self.args_stack[-1].append(self.expressions_stack[-1])
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
        if len(self.block_type) > 0:
            self.block_type[-1] = "string"

    def p_literal_integer(self, p):
        "literal_integer : INTEGER_LITERAL"
        p[0] = p[1] + " : int32"
        if len(self.expressions_stack) > 0:
            self.expressions_stack[-1] = "int32"
        if len(self.block_type) > 0:
            self.block_type[-1] = "int32"

    def p_boolean_literal(self, p):
        '''boolean-literal : TRUE
                        | FALSE'''
        p[0] = p[1] + " : bool"
        if len(self.expressions_stack) > 0:
            self.expressions_stack[-1] = "bool"
        if len(self.block_type) > 0:
            self.block_type[-1] = "bool"

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
