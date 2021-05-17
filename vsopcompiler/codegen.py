import sys, os
from llvmlite import ir, binding
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
        self.pow = None
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

        self.classes = {'Object': {}}
        self.compile_object()
        self.compile_classes()
        self.compile_program(self.tree)

    def save_ir(self, filename):
        result = str(self.module).split('\n', 3)[3]
        object_ll = object.getObject()
        result = object_ll + result
        output_file = open(filename + '.ll', 'w')
        output_file.write(result)
        output_file.close()
        #compile locally with llc-11
        os.system('llc ' + filename + '.ll')
        os.system('clang ' + filename + '.s -lm -o ' + filename) 

    def print_ir(self): 
        result = str(self.module).split('\n', 3)[3]
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
            "new type": self.compile_new_type,
            "call": self.compile_call,
            "binop": self.compile_binop,
            "unop": self.compile_unop,
            "assign": self.compile_assign,
            "let": self.compile_let,
            "while": self.compile_while,
            "if": self.compile_if,
            "block": self.compile_block,
            "class" : self.compile_class_inside
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

        if node.name == "self":
            ptr = scope.getValue(node.node_class)
            return builder.load(ptr)

        if node.name == "object identifier":
            ptr = scope.getValue(node.values[0])
            if ptr is not None:
                value = builder.load(ptr)
            else:
                field = self.classes[node.node_class]['fields'].get(node.values[0])
                selfPtr = scope.getValue(node.node_class)
                ld = builder.load(selfPtr)
                fctType = builder.gep(ld, [self.types['int32'](0), self.types['int32'](field[0])], inbounds=True)
                value = builder.load(fctType)
            return value
        
    def compile_class_inside(self, node, builder, scope):
        for method in node.children[1].children:
            fct = self.classes[node.values[0]]['methods'][method.children[0].values[0]][2]
            block = fct.append_basic_block()
            builder = ir.IRBuilder(block)
            self.compile_tree(method, builder, scope)


    def compile_block(self, node, builder, scope):
        scope.addScope()

        for child in node.children:
            i =  self.compile_tree(child, builder, scope)
        
        scope.removeScope()
        return i

    def compile_new_type(self, node, builder, scope):
        return builder.call(self.classes[node.values[0]]['new'], [])

    def compile_args(self, node, builder, scope):
        args = []
        for child in node.children:
            arg = self.compile_tree(child, builder, scope)
            args.append(arg)
        return args

    def compile_call(self, node, builder, scope):

        class_name = node.children[0].type
        method_name = node.children[1].values[0]
        method = self.classes[class_name]["methods"][method_name]

        # Recover self argument and function arguments casts
        value = self.compile_tree(node.children[0], builder, scope)
        vTablePtr = builder.gep(value, [self.types['int32'](0), self.types['int32'](0)], inbounds=True)
        vtbl = builder.load(vTablePtr)

        # Recover function from VT and its arguments
        fctPtr = builder.gep(vtbl, [self.types['int32'](0), self.types['int32'](method[0])], inbounds=True)
        fct = builder.load(fctPtr)
        args = self.compile_args(node.children[2], builder, scope)

        cast = builder.bitcast(value, method[2].args[0].type)
        fct_args = [cast]
        for i, arg in enumerate(args):
            cast = builder.bitcast(arg, method[2].args[i+1].type)
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

    def compile_pow(self, node, builder, scope):
        args = []
        # Convert int21 to double
        args.append(builder.uitofp(self.compile_tree(node.children[0], builder, scope), ir.DoubleType()))
        args.append(builder.uitofp(self.compile_tree(node.children[1], builder, scope), ir.DoubleType()))
        # Call pow function
        if self.pow is None:
            powType = ir.FunctionType(ir.DoubleType(), [ir.DoubleType(), ir.DoubleType()])
            self.pow = ir.Function(self.module, powType, name="pow")

        call = builder.call(self.pow, args)
        # Return value after conversion to int32
        return builder.fptoui(call, self.types['int32'])

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
        return builder.not_(self.compile_tree(node.children[0], builder, scope))

    def compile_minus(self, node, builder, scope):
        return builder.neg(self.compile_tree(node.children[0], builder, scope))

    def compile_isnull(self, node, builder, scope):
        typeNull = ir.Constant(self.classes[node.node_class]['pointer'], None)
        return  builder.icmp_unsigned('==', self.compile_tree(node.children[0], builder, scope), typeNull)

    def compile_unop(self, node, builder, scope):
        switcher = {
            "not" : self.compile_not(node, builder, scope),
            "-": self.compile_minus(node, builder, scope),
            "isnull": self.compile_isnull(node, builder, scope)
            }
        return switcher[node.values[0]](node, builder, scope)
        

    def compile_assign(self, node, builder, scope):
        
        if node.type in self.types:
            returnType = self.types[node.type]
        else:
            returnType = self.classes[node.type]['pointer']

        val = self.compile_tree(node.children[1], builder, scope)

        # Store if argument
        ptr = scope.getValue(node.children[0].values[0])
        if ptr is not None:
            cast = builder.bitcast(val, returnType)
            builder.store(cast, ptr)

        # If field
        else:
            field = self.classes[node.node_class]['fields'][node.children[0].values[0]]
            selfPtr = scope.getValue(node.node_class)
            ld = builder.load(selfPtr)
            fieldPtr = builder.gep(ld, [self.types['int32'](0), self.types['int32'](field[0])], inbounds=True)
            cast = builder.bitcast(val, field[1])
            builder.store(cast, fieldPtr)

        return val 

    def compile_let(self, node, builder, scope):
        
        # Get type of object identifier in let
        if node.children[0].type in self.types:
            returnType = self.types[node.children[0].type]
        else:
            returnType = self.classes[node.type]['pointer']

        ptr = builder.alloca(returnType)

        if len(node.children) == 2: 
            # Initialize variable with default one
            if node.type == "int32":
                builder.store(self.types['int32'](0), ptr)
            
            elif node.type == "bool":
                builder.store(self.types['bool'](0), ptr)
            
            elif node.type == "string":
                cst = ir.Constant(ir.ArrayType(ir.IntType(8), len(chr(0))), bytearray(chr(0).encode('utf8')))
                globalStr = ir.GlobalVariable(self.module, cst.type, self.module.get_unique_name('string'))
                globalStr.global_constant = True
                globalStr.initializer = cst
                builder.store(globalStr, ptr)
            
            else:
                # Initialize to null at default 
                null = ir.Constant(returnType, None)
                builder.store(null, ptr)
        
        else:
            # Initialize variable with expression (assign)
            val = self.compile_tree(node.children[1], builder, scope)
            cast = builder.bitcast(val, returnType)
            builder.store(cast, ptr)
        
        scope.addScope()
        scope.addVariable(node.children[0].values[0],ptr)

        # Compile inside the let
        if len(node.children) == 2:
            insideLet = self.compile_tree(node.children[1], builder, scope)
        else:
            insideLet = self.compile_tree(node.children[2], builder, scope)
        
        scope.removeScope()
        return insideLet
            

    def compile_while(self, node, builder, scope):

        whileCond = builder.function.append_basic_block(name='while_cond')
        whileBod = builder.function.append_basic_block(name='while_body')
        whileExit = builder.funciton.append_basic_block(name='while_exit')

        
        # Block for condition
        builder.branch(whileCond)
        builder.position_at_end(whileCond)

        # Branch to right block
        cond = self.compile_tree(node.children[0], builder, scope)
        builder.cbranch(cond, whileBod, whileExit)

        # Block for block entry
        builder.position_at_end(whileBod)
        builder.branch(cond)

        # Block for end of while (no need to branch)
        builder.position_at_end(whileExit)
        
        return self.types['unit']

    def compile_if(self, node, builder, scope):

        if len(node.children) == 3:

            if node.type in self.types:
                ifType = self.types[node.type]
            else:
                ifType = self.classes[node.type]['pointer']
            ptr = builder.alloca(ifType)
             
            with builder.if_else(self.compile_tree(node.children[0], builder, scope)) as (then, otherwise):
                with then:
                    iThen = self.compile_tree(node.children[1], builder, scope)
                    cast = builder.bitcast(iThen, ifType)
                    # Store result in case then
                    builder.store(cast, ptr)

                with otherwise:
                    iElse = self.compile_tree(node.children[2], builder, scope)
                    cast = builder.bitcast(iElse, ifType)
                    # Store result in case else
                    builder.store(cast, ptr)
            return builder.load(ptr)

        else:
            with builder.if_then(self.compile_tree(node.children[0], builder, scope)):
                i = self.compile_tree(node.chilren[1], builder, scope)
                # If only then, return void
                i = self.types['unit']
            return i


    def compile_method(self, node):
        # Create new scope and builder
        scope = variableScope()
        block = self.classes[node.node_class]["methods"][node.children[0].values[0]][2].append_basic_block()
        builder = ir.IRBuilder(block)

        # Allocate memory for 'self'
        args = self.classes[node.node_class]['methods'][node.children[0].values[0]][2].args
        ptr = builder.alloca(args[0].type)
        builder.store(args[0], ptr)
        scope.addVariable(node.node_class, ptr)

        # Allocate memory for every argument
        for i, formal in enumerate(node.children[1].children):
            ptr = builder.alloca(args[i+1].type)
            builder.store(args[i+1], ptr)
            scope.addVariable(formal.values[0], ptr)

        # Compile body of the method
        retVal = self.compile_tree(node.children[2], builder, scope)
        if retVal == self.types['unit']:
            builder.ret_void()
        else:
            builder.ret(retVal)
    


    def compile_object(self):
        objModule = ir.Module(name='objModule')

        objectPointer = ir.Context().get_identified_type("Object")
        objectVT = ir.Context().get_identified_type("ObjectVTable")

        # Set Object structure body
        objectPointer.set_body(*[objectVT.as_pointer()])

        # C malloc function declaration
        mallocType = ir.FunctionType(ir.IntType(8).as_pointer(), [ir.IntType(64)])
        self.malloc = ir.Function(objModule, mallocType, name='malloc')

        # Type of methods in Object VT
        typePrint = ir.FunctionType(objectPointer.as_pointer(), [objectPointer.as_pointer(), self.types['string']])
        typePrintBool = ir.FunctionType(objectPointer.as_pointer(), [objectPointer.as_pointer(), self.types['bool']])
        typePrintInt32 = ir.FunctionType(objectPointer.as_pointer(), [objectPointer.as_pointer(), self.types['int32']])
        typeInputLine = ir.FunctionType(self.types['string'], [objectPointer.as_pointer()])
        typeInputBool = ir.FunctionType(self.types['bool'], [objectPointer.as_pointer()])
        typeInputInt32 = ir.FunctionType(self.types['int32'], [objectPointer.as_pointer()])


        # Methods of Object
        objectPrint = ir.Function(objModule, typePrint, name="Object__print")
        objectPrintBool = ir.Function(objModule, typePrintBool, name="Object__printBool")
        objectPrintInt32 = ir.Function(objModule, typePrintInt32, name="Object__printInt32")
        objectInputLine= ir.Function(objModule, typeInputLine, name="Object__inputLine")
        objectInputBool= ir.Function(objModule, typeInputBool, name="Object__inputBool")
        objectInputInt32= ir.Function(objModule, typeInputInt32, name="Object__inputInt32")

        objectVTbody = [typePrint.as_pointer(), typePrintBool.as_pointer(), typePrintInt32.as_pointer(), typeInputLine.as_pointer(), typeInputBool.as_pointer(), 
                        typeInputInt32.as_pointer()]        
        objectVT.set_body(*objectVTbody)


        self.classes['Object']['pointer'] = objectPointer.as_pointer()
        self.classes['Object']['VTable'] = objectVT

        self.classes['Object']['fields'] = {}

        self.classes['Object']['methods'] = {
            'print' : [0, typePrint, objectPrint],
            'printBool' : [1, typePrintBool, objectPrintBool],
            'printInt32' : [2, typePrintInt32, objectPrintInt32],
            'inputLine' : [3, typeInputLine, objectInputLine],
            'inputBool': [4, typeInputBool, objectInputBool],
            'inputInt32' : [5, typeInputInt32, objectInputInt32]
        }

        newType = ir.FunctionType(objectPointer.as_pointer(), [])
        self.classes['Object']['new'] = ir.Function(objModule, newType, name='Object___new')
        initType = ir.FunctionType(objectPointer.as_pointer(), [objectPointer.as_pointer()])
        self.classes['Object']['init'] = ir.Function(objModule, initType, name="Object___init")


    def compile_class(self, class_name):
        classPointer = ir.global_context.get_identified_type(class_name)
        classVT = ir.global_context.get_identified_type(class_name+"VT")

        # Set class structure body
        classBody = [classVT.as_pointer()]

        # Deep copy from parent class
        # Be careful ! Not update to avoid linking between dictionaries
        self.classes[class_name] = self.classes[self.extends[class_name]].copy()
        self.classes[class_name]['methods'] = self.classes[self.extends[class_name]]['methods'].copy()
        self.classes[class_name]['fields'] = self.classes[self.extends[class_name]]['fields'].copy()

        for field in self.classes[self.extends[class_name]]['fields'].keys():
             self.classes[class_name]['fields'][field] = self.classes[self.extends[class_name]]['fields'][field].copy()

        for method in self.classes[self.extends[class_name]]['methods'].keys():
            self.classes[class_name]['methods'][method] = self.classes[self.extends[class_name]]['methods'][method].copy()


        # Get field and method number in parent
        nbMethod = len(self.classes[class_name]['methods'])
        nbFields = len(self.classes[class_name]['fields']) + 1

        # Set class methods inside dictionary and classVT body list
        for method in self.methods_dict[class_name]:
            if method[1] in self.types:
                returnType = self.types[method[1]]
            else:
                returnType = self.classes[method[1]]['pointer']

            argsType  = [classPointer.as_pointer()]
            for arg in self.formals_dict[(class_name, method[0])]:
                if arg[1] in self.types:
                    argsType.append(self.types[arg[1]])
                else:
                    argsType.append(self.classes[arg[1]]['pointer'])
            
            typeMethod = ir.FunctionType(returnType, argsType)
            if method[0] == "main":
                methodFct = ir.Function(self.module, typeMethod, name="main")
            else:
                methodFct = ir.Function(self.module, typeMethod, name=class_name+"__"+method[0])

            methodObj = self.classes[class_name]['methods'].get(method[0])
            # Override if method already exists
            if methodObj is not None:
                self.classes[class_name]['methods'][method[0]] = [methodObj[0], typeMethod, methodFct]
            else:
                self.classes[class_name]['methods'][method[0]] = [nbMethod, typeMethod, methodFct]
                nbMethod += 1

        classVTbody = [None] * len(self.classes[class_name]['methods'])
        classMethods = [None] * len(self.classes[class_name]['methods'])

        for method in self.classes[class_name]['methods'].items():
            classVTbody[method[1][0]] = method[1][1].as_pointer()
            classMethods[method[1][0]] =  method[1][2]

            
        # Set class fields in dictionary
        for field in self.fields_dict[class_name]:
            if field[1] in self.types:
                fieldType = self.types[field[1]]
            else:
                fieldType = self.classes[field[1]]['pointer']
            
            classBody.append(fieldType)
            self.classes[class_name]["fields"][field[0]] = [nbFields, fieldType]
            nbFields += 1
        

        # Set class VT body and class structure body
        classVT.set_body(*classVTbody)
        classPointer.set_body(*classBody)


        # Set structure and VT structure in dictionary
        self.classes[class_name]['pointer'] = classPointer.as_pointer()
        self.classes[class_name]['VTable'] = classVT


        # New and Init functions
        newType = ir.FunctionType(classPointer.as_pointer(), [])
        newFct = ir.Function(self.module, newType, name=class_name+'___new')
        self.classes[class_name]['new'] = newFct
        initType = ir.FunctionType(classPointer.as_pointer(), [classPointer.as_pointer()])
        initFct = ir.Function(self.module, initType, name=class_name+'___init')
        self.classes[class_name]['init'] = initFct


        # New initialization and block builder
        block = newFct.append_basic_block()
        builder = ir.IRBuilder(block)

        nullSize = ir.Constant(self.classes[class_name]['pointer'], None)
        sizePtr = builder.gep(nullSize, [self.types["int32"](1)], inbounds=False, name="size_ptr")
        sizeI64 = builder.ptrtoint(sizePtr, ir.IntType(64), name="size_i64")

        mallocPtr = builder.call(self.malloc, [sizeI64])
        cast = builder.bitcast(mallocPtr, self.classes[class_name]['pointer'])
        retVal = builder.call(initFct, [cast])
        builder.ret(retVal)

        # Init initialization and block builder
        block = initFct.append_basic_block()
        builder = ir.IRBuilder(block)

        arg = initFct.args[0]
        with builder.if_then(builder.icmp_unsigned('!=', arg, nullSize)):

            # .super function from parent
            cast = builder.bitcast(arg, self.classes[self.extends[class_name]]['pointer'])
            call = builder.call(self.classes[self.extends[class_name]]['init'], [cast])

            # Vtable
            ptr = builder.gep(arg, [self.types['int32'](0), self.types['int32'](0)], inbounds=True)
            value = ir.Constant(self.classes[class_name]['VTable'], classMethods)
            classVTable = ir.GlobalVariable(self.module, self.classes[class_name]['VTable'], name=class_name+'_vtable')
            classVTable.global_constant = True
            classVTable.initializer = value
            builder.store(classVTable, ptr)
        
            # Initialize fields

            # Get parent's fields number
            l = len(self.classes[self.extends[class_name]]['fields'])
            for child in self.tree.children:
                if child.values[0] == class_name:
                    classNode = child

            for i, field in enumerate(classNode.children[0].children):
                fieldPtr = builder.gep(arg, [self.types['int32'](0), self.types['int32'](l+i+1)])
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
                        nullPtr = ir.Constant(self.classes[class_name]['fields'][field.children[0].values[0]][1], None)
                        builder.store(nullPtr, fieldPtr)


        builder.ret(arg)


    def compile_main(self, node):
        for method in node.children:
            if method.children[0].values[0] == "main":
                scope = variableScope()
                block = self.classes["Main"]["methods"]["main"][2].append_basic_block()
                builder = ir.IRBuilder(block)
                
                main = builder.call(self.classes['Main']['new'], [])
                args = self.classes["Main"]["methods"]["main"][2].args
                ptr = builder.alloca(args[0].type)
                builder.store(main, ptr)

                scope.addVariable('Main', ptr)
                builder.ret(self.compile_tree(method.children[2], builder, scope))
            else:
                self.compile_method(method)


    def compile_program(self, node):
        for child in node.children:
            if child.values[0] == "Main":
                self.compile_main(child.children[1])
            else:
                for method in child.children[1]:
                    self.compile_method(method)


    def compile_extends(self, class_name):
        if self.extends[class_name] not in self.classes:
            self.compile_extends(self.extends[class_name])

        elif class_name not in self.classes:
            self.compile_class(class_name)


    def compile_classes(self):
        for class_name in self.extends:
            while self.extends[class_name] not in self.classes:
                self.compile_extends(class_name)
            
            if class_name not in self.classes:
                self.compile_class(class_name)





