# -*- coding: utf-8 -*-
"""
Created on Sat May 2021

@author: Guilherme Madureira & Julien Carion
"""
from llvmlite import ir
from llvmlite.binding.ffi import LLVMContextRef

class Tree_node_gen:

    declared_functions = {}
    

    def __init__(self,  module, builder, name, children, values, position, node_class = "", node_type = None):
        self.name = name
        self.type = node_type
        self.children = children
        self.values = values
        self.node_class = node_class
        self.position = position
        self.parent = None
        self.module = module
        self.builder = builder

def set_parent_nodes(node, parent):
    node.parent = parent
    for child in node.children:
        set_parent_nodes(child, node)


def print_tree(node):
    switcher = {
        "boolean literal": compile_expression,
        "integer literal": compile_expression,
        "string literal": compile_expression,
        "args": print_list,
        "par alone": compile_expression,
        "self": compile_expression,
        "object identifier": compile_expression,
        "new type": print_new_type,
        "call": compile_call,
        "binop": compile_binop,
        "unop": compile_unop,
        "assign": compile_assign,
        "let": print_let,
        "while": compile_while,
        "if": compile_if,
        "block": print_block,
        "formals": print_list,
        "formal": print_formal,
        "method": compile_method,
        "field": print_field,
        "methods": print_list,
        "fields": print_list,
        "class": compile_class,
        "program": compile_program
    }    
    string = switcher[node.name](node)
    return string

def compile_tree(node):
    switcher = {
        "boolean literal": compile_expression,
        "integer literal": compile_expression,
        "string literal": compile_expression,
        "args": compile_args,
        "par alone": compile_expression,
        "self": compile_expression,
        "object identifier": compile_expression,
        "new type": print_new_type,
        "call": compile_call,
        "binop": compile_binop,
        "unop": compile_unop,
        "assign": compile_assign,
        "let": print_let,
        "while": compile_while,
        "if": compile_if,
        "block": print_block,
        "formals": print_list,
        "formal": print_formal,
        "method": compile_method,
        "field": print_field,
        "methods": print_list,
        "fields": print_list,
        "class": compile_class,
        "program": compile_program
    }    
    i = switcher[node.name](node)
    return i

def compile_expression(node):

    if node.name == "boolean literal":
        value = 0 if node.values[0] == 'false' else 1
        i = ir.Constant(ir.IntType(1), value)
        return i

    if node.name == "integer literal":
        i = ir.Constant(ir.IntType(32), node.values[0])
        return i

    if node.name == "string literal":
        length = len(node.values[0]) + 1
        i = ir.Constant(ir.ArrayType(ir.IntType(8), length), node.values[0])
        return i

    if node.name == "par alone":
        i = ir.VoidType
        return i

    if node.name == "self":
        # To do
        return 

    if node.name == "object identifier":
        switcher = {
            "int32" : ir.IntType(32),
            "bool": ir.IntType(1),
            "string":ir.ArrayType(ir.IntType(8), 100),
            "unit": ir.VoidType
        }

        type = switcher.get(node.node_type)
        # Add other object identifier more complex 

        i = ir.GlobalVariable(node.module, type, node.values[0])
        return i

def print_list(node, with_types):
    strings = []
    for child in node.children:
        strings.append(print_tree(child, with_types))
    return "[" + ', '.join(strings) + "]"

def print_block(node):
    for child in node.children:
        child.builder = node.builder
        i =  compile_tree(child)
    return i

def print_new_type(node, with_types):
    if with_types and not node.type is None:
        return "New(" + node.values[0] + ") : " + node.type
    return "New(" + node.values[0] + ")"

def compile_args(list, builder):
    args = []
    for node in list:
        node.builder = builder
        for child in node.children:
            child.builder = builder
        
        arg = compile_tree(node)
        args.append(arg)
    return args

def compile_call(node):
    for child in node.children:
        child.builder = node.builder

    if node.children[1].values[0] == "printBool":
        args = compile_args(node.children[2], node.builder)
        node.builder.call("Object__printBool",args)



def compile_plus(node):
     return node.builder.add(compile_tree(node.children[0]), compile_tree(node.children[1]))

def compile_sub(node):
     return node.builder.sub(compile_tree(node.children[0]), compile_tree(node.children[1]))

def compile_times(node):
    return node.builder.mul(compile_tree(node.children[0]), compile_tree(node.children[1]))

def compile_div(node):
    return node.builder.udiv(compile_tree(node.children[0]), compile_tree(node.children[1]))

def compile_pow(node): # Change op
    return node.builder.udiv(compile_tree(node.children[0]), compile_tree(node.children[1]))

