from llvmlite import ir, binding
import sys

class CodeGen():

    def __init__(self):
        self.binding = binding
        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_all_asmprinters()
        self._create_execution_engine()
        self._compile_ir()
        self.module.triple = self.binding.get_default_triple()


    # Declare Object and other class functions here for simplicity

    def save_ir(self, filename):
        with open(filename, "w") as output:
            output.write(str(self.module))

    def print_ir(self,module):
        ir_str = self._add_object(module)
        sys.stdout.write(ir_str)

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
        

def add_object():
    filename = "object.ll"
    output = ""
    with open(filename) as f:
        content = f.readlines()
    
    for line in content:
        output += line

    return output



