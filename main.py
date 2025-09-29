import re

TOKEN_SPEC = [("NUMBER", r"\d+"),("PRINT", r"print"),("PLUS", r"\+"),("LPAREN", r"\("),("RPAREN", r"\)"),("SKIP", r"[ \t]+"),("MISMATCH", r"."),]

def lexer(code):
    
    tokens = []
    index = 0
    while index < len(code):
        for token_type, pattern in TOKEN_SPEC:
            regex = re.compile(pattern)
            match = regex.match(code, index)
            if match:
                text = match.group(0)
                if token_type != "SKIP":
                    if token_type == "MISMATCH":
                        raise RuntimeError(f"Unexpected character: {text}")
                    tokens.append((token_type, text))
                index = match.end(0)
                break
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        else:
            return None

    def consume(self, expected_type=None):
        current = self.peek()
        if current is None:
            raise RuntimeError(f"Expected token {expected_type} but got {current[0]}")
        self.position += 1
        return current
    def parse(self):
        token = self.consume("PRINT")
        self.consume("LPAREN")
        left = self.consume("NUMBER")
        op = self.consume("PLUS")
        right = self.consume("NUMBER")
        self.consume("RPAREN")
        return ("print", ("add", int(left[1]), int(right[1])))

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


code = input("Enter NotP code >>> ")
tokens = lexer(code)

parser = Parser(tokens)
ast = parser.parse()
# print("RAW AST:", ast)

def interpret(ast):
    command = ast[0]
    if command == "print":
        operation = ast[1]
        if operation[0] == "add":
            left = operation[1]
            right = operation[2]
            #print(left+right)
        else:
            raise RuntimeError("Unknown operation")
    else:
        raise RuntimeError("Unknown command")

interpret(ast)

compiler = Compiler()
compiler.compile(ast)
compiler.run()
