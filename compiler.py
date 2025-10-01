class Compiler:
    def __init__(self):
        self.bytecode = []

    def compile(self, ast):
        cmd = ast[0]

        if cmd == "program":
            for stmt in ast[1]:
                self.compile(stmt)

        elif cmd == "assign":
            var_name = ast[1]
            self.compile(ast[2])
            self.bytecode.append(("STORE", var_name))

        elif cmd == "print":
            self.compile(ast[1])
            self.bytecode.append(("PRINT",))

        elif cmd == "number":
            self.bytecode.append(("LOAD_CONST", ast[1]))

        elif cmd == "string":
            self.bytecode.append(("LOAD_CONST", ast[1]))

        elif cmd == "variable":
            self.bytecode.append(("LOAD_VAR", ast[1]))

        elif cmd == "add":
            self.compile(ast[1])
            self.compile(ast[2])
            self.bytecode.append(("BINARY_ADD",))

        elif cmd == "sub":
            self.compile(ast[1])
            self.compile(ast[2])
            self.bytecode.append(("BINARY_SUB",))

        elif cmd == "mult":
            self.compile(ast[1])
            self.compile(ast[2])
            self.bytecode.append(("BINARY_MUL",))

        elif cmd == "div":
            self.compile(ast[1])
            self.compile(ast[2])
            self.bytecode.append(("BINARY_DIV",))

        elif cmd == "eq":
            self.compile(ast[1])
            self.compile(ast[2])
            self.bytecode.append(("BINARY_EQ",))

        elif cmd == "lt":
            self.compile(ast[1])
            self.compile(ast[2])
            self.bytecode.append(("BINARY_LT",))

        elif cmd == "gt":
            self.compile(ast[1])
            self.compile(ast[2])
            self.bytecode.append(("BINARY_GT",))

        elif cmd == "block":
            for stmt in ast[1]:
                self.compile(stmt)

        elif cmd == "if":
            self.compile(ast[1])
            pos = len(self.bytecode)
            self.bytecode.append(("JUMP_IF_FALSE", 0))
            self.compile(ast[2])
            self.bytecode[pos] = ("JUMP_IF_FALSE", len(self.bytecode) + 1)
            if ast[3]:
                self.compile(ast[3])

        elif cmd == "while":
            start = len(self.bytecode)
            self.compile(ast[1])
            pos = len(self.bytecode)
            self.bytecode.append(("JUMP_IF_FALSE", 0))
            self.compile(ast[2])
            self.bytecode.append(("JUMP", start))
            self.bytecode[pos] = ("JUMP_IF_FALSE", len(self.bytecode))

    def run(self):
        stack = []
        variables = {}
        ip = 0
        while ip < len(self.bytecode):
            op, *args = self.bytecode[ip]
            if op == "LOAD_CONST":
                stack.append(args[0])
            elif op == "LOAD_VAR":
                name = args[0]
                stack.append(variables[name])
            elif op == "STORE":
                value = stack.pop()
                name = args[0]
                variables[name] = value
            elif op == "BINARY_ADD":
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            elif op == "BINARY_SUB":
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
            elif op == "BINARY_MUL":
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
            elif op == "BINARY_DIV":
                b = stack.pop()
                a = stack.pop()
                stack.append(a // b)
            elif op == "BINARY_EQ":
                b = stack.pop()
                a = stack.pop()
                stack.append(a == b)
            elif op == "BINARY_LT":
                b = stack.pop()
                a = stack.pop()
                stack.append(a < b)
            elif op == "BINARY_GT":
                b = stack.pop()
                a = stack.pop()
                stack.append(a > b)
            elif op == "PRINT":
                print(stack.pop())
            elif op == "JUMP_IF_FALSE":
                value = stack.pop()
                if not value:
                    ip = args[0] - 1
            elif op == "JUMP":
                ip = args[0] - 1
            ip += 1