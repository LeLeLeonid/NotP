from parser import Parser

class Compiler:
    def __init__(self):
        self.bytecode = []

    def compile(self, ast):
        cmd = ast[0]
        if cmd == "print":
            self.bytecode.append(("PRINT",))
            expr = ast[1]
            if expr[0] == "add":
                self.bytecode.append(("ADD", expr[1], expr[2]))

    def run(self):
        for instruction in self.bytecode:
            if instruction[0] == "PRINT":
                pass
            elif instruction[0] == "ADD":
                print(instruction[1] + instruction[2])