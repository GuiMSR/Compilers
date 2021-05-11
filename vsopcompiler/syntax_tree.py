# -*- coding: utf-8 -*-
"""
Created on Sat May 2021

@author: Guilherme Madureira & Julien Carion
"""

class Tree_node:
    def __init__(self, name, children, values, position, node_class = "", node_type = None):
        self.name = name
        self.type = node_type
        self.children = children
        self.values = values
        self.node_class = node_class
        self.position = position
        self.parent = None

def set_parent_nodes(node, parent):
    node.parent = parent
    for child in node.children:
        set_parent_nodes(child, node)


def print_tree(node, with_types):
    switcher = {
        "boolean literal": print_expression,
        "integer literal": print_expression,
        "string literal": print_expression,
        "args": print_list,
        "par alone": print_expression,
        "self": print_expression,
        "object identifier": print_expression,
        "new type": print_new_type,
        "call": print_call,
        "binop": print_binop,
        "unop": print_unop,
        "assign": print_assign,
        "let": print_let,
        "while": print_while,
        "if": print_if,
        "block": print_block,
        "formals": print_list,
        "formal": print_formal,
        "method": print_method,
        "field": print_field,
        "methods": print_list,
        "fields": print_list,
        "class": print_class,
        "program": print_program
    }    
    string = switcher[node.name](node, with_types)
    return string

def print_expression(node, with_types):
    if with_types and not node.type is None:
        return node.values[0] + " : " + node.type
    return node.values[0]

def print_list(node, with_types):
    strings = []
    for child in node.children:
        strings.append(print_tree(child, with_types))
    return "[" + ', '.join(strings) + "]"

def print_block(node, with_types):
    strings = []
    for child in node.children:
        strings.append(print_tree(child, with_types))
    if with_types and not node.type is None:
        return "[" + ', '.join(strings) + "] : " + node.type
    return "[" + ', '.join(strings) + "]"

def print_new_type(node, with_types):
    if with_types and not node.type is None:
        return "New(" + node.values[0] + ") : " + node.type
    return "New(" + node.values[0] + ")"

def print_call(node, with_types):
    if with_types and not node.type is None:
        return "\nCall("+ print_tree(node.children[0], 1) +  ", " + print_tree(node.children[1], 1) + ", " + print_tree(node.children[2], 1) + ") : " + node.type
    return "\nCall("+ print_tree(node.children[0], with_types) +  ", " + print_tree(node.children[1], with_types) + ", " + print_tree(node.children[2], with_types) + ")"

def print_binop(node, with_types):
    if with_types and not node.type is None:
        return "BinOp("+ node.values[0] +", " + print_tree(node.children[0], 1) + ", " + print_tree(node.children[1], 1) +") : " + node.type
    return "BinOp("+ node.values[0] +", " + print_tree(node.children[0], with_types) + ", " + print_tree(node.children[1], with_types) +")"

def print_unop(node, with_types):
    if with_types and not node.type is None:
        return "UnOp("+ node.values[0] +", " + print_tree(node.children[0], 1) +") : " + node.type
    return "UnOp("+ node.values[0] +", " + print_tree(node.children[0], with_types) + ")"

def print_assign(node, with_types):
    if with_types and not node.type is None:
        return "Assign("+ print_tree(node.children[0], 1) + ", " + print_tree(node.children[1], 1) +") : " + node.type
    return "Assign("+ print_tree(node.children[0], with_types) + ", " + print_tree(node.children[1], with_types) +")"

def print_let(node, with_types):
    if with_types and not node.type is None:
        if len(node.children) == 3:
            return "Let(" + print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + print_tree(node.children[1], 1) + ", " + print_tree(node.children[2], 1) +") : " + node.type
        return "Let(" + print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + print_tree(node.children[1], 1) +") : " + node.type
    if len(node.children) == 3:
        return "Let(" + print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + print_tree(node.children[1], with_types) + ", " + print_tree(node.children[2], with_types) +")"
    return "Let(" + print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + print_tree(node.children[1], with_types) +")"

def print_while(node, with_types):
    if with_types and not node.type is None:
        return "While("+ print_tree(node.children[0], 1) + ", " + print_tree(node.children[1], 1) +") : " + node.type
    return "While("+ print_tree(node.children[0], with_types) + ", " + print_tree(node.children[1], with_types) +")"

def print_if(node, with_types):
    if with_types and not node.type is None:
        if len(node.children) == 3:
            return "If(" + print_tree(node.children[0], 1) + ", " + print_tree(node.children[1], 1) + ", " + print_tree(node.children[2], 1) +") : " + node.type
        return "If(" + print_tree(node.children[0], 1) + ", " + print_tree(node.children[1], 1) +") : " + node.type
    if len(node.children) == 3:
        return "If(" + print_tree(node.children[0], with_types) + ", " + print_tree(node.children[1], with_types) + ", " + print_tree(node.children[2], with_types) +")"
    return "If(" + print_tree(node.children[0], with_types) + ", " + print_tree(node.children[1], with_types) +")"

def print_formal(node, with_types):
    return print_expression(node, 1)

def print_method(node, with_types):
    return "\nMethod(" + print_tree(node.children[0], 0) + ", " + print_tree(node.children[1], with_types) + ", " + node.type + ", " + print_tree(node.children[2], with_types) + ")"

def print_field(node, with_types):
    if len(node.children) == 2:
        return "\nField(" + print_tree(node.children[0], 0) + ", " + node.type + ", " + print_tree(node.children[1], with_types) +")"
    return "\nField(" + print_tree(node.children[0], 0) + ", " + node.type +")"

def print_class(node, with_types):
    if len(node.values) == 2:
        return "Class(" + node.values[0] + ", " + node.values[1] + ", " + print_tree(node.children[0], with_types) + ", " + print_tree(node.children[1], with_types) + ")"
    return "Class(" + node.values[0] + ", Object, " + print_tree(node.children[0], with_types) + ", " + print_tree(node.children[1], with_types) + ")"

def print_program(node, with_types):
    strings = []
    for child in node.children:
        strings.append(print_tree(child, with_types))
    return "[" + ', \n'.join(strings) + "]"






    