def compile_comp(node):
    if node.values[0] != "=":
        return node.builder.icmp_unsigned(node.values[0], compile_tree(node.children[0]), compile_tree(node.children[1]))
    else:
        return node.builder.icmp_unsigned("==", compile_tree(node.children[0]), compile_tree(node.children[1]))

def compile_and(node):
    return node.builder.and_(compile_tree(node.children[0]), compile_tree(node.children[1]))

def compile_binop(node):

    for child in node.children:
        child.builder = node.builder

    switcher = {
        "+" : compile_plus,
        "-": compile_sub,
        "*": compile_times,
        "/": compile_div,
        "^" : compile_pow,
        "=": compile_comp,
        "<=" : compile_comp,
        "<" :compile_comp,
        "and": compile_and
    }
    return switcher[node.values[0]](node)

def compile_not(node):
    return node.builder.not_(compile_tree(node.children[0]))

def compile_minus(node):
    return node.builder.neg(compile_tree(node.children[0]))

def compile_isnull(node):
    return  # Add operation

def compile_unop(node):
    for child in node.children:
        child.builder = node.builder

    switcher = {
        "not" : compile_not(node),
        "-": compile_minus(node),
        "isnull": compile_isnull(node)
        }
    return switcher[node.values[0]](node)
    

def compile_assign(node):
    var_ptr = node.module.get_global(node.children[0].values[0]) # Gets global variable pointer (as global value)
    node.builder.store(compile_tree(node.children[1]),var_ptr)
    return 

def print_let(node, with_types):
    if with_types and not node.type is None:
        if len(node.children) == 3:
            return "Let(" + print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + print_tree(node.children[1], 1) + ", " + print_tree(node.children[2], 1) +") : " + node.type
        return "Let(" + print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + print_tree(node.children[1], 1) +") : " + node.type
    if len(node.children) == 3:
        return "Let(" + print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + print_tree(node.children[1], with_types) + ", " + print_tree(node.children[2], with_types) +")"
    return "Let(" + print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + print_tree(node.children[1], with_types) +")"

def compile_while(node):
    for child in node.children:
        child.builder = node.builder

    with node.builder.if_then(compile_tree([node.children[0]])) as then:
        with then:
            i = compile_tree(node.children[1])
            node.builder.branch(node.builder.block)
    return i

def compile_if(node):
    for child in node.children:
        child.builder = node.builder

    if len(node.children) == 3:
        with node.builder.if_else(compile_tree(node.children[0])) as (then, otherwise):
            with then:
                i = compile_tree(node.children[1])

            with otherwise:
                i = compile_tree(node.children[2])
    else:
        with node.builder.if_then(compile_tree(node.children[0])) as then:
            with then:
                i = compile_tree(node.chilren[1])
    
    return i

def print_formal(node):
    return compile_expression(node, 1)

def compile_method(node):
    type = create_type(node.node_type)
    fnty = ir.FunctionType(type, ())
    func = ir.Function(node.module, fnty, name=node.value[0])

    block = func.append_basic_block(name=node.values[0])
    builder = ir.IRBuilder(block)
    node.builder = builder
    return 


def compile_main(node):
    fnty = ir.FunctionType(ir.IntType(32), [], False)
    func = ir.Function(node.module, fnty, name="main")

    block = func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    node.builder = builder
    node.children[2].builder = builder
    node.parent.builder = builder
    
    return compile_tree(node.children[2])


def print_field(node, with_types):
    if len(node.children) == 2:
        return "\nField(" + print_tree(node.children[0], 0) + ", " + node.type + ", " + print_tree(node.children[1], with_types) +")"
    return "\nField(" + print_tree(node.children[0], 0) + ", " + node.type +")"

def compile_class(node):
    context = LLVMContextRef.get_global_context()
    if len(node.values == 1):
        ir.IdentifiedStructType(context, node.values[0]).set_body([compile_tree(node.children[0]), compile_tree(node.children[1])])
    else:
        ir.IdentifiedStructType(context, node.values[0]).set_body([compile_tree(node.children[0]), compile_tree(node.children[1])]) # Must add fields and methods from parent


def execute_main(node):
    result = compile_main(node.children[0])
    node.builder.ret(result)


def compile_program(node, dictionaries):
    for child in node.children:
        if child.values[0] == "Main":
            execute_main(child.children[1])
        elif child.values[0] != "Object":
            compile_other_class(child, dictionaries)
    return node.module



def compile_other_class(node, dictionaries):

    # extensions checking to do + creating structures for each class such as in object
    return 



def create_type(type):

    if type == "int32":
        return ir.Type(32)
    elif type == "bool":
        return ir.Type(1)
    elif type == "unit":
        return ir.VoidType()
    elif type == "string":
        return ir.ArrayType(ir.IntType(8), 100)
    else:
        return 0 # Returns class type (to implement)



    