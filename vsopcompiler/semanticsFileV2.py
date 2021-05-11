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


class VsopParser2V2():


    def __init__(self, lexer, file_name, string_text, dictionaries):
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
        self.extends = dictionaries[2]
        self.methods_dict = dictionaries[1]
        self.fields_dict = dictionaries[0]
        self.formals_dict = dictionaries[3]
        self.variables_list = []
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

    def fill_fields_of_class(self, class_id, vars):
        if self.extends.get(class_id) != None:
            vars = self.fill_fields_of_class(self.extends[class_id], vars)
        for item in self.fields_dict[class_id]:
            vars.update({item[0]: item[1]})
        return vars

    def search_type(self, identifier):
        for d in reversed(self.variables_list):
            if(d.get(identifier) != None):
                if self.inside_field and self.search_type_in_fields(identifier, self.current_class) != None:
                    return "error"
                return d[identifier]
        return None

    def check_formals(self, args_types, formals):
        for i, formal in enumerate(formals):
            if not self.unordered_compare_types(formal[1], args_types[i]):
                return i
        return -1

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
        
    def add_variable(self, identifier, type_id):
        self.variables_list[-1].update({identifier: type_id})

    def is_extend_of(self, class1, class2):
        if class1 == class2:
            return True
        if self.extends.get(class1) != None:
            if self.extends[class1] == class2:
                return True
            return self.is_extend_of(self.extends[class1], class2)
        return False

    def type_of_method(self, class_id, method_id):
        for i in self.methods_dict[class_id]:
            if i[0] == method_id:
                if self.inside_field and self.is_extend_of(self.current_class, class_id):
                    return "error"
                return (class_id, i[1])
        if self.extends.get(class_id) != None:
            return self.type_of_method(self.extends[class_id], method_id)
        return None

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
        self.variables_list.pop()

    def p_new_class_scope(self, p):
        "new_class_scope : TYPE_IDENTIFIER"
        p[0] = p[1]
        self.current_class = p[1]
        s = { }
        s = self.fill_fields_of_class(p[1], s)
        self.variables_list.append(s)

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
        '''field : field_identifier SEMICOLON
                | field_identifier ASSIGN expression SEMICOLON'''
        pos = p[1].position
        if len(p) == 3:
            p[0] = st.Tree_node("field", [p[1]], [], pos, self.current_class, p[1].type)
        else:
            p[0] = st.Tree_node("field", [p[1], p[3]], [], pos, self.current_class, p[1].type)
            if not self.compare_types(p[1].type, p[3].type):
                pos = p[3].position
                sys.stderr.write("{0}:{1}:{2}: semantic error: expression does not conform to type {3}\n".format(self.file_name, pos[0], pos[1], p[1].type))
                sys.exit(1)
            # if p[3].name == "assign":
            #     pos = p[3].position
            #     sys.stderr.write("{0}:{1}:{2}: semantic error: use of unbound variable\n".format(self.file_name, pos[0], pos[1]))
            #     sys.exit(1)
        self.inside_field = False

    def p_field_identifier(self, p):
        'field_identifier : OBJECT_IDENTIFIER COLON type'
        pos = self.find_position(p, 1)
        self.inside_field = True
        p[0] = st.Tree_node("object identifier", [], [p[1]], pos, self.current_class, p[3])

    def p_method(self, p):
        'method : method_identifier LPAR formals RPAR COLON type block'
        pos = self.find_position(p, 2)
        p[0] = st.Tree_node("method", [st.Tree_node("object identifier", [], [p[1]], pos, self.current_class, p[6]), st.Tree_node("formals", self.formals[-1], [], self.find_position(p, 4), self.current_class), p[7]], [], pos, self.current_class, p[6])
        if not self.compare_types(p[6], p[7].type):
            pos = p[7].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: resulting type of this block is {3}, but expected type was {4}\n".format(self.file_name, pos[0], pos[1], p[7].type, p[6]))
            sys.exit(1)
        # if p[7].children[-1].name == "assign":
        #     pos = p[7].children[-1].position
        #     var = p[7].children[-1].children[0].values[0]
        #     sys.stderr.write("{0}:{1}:{2}: semantic error: use of unbound variable {3}\n".format(self.file_name, pos[0], pos[1], var))
        #     sys.exit(1)
        del self.formals[-1]
        self.variables_list.pop()

    def p_method_identifier(self, p):
        'method_identifier : OBJECT_IDENTIFIER'
        p[0] = p[1]
        self.formals.append([])
        s = { }
        self.variables_list.append(s)

    def p_type(self, p):
        '''type : TYPE_IDENTIFIER
                | INT32
                | BOOL
                | STRING
                | UNIT '''
        if p[1] not in ["int32", "bool", "string", "unit"] and self.fields_dict.get(p[1]) == None:
            pos = self.find_position(p, 1)
            sys.stderr.write("{0}:{1}:{2}: semantic error: use of undefined type {3}\n".format(self.file_name, pos[0], pos[1], p[1]))
            sys.exit(1)
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
        self.add_variable(p[1], p[3])

    def p_block(self, p): 
        'block : block_lbrace inblock RBRACE'
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
                | expression
                |'''
        if len(p) == 2:
            p[0] = None
            self.blocks[-1].append(p[1])
        elif len(p) == 4:
            p[0] = None
            self.blocks[-1].append(p[3])
        else:
            p[0] = None

    def p_block_error(self,p):
        '''inblock : inblock error '''
        sys.stderr.write("semicolon is missing after block element\n")
        sys.exit(1)

    def p_if(self, p):
        '''expression : IF expression THEN expression
                    | IF expression THEN expression ELSE expression'''
        if(p[2].type != "bool"):
            pos = p[2].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type bool but found {3}\n".format(self.file_name, pos[0], pos[1], p[2].type))
            sys.exit(1)
        pos = self.find_position(p, 1)
        if len(p) == 5:
            p[0] = st.Tree_node("if", [p[2], p[4]], [], pos, self.current_class, "unit")
        else: 
            if self.unordered_compare_types(p[4].type, p[6].type):
                p[0] = st.Tree_node("if", [p[2], p[4], p[6]], [], pos, self.current_class, p[6].type)
            else:
                p[0] = st.Tree_node("if", [p[2], p[4], p[6]], [], pos, self.current_class, "unit")

    def p_while(self, p):
        'expression : WHILE expression DO expression'
        if(p[2].type != "bool"):
            pos = p[2].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type bool but found {3}\n".format(self.file_name, pos[0], pos[1], p[2].type))
            sys.exit(1)
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("while", [p[2], p[4]], [], pos, self.current_class, "unit")

    def p_let(self, p):
        '''expression : LET let_type let_in expression
                    | LET let_type ASSIGN expression let_in expression'''
        pos = self.find_position(p, 1)
        if len(p) == 5:
            p[0] = st.Tree_node("let", [p[2], p[4]], [], pos, self.current_class, p[4].type)
        else:
            if not self.compare_types(p[2].type, p[4].type):
                position = p[4].position
                sys.stderr.write("{0}:{1}:{2}: semantic error: expected type {3} but found {4}\n".format(self.file_name, position[0], position[1], p[2].type, p[4].type))
                sys.exit(1)
            p[0] = st.Tree_node("let", [p[2], p[4], p[6]], [], pos, self.current_class, p[6].type)
        self.variables_list.pop()

    def p_let_type(self, p):
        "let_type : OBJECT_IDENTIFIER COLON type"
        p[0] = st.Tree_node("object identifier", [], [p[1]], self.find_position(p, 1), self.current_class, p[3])
        self.add_variable(p[1], p[3])

    def p_let_in(self, p):
        "let_in : IN"
        s = { }
        self.variables_list.append(s)
        p[0] = p[1]

    def p_assign(self, p):
        'expression : OBJECT_IDENTIFIER ASSIGN expression'
        pos = self.find_position(p, 1)
        t = self.search_type(p[1])
        if t is None:
            sys.stderr.write("{0}:{1}:{2}: semantic error: use of unbound variable {3}\n".format(self.file_name, pos[0], pos[1], p[1]))
            sys.exit(1)
        if t == "error":
            sys.stderr.write("{0}:{1}:{2}: semantic error: cannot use class fields in field initializers\n".format(self.file_name, pos[0], pos[1]))
            sys.stderr.write("{0}:{1}:{2}: semantic error: use of unbound variable {3}\n".format(self.file_name, pos[0], pos[1], p[1]))
            sys.exit(1)
        p[0] = st.Tree_node("assign", [st.Tree_node("object identifier", [], [p[1]], pos, self.current_class), p[3]], [], pos, self.current_class, p[3].type)
        self.add_variable(p[1], p[3])

    def p_unary_not(self, p):
        'expression : NOT expression'
        if(p[2].type != "bool"):
            pos = p[2].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type bool but found {3}\n".format(self.file_name, pos[0], pos[1], p[2].type))
            sys.exit(1)
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("unop", [p[2]], [p[1]], pos, self.current_class, "bool")

    def p_unary_minus(self, p):
        'expression : MINUS expression %prec UMINUS'
        if(p[2].type != "int32"):
            pos = p[2].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type int32 but found {3}\n".format(self.file_name, pos[0], pos[1], p[2].type))
            sys.exit(1)
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("unop", [p[2]], [p[1]], pos, self.current_class, "int32")

    def p_unary_isnull(self, p):
        "expression : ISNULL expression"
        if not self.compare_types("Object", p[2].type):
            pos = p[2].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: this literal has type {3}, but expected type was Object\n".format(self.file_name, pos[0], pos[1], p[2].type))
            sys.exit(1)
        pos = self.find_position(p, 1)
        p[0] = st.Tree_node("unop", [p[2]], [p[1]], pos, self.current_class, "bool")

    def p_binary_equal(self, p):
        'expression : expression EQUAL expression'
        if not self.compare_types(p[1].type, p[3].type):
            pos = p[3].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type {3} but found {4}\n".format(self.file_name, pos[0], pos[1], p[1].type, p[3].type))
            sys.exit(1)
        pos = self.find_position(p, 2)
        p[0] = st.Tree_node("binop", [p[1], p[3]], [p[2]], pos, self.current_class, "bool")


    def p_binary_and(self, p):
        'expression : expression AND expression'
        if(p[1].type != "bool"):
            pos = p[1].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type bool but found {3}\n".format(self.file_name, pos[0], pos[1], p[1].type))
            sys.exit(1)
        if(p[3].type != "bool"):
            pos = p[3].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type bool but found {3}\n".format(self.file_name, pos[0], pos[1], p[3].type))
            sys.exit(1)
        pos = self.find_position(p, 2)
        p[0] = st.Tree_node("binop", [p[1], p[3]], [p[2]], pos, self.current_class, "bool")

    def p_binary_int_operators(self, p):
        '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIV expression
                  | expression POW expression'''
        if(p[1].type != "int32"):
            pos = p[1].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type int32 but found {3}\n".format(self.file_name, pos[0], pos[1], p[1].type))
            sys.exit(1)
        if(p[3].type != "int32"):
            pos = p[3].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type int32 but found {3}\n".format(self.file_name, pos[0], pos[1], p[3].type))
            sys.exit(1)
        pos = self.find_position(p, 2)
        p[0] = st.Tree_node("binop", [p[1], p[3]], [p[2]], pos, self.current_class, "int32")

    def p_binary_comp_operators(self, p):
        '''expression : expression LOWER_EQUAL expression
                    | expression LOWER expression'''
        if(p[1].type != "int32"):
            pos = p[1].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type int32 but found {3}\n".format(self.file_name, pos[0], pos[1], p[1].type))
            sys.exit(1)
        if(p[3].type != "int32"):
            pos = p[3].position
            sys.stderr.write("{0}:{1}:{2}: semantic error: expected type int32 but found {3}\n".format(self.file_name, pos[0], pos[1], p[3].type))
            sys.exit(1)
        pos = self.find_position(p, 2)
        p[0] = st.Tree_node("binop", [p[1], p[3]], [p[2]], pos, self.current_class, "bool")  


    def p_object_call(self, p):
        '''expression : call_identifier LPAR args RPAR
                    | expression DOT call_identifier LPAR args RPAR'''
        pos = self.find_position(p, 2)
        args_types = []
        for arg in self.args[-1]:
            args_types.append(arg.type)
        if len(p) == 5:
            result = self.type_of_method(self.current_class, p[1])
            if result is None:
                sys.stderr.write("{0}:{1}:{2}: semantic error: method {3} not defined in this scope\n".format(self.file_name, pos[0], pos[1], p[1]))
                sys.exit(1)
            if result == "error":
                sys.stderr.write("{0}:{1}:{2}: semantic error: cannot find method {3} in type <invalid-type>.\n".format(self.file_name, pos[0], pos[1], p[1]))
                sys.stderr.write("{0}:{1}:{2}: semantic error: cannot use self in field initializer.\n".format(self.file_name, pos[0], pos[1]))
                sys.stderr.write("{0}:{1}:{2}: semantic error: use of unbound variable self.\n".format(self.file_name, pos[0], pos[1]))
                sys.exit(1)
            (class_id, method_type) = result
            formals = self.formals_dict[(class_id, p[1])]
            if len(formals) != len(args_types):
                sys.stderr.write("{0}:{1}:{2}: semantic error: method {3} of class {4} expects {5} arguments, but {6} were provided\n".format(self.file_name, pos[0], pos[1], p[1], class_id, len(formals), len(args_types)))
                sys.exit(1)
            index = self.check_formals(args_types, formals)
            if index >= 0:
                sys.stderr.write("{0}:{1}:{2}: semantic error: this literal has type {3}, but expected type was {4}.\n".format(self.file_name, pos[0], pos[1], args_types[index], formals[index][1]))
                sys.exit(1)
            p[0] = st.Tree_node("call", [st.Tree_node("self", [], ["self"], pos, self.current_class, self.current_class), st.Tree_node("object identifier", [], [p[1]], pos, self.current_class), st.Tree_node("args", self.args[-1], [], self.find_position(p, 4), self.current_class)], [], pos, self.current_class, method_type)
        else: 
            pos_o = self.find_position(p, 2)
            t = p[1].type
            if t is None:
                sys.stderr.write("{0}:{1}:{2}: semantic error: object {3} is not a class\n".format(self.file_name, p[1].position[0], p[1].position[1], p[1]))
                sys.exit(1)
            result = self.type_of_method(t, p[3])
            if result is None:
                sys.stderr.write("{0}:{1}:{2}: semantic error: method {3} is not part of class {4}\n".format(self.file_name, pos_o[0], pos_o[1], p[3], t))
                sys.exit(1)
            if result == "error":
                sys.stderr.write("{0}:{1}:{2}: semantic error: cannot find method {3} in type <invalid-type>.\n".format(self.file_name, pos_o[0], pos_o[1], p[1]))
                sys.stderr.write("{0}:{1}:{2}: semantic error: cannot use self in field initializer.\n".format(self.file_name, pos_o[0], pos_o[1]))
                sys.stderr.write("{0}:{1}:{2}: semantic error: use of unbound variable self.\n".format(self.file_name, pos_o[0], pos_o[1]))
            (t, method_type) = result
            formals = self.formals_dict[(t, p[3])]
            if len(formals) != len(args_types):
                sys.stderr.write("{0}:{1}:{2}: semantic error: method {3} of class {4} expects {5} arguments, but {6} were provided\n".format(self.file_name, pos_o[0], pos_o[1], p[3], t, len(formals), len(args_types)))
                sys.exit(1)
            index = self.check_formals(args_types, formals)
            if index >= 0:
                sys.stderr.write("{0}:{1}:{2}: semantic error: this literal has type {3}, but expected type was {4}.\n".format(self.file_name, pos_o[0], pos_o[1], args_types[index], formals[index][1]))
                sys.exit(1)
            p[0] = st.Tree_node("call", [p[1], st.Tree_node("object identifier", [], [p[3]], self.find_position(p, 4), self.current_class), st.Tree_node("args", self.args[-1], [], self.find_position(p, 6), self.current_class)], [], pos, self.current_class, method_type) 
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
        t = self.search_type(p[1])
        if t is None:
            sys.stderr.write("{0}:{1}:{2}: semantic error: an identifier is used that is not defined in the scope : {3}\n".format(self.file_name, pos[0], pos[1], p[1]))
            sys.exit(1)
        if t == "error":
            sys.stderr.write("{0}:{1}:{2}: semantic error: cannot use class fields in field initializers\n".format(self.file_name, pos[0], pos[1]))
            sys.stderr.write("{0}:{1}:{2}: semantic error: use of unbound variable {3}\n".format(self.file_name, pos[0], pos[1], p[1]))
            sys.exit(1)
        p[0] = st.Tree_node("object identifier", [], [p[1]], pos, self.current_class, t)

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

    def find_position(self, p, i):
        colno = p.lexpos(i) - self.string_text.rfind('\n', 0, p.lexpos(i))
        lineno = 1 if p.lineno(i) == 0 else p.lineno(i) - self.string_text.count('\n') * 2
        return (lineno, colno)
