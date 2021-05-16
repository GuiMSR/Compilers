from llvmlite import ir, binding
import sys, os
from llvmlite.ir import context

from llvmlite.ir.values import GlobalVariable
import object


class variableScope():

    # Create new scope for each field and method

    def __init__(self):
        self.scopes = [{}]

    def addScope(self):
        self.scopes.append({})
    
    def removeScope(self):
        self.scopes.pop()
    
    def addVariable(self, key, value):
        self.scopes[-1][key] = value

    def getValue(self, key):
        for d in reversed(self.scopes):
            if d.get(key) != None:
                return d[key]
        return None


class CodeGen():

    def __init__(self, parsed_tree, dictionaries):
        self.tree = parsed_tree
        self.extends = dictionaries[2]
        self.methods_dict = dictionaries[1]
        self.fields_dict = dictionaries[0]
        self.formals_dict = dictionaries[3]
        self.module = ir.Module(name="vsop")
        self.binding = binding
        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_all_asmprinters()
        self._create_execution_engine()
        self.module.triple = self.binding.get_default_triple()
        

    def codeGeneration(self):
        self.types = {
            'int32' : ir.IntType(32),
            'string': ir.IntType(8).as_pointer(),
            'bool'  : ir.IntType(1),
            'unit'  : ir.VoidType()
            }

        self.dict = {'Object': {}}
        mallocType = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(64)])
        self.malloc = ir.Function(self.module, mallocType, name='malloc')
        self.compile_object()
        self.compile_classes()
        self.compile_program(self.tree)

    def save_ir(self, filename):
        result = str(self.module)
        object_ll = object.getObject()
        result = object_ll + result
        output_file = open(filename + '.ll', 'w')
        output_file.write(result)
        output_file.close()
        os.system('llc < ' + filename + '.ll > ' + filename + '.s')
        os.system('clang ' + filename + '.s -lm -o ' + filename) 

    def print_ir(self):
        result = str(self.module)
        object_ll = object.getObject()
        result = object_ll + result
        sys.stdout.write(result)

    def print_ir_only(self, module):
        sys.stdout.write(str(module))


    def _create_execution_engine(self):
        target = self.binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_module = self.binding.parse_assembly("")
        self.engine = self.binding.create_mcjit_compiler(backing_module, target_machine)

    def _compile_ir(self):
        ir_str = add_object()
        llvm_ir = ir_str
        module = self.binding.parse_assembly(llvm_ir)
        module.name = "vsopc"
        self.module = module
    
    def _end_ir(self):
        self.module.verify()
        self.engine.add_module(self.module)
        self.engine.finalize_object()
        self.engine.run_static_constructors()

    
    def compile_tree(self, node, builder, scope):
        switcher = {
            "boolean literal": self.compile_expression,
            "integer literal": self.compile_expression,
            "string literal": self.compile_expression,
            "args": self.compile_args,
            "par alone": self.compile_expression,
            "self": self.compile_expression,
            "object identifier": self.compile_expression,
            "new type": self.print_new_type,
            "call": self.compile_call,
            "binop": self.compile_binop,
            "unop": self.compile_unop,
            "assign": self.compile_assign,
            "let": self.print_let,
            "while": self.compile_while,
            "if": self.compile_if,
            "block": self.compile_block,
            "formals": self.print_list,
            "formal": self.print_formal,
            "method": self.compile_method,
            "field": self.print_field,
            "methods": self.print_list,
            "fields": self.print_list
        }    
        i = switcher[node.name](node, builder, scope)
        return i

    def compile_expression(self, node, builder, scope):

        if node.name == "boolean literal":
            value = 0 if node.values[0] == 'false' else 1
            i = ir.Constant(ir.IntType(1), value)
            return i

        if node.name == "integer literal":
            i = ir.Constant(ir.IntType(32), node.values[0])
            return i

        if node.name == "string literal":
            string = node.values[0][1:-1]
            #Convert \xhh to utf8

            string = string.replace('\\x09', bytearray.fromhex('09').decode())
            string = string.replace('\\x0a', bytearray.fromhex('0a').decode())
            string = string.replace('\\x08', bytearray.fromhex('08').decode())
            string = string.replace('\\x0d', bytearray.fromhex('0d').decode())
            string = string.replace('\\x5c', bytearray.fromhex('5c').decode())
            string = string.replace('\\x22', bytearray.fromhex('22').decode())
            string += chr(0)
            length = len(string)
            constant = ir.Constant(ir.ArrayType(ir.IntType(8), length), bytearray(string.encode('utf8')))
            globalVar = ir.GlobalVariable(self.module, constant.type, self.module.get_unique_name('string'))
            globalVar.global_constant = True
            globalVar.initializer = constant
            stringPtr = builder.gep(globalVar, [self.types['int32'](0), self.types['int32'](0)], inbounds=True)
            return stringPtr

        if node.name == "par alone":
            i = ir.VoidType
            return i

        if node.name == "object identifier" or node.name == "self":

            ptr = scope.getValue(node.values[0])

            if ptr is not None:
                value = builder.load(ptr)
            else:
                field = self.dict[node.node_class]['fields'].get(node.values[0])
                temp = list(self.dict[node.node_class]['fields'].items()) 
                index = [idx for idx, key in enumerate(temp) if key[0] == node.values[0]]
                selfPtr = scope.getValue(node.node_class)
                ld = builder.load(selfPtr)
                fctType = builder.gep(ld, [self.types['int32'](0), self.types['int32'](index[0])], inbounds=True)
                value = builder.load(fctType)

            return value

    def print_list(self, node, with_types):
        strings = []
        for child in node.children:
            strings.append(self.print_tree(child, with_types))
        return "[" + ', '.join(strings) + "]"

    def compile_block(self, node, builder, scope):
        scope.addScope()

        for child in node.children:
            i =  self.compile_tree(child, builder, scope)
        
        scope.removeScope()
        return i

    def print_new_type(self, node, with_types):
        if with_types and not node.type is None:
            return "New(" + node.values[0] + ") : " + node.type
        return "New(" + node.values[0] + ")"

    def compile_args(self, node, builder, scope):
        args = []
        for child in node.children:
            arg = self.compile_tree(child, builder, scope)
            args.append(arg)
        return args

    def compile_call(self, node, builder, scope):

        class_name = node.children[0].type
        method_name = node.children[1].values[0]

        if class_name == "Main":
            method_list = self.dict["Object"]["methods"][method_name]
        else:
            method_list = self.dict[class_name]["methods"][method_name]

        # Recover function and its arguments
        fctPtr = method_list[1]
        fct = builder.load(fctPtr)
        args = self.compile_args(node.children[2], builder, scope)
        # Recover self argument and function arguments casts
        value = self.compile_tree(node.children[0], builder, scope)
        cast = builder.bitcast(value, method_list[1].args[0].type)
        fct_args = [cast]
        for i, arg in enumerate(args):
            cast = builder.bitcast(arg, method_list[1].args[i+1].type)
            fct_args.append(cast)

        return builder.call(fct, fct_args)


    def compile_plus(self, node, builder, scope):
        return builder.add(self.compile_tree(node.children[0], builder, scope), self.compile_tree(node.children[1], builder, scope))

    def compile_sub(self, node, builder, scope):
        return builder.sub(self.compile_tree(node.children[0], builder, scope), self.compile_tree(node.children[1], builder, scope))

    def compile_times(self, node, builder, scope):
        return builder.mul(self.compile_tree(node.children[0], builder, scope), self.compile_tree(node.children[1], builder, scope))

    def compile_div(self, node, builder, scope):
        return builder.udiv(self.compile_tree(node.children[0], builder, scope), self.compile_tree(node.children[1], builder, scope))

    def compile_pow(self, node, builder, scope): # Change op
        return builder.udiv(self.compile_tree(node.children[0], builder, scope), self.compile_tree(node.children[1], builder, scope))

    def compile_comp(self, node, builder, scope):
        if node.values[0] != "=":
            return builder.icmp_unsigned(node.values[0], self.compile_tree(node.children[0], builder, scope), self.compile_tree(node.children[1], builder, scope))
        else:
            return builder.icmp_unsigned("==", self.compile_tree(node.children[0], builder, scope), self.compile_tree(node.children[1], builder, scope))

    def compile_and(self, node, builder, scope):
        return builder.and_(self.compile_tree(node.children[0], builder, scope), self.compile_tree(node.children[1], builder, scope))

    def compile_binop(self, node, builder, scope):

        switcher = {
            "+" : self.compile_plus,
            "-": self.compile_sub,
            "*": self.compile_times,
            "/": self.compile_div,
            "^" : self.compile_pow,
            "=": self.compile_comp,
            "<=" : self.compile_comp,
            "<" :self.compile_comp,
            "and": self.compile_and
        }
        return switcher[node.values[0]](node, builder, scope)

    def compile_not(self, node, builder, scope):
        return builder.not_(self.compile_tree(node.children[0]))

    def compile_minus(self, node, builder, scope):
        return builder.neg(self.compile_tree(node.children[0]))

    def compile_isnull(self, node, builder, scope):
        return  # Add operation

    def compile_unop(self, node, builder, scope):
        for child in node.children:
            child.builder = builder

        switcher = {
            "not" : self.compile_not(node, builder, scope),
            "-": self.compile_minus(node, builder, scope),
            "isnull": self.compile_isnull(node, builder, scope)
            }
        return switcher[node.values[0]](node, builder, scope)
        

    def compile_assign(self, node, builder, scope):
        var_ptr = self.module.get_global(node.children[0].values[0]) # Gets global variable pointer (as global value)
        builder.store(self.compile_tree(node.children[1]),var_ptr)
        return 

    def print_let(self, node, with_types):
        if with_types and not node.type is None:
            if len(node.children) == 3:
                return "Let(" + self.print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + self.print_tree(node.children[1], 1) + ", " + self.print_tree(node.children[2], 1) +") : " + node.type
            return "Let(" + self.print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + self.print_tree(node.children[1], 1) +") : " + node.type
        if len(node.children) == 3:
            return "Let(" + self.print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + self.print_tree(node.children[1], with_types) + ", " + self.print_tree(node.children[2], with_types) +")"
        return "Let(" + self.print_tree(node.children[0], 0) + ", " + node.children[0].type + ", " + self.print_tree(node.children[1], with_types) +")"

    def compile_while(self, node, builder, scope):
        for child in node.children:
            child.builder = builder

        with builder.if_then(self.compile_tree([node.children[0]])) as then:
            with then:
                i = self.compile_tree(node.children[1])
                builder.branch(builder.block)
        return i

    def compile_if(self, node, builder, scope):
        for child in node.children:
            child.builder = builder

        if len(node.children) == 3:
            with builder.if_else(self.compile_tree(node.children[0])) as (then, otherwise):
                with then:
                    i = self.compile_tree(node.children[1])

                with otherwise:
                    i = self.compile_tree(node.children[2])
        else:
            with builder.if_then(self.compile_tree(node.children[0])) as then:
                with then:
                    i = self.compile_tree(node.chilren[1])
        
        return i

    def print_formal(self, node, builder, scope):
        return self.compile_expression(node, 1)

    def compile_method(self, node, builder, scope):
        return 
    
    
    def print_field(self, node, with_types):
        if len(node.children) == 2:
            return "\nField(" + self.print_tree(node.children[0], 0) + ", " + node.type + ", " + self.print_tree(node.children[1], with_types) +")"
        return "\nField(" + self.print_tree(node.children[0], 0) + ", " + node.type +")"


    def compile_object(self):
        objectStruct = ir.Context().get_identified_type("struct.Object")
        objectVT = ir.Context().get_identified_type("struct.ObjectVT")

        # Set Object structure body
        objectStruct.set_body(*[objectVT.as_pointer()])

        # Type of methods in Object VT
        typePrint = ir.FunctionType(objectStruct.as_pointer(), [objectStruct.as_pointer(), self.types['string']])
        typePrintBool = ir.FunctionType(objectStruct.as_pointer(), [objectStruct.as_pointer(), self.types['bool']])
        typePrintInt32 = ir.FunctionType(objectStruct.as_pointer(), [objectStruct.as_pointer(), self.types['int32']])
        typeInputLine = ir.FunctionType(self.types['string'], [objectStruct.as_pointer()])
        typeInputBool = ir.FunctionType(self.types['bool'], [objectStruct.as_pointer()])
        typeInputInt32 = ir.FunctionType(self.types['int32'], [objectStruct.as_pointer()])


        # Methods of Object
        objectPrint = ir.Function(self.module, typePrint, name="Object__print")
        objectPrintBool = ir.Function(self.module, typePrintBool, name="Object__printBool")
        objectPrintInt32 = ir.Function(self.module, typePrintInt32, name="Object__printint32")
        objectInputLine= ir.Function(self.module, typeInputLine, name="Object__inputLine")
        objectInputBool= ir.Function(self.module, typeInputBool, name="Object__inputBool")
        objectInputInt32= ir.Function(self.module, typeInputInt32, name="Object__inputInt32")

        objectVTbody = [typePrint.as_pointer(), typePrintBool.as_pointer(), typePrintInt32.as_pointer(), typeInputLine.as_pointer(), typeInputBool.as_pointer(), 
                        typeInputInt32.as_pointer()]        
        objectVT.set_body(*objectVTbody)


        self.dict['Object']['struct'] = objectStruct.as_pointer()
        self.dict['Object']['VTstruct'] = objectVT

        self.dict['Object']['fields'] = {}

        self.dict['Object']['methods'] = {
            'print' : [typePrint, objectPrint],
            'printBool' : [typePrintBool, objectPrintBool],
            'printInt32' : [typePrintInt32, objectPrintInt32],
            'inputLine' : [typeInputLine, objectInputLine],
            'inputBool': [typeInputBool, objectInputBool],
            'inputInt32' : [typeInputInt32, objectInputInt32]
        }

        newType = ir.FunctionType(objectStruct.as_pointer(), [])
        self.dict['Object']['new'] = ir.Function(self.module, newType, name='Object__new')
        initType = ir.FunctionType(objectStruct.as_pointer(), [objectStruct.as_pointer()])
        self.dict['Object']['init'] = ir.Function(self.module, initType, name="Object__init")


    def compile_class(self, class_name):
        classStruct = ir.Context().get_identified_type("struct."+class_name)
        classVT = ir.Context().get_identified_type("struct."+class_name+"VT")

        # Set class structure body
        classBody = [classVT.as_pointer()]
        classVTbody = []
        classMethods = []

        # Deep copy from parent class
        self.dict[class_name] = self.dict[self.extends[class_name]].copy()
        self.dict[class_name]['methods'].update(self.dict[self.extends[class_name]]['methods'].copy())
        self.dict[class_name]['fields'].update(self.dict[self.extends[class_name]]['fields'].copy())

        # for key in self.dict[self.extends[class_name]]['fields'].keys():
        #     self.dict[class_name]['fields'][key] = self.dict[self.extends[class_name]]['fields'][key].copy()
        #     classBody.append(self.dict[self.extends[class_name]]['fields'][key][1].copy())

        for key in self.dict[self.extends[class_name]]['methods'].keys():
            self.dict[class_name]['methods'][key] = self.dict[self.extends[class_name]]['methods'][key].copy()
            #classVTbody.append(self.dict[self.extends[class_name]]['methods'][key][0])

        # Set class methods inside dictionary and classVT body list
        if len(self.methods_dict[class_name]) == 0:
            self.dict[class_name]['methods'] = {}
        else:
            for method in self.methods_dict[class_name]:
                if method[1] in self.types:
                    returnType = self.types[method[1]]
                else:
                    returnType = self.dict[method[1]]['struct']

                argsType  = [classStruct.as_pointer()]
                for arg in self.formals_dict[(class_name, method[0])]:
                    if arg[1] in self.types:
                        argsType.append(self.types[arg[1]])
                    else:
                        argsType.append(self.dict[arg[1]]['struct'])
                
                typeMethod = ir.FunctionType(returnType.as_pointer(), argsType)
                if method[0] == "main":
                    classMethod = ir.Function(self.module, typeMethod, name="main")
                else:
                    classMethod = ir.Function(self.module, typeMethod, name=class_name+"__"+method[0])

                classVTbody.append(typeMethod.as_pointer())
                classMethods.append(classMethod)
                self.dict[class_name]['methods'].update({method[0] : [typeMethod, classMethod]})

        # Set class fields in dictionary
        if len(self.fields_dict[class_name]) == 0:
            self.dict['Object']['fields'] = {}
        else:
            for field in self.fields_dict[class_name]:
                if field[1] in self.types:
                    fieldType = self.types[field[1]]
                else:
                    fieldType = self.dict[field[1]]['struct']
                classBody.append(fieldType)
                self.dict[class_name]["fields"].update({field[0] : fieldType})

        # Set class VT body and class structure body
        classVT.set_body(*classVTbody)
        classStruct.set_body(*classBody)

        # Set structure and VT structure in dictionary
        self.dict[class_name]['struct'] = classStruct.as_pointer()
        self.dict[class_name]['VTstruct'] = classVT


        # New and Init functions
        newType = ir.FunctionType(classStruct.as_pointer(), [])
        newFct = ir.Function(self.module, newType, name=class_name+'_new')
        self.dict[class_name]['new'] = newFct
        initType = ir.FunctionType(classStruct.as_pointer(), [classStruct.as_pointer()])
        initFct = ir.Function(self.module, initType, name=class_name+'_init')
        self.dict[class_name]['init'] = initFct


        # New initialization and block builder
        block = newFct.append_basic_block()
        builder = ir.IRBuilder(block)

        nullSize = ir.Constant(self.dict[class_name]['struct'], None)
        sizePtr = builder.gep(nullSize, [self.types["int32"](1)], inbounds=False, name="size_ptr")
        sizeI64 = builder.ptrtoint(sizePtr, ir.IntType(64), name="size_i64")

        mallocPtr = builder.call(self.malloc, [sizeI64])
        cast = builder.bitcast(mallocPtr, self.dict[class_name]['struct'])
        ret_val = builder.call(initFct, [cast])
        builder.ret(ret_val)

        # Init initialization and block builder
        block = initFct.append_basic_block()
        builder = ir.IRBuilder(block)

        arg = initFct.args[0]
        with builder.if_then(builder.icmp_unsigned('!=', arg, nullSize)):

            # .super function from parent
            cast = builder.bitcast(arg, self.dict[self.extends[class_name]]['struct'])
            call = builder.call(self.dict[self.extends[class_name]]['init'], [cast])

            # Vtable
            ptr = builder.gep(arg, [self.types['int32'](0), self.types['int32'](0)], inbounds=True)
            value = ir.Constant(self.dict[class_name]['VTstruct'], classMethods)
            classVTable = ir.GlobalVariable(self.module, self.dict[class_name]['VTstruct'], name=class_name+'_vtable')
            classVTable.global_constant = True
            classVTable.initializer = value
            builder.store(classVTable, ptr)
        
            # Initialize fields

            # Get parent's fields number
            l = len(self.dict[self.extends[class_name]]['fields']) + 1
            for child in self.tree.children:
                if child.values[0] == class_name:
                    classNode = child

            for i, field in enumerate(classNode.children[0].children):

                fieldPtr = builder.gep(arg, [self.types['int32'](0), self.types['int32'](l+i)])
                if len(field.children) == 2:

                    # Recovers value in tree if assign
                    value = self.compile_tree(field.children[1], builder, variableScope())
                    ldPtr = builder.load(fieldPtr)
                    cast = builder.bitcast(value, ldPtr.type)
                    builder.store(cast, fieldPtr)
                
                else:
                    if field.type == 'int32':
                        builder.store(self.types['int32'](0), fieldPtr)
                    
                    elif field.type == 'bool':
                        builder.store(self.types['bool'](0), fieldPtr)
                    
                    elif field.type == 'string':
                        cst = ir.Constant(ir.ArrayType(ir.IntType(8), len(chr(0))), bytearray(chr(0).encode('utf8')))
                        globalStr = ir.GlobalVariable(self.module, cst.type, self.module.get_unique_name('string'))
                        globalStr.global_constant = True
                        globalStr.initializer = cst

                        strPtr = builder.gep(globalStr, [self.types['int32'](0), self.types['int32'](0)], inbounds=True)
                        builder.store(strPtr, fieldPtr)
                    
                    else:
                        nullPtr = ir.Constant(self.dict[class_name]['fields'][field.children[0].values[0]][0], None)
                        builder.store(nullPtr, fieldPtr)

        builder.ret(arg)


    def compile_main(self, node):
        scope = variableScope()
        block = self.dict["Main"]["methods"]["main"][1].append_basic_block(name="entry")
        builder = ir.IRBuilder(block)
        
        main = builder.call(self.dict['Main']['new'], [])
        args = self.dict["Main"]["methods"]["main"][1].args
        ptr = builder.alloca(args[0].type)
        builder.store(main, ptr)

        scope.addVariable('self', ptr)
        builder.ret(self.compile_tree(node.children[2], builder, scope))


    def compile_program(self, node):
        for child in node.children:
            if child.values[0] == "Main":
                self.compile_main(child.children[1].children[0])


    def compile_extends(self, class_name):
        if self.extends[class_name] not in self.dict:
            self.compile_extends(self.extends[class_name])

        elif class_name not in self.dict:
            self.compile_class(class_name)


    def compile_classes(self):
        for class_name in self.extends:
            while self.extends[class_name] not in self.dict:
                self.compile_extends(class_name)
            
            if class_name not in self.dict:
                self.compile_class(class_name)





