from lexer import lexer
from parser import Parser
from compiler import Compiler
from interpreter import interpret

def main():
    with open("examples/example1.notp") as f:
        code = f.read()
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()
    interpret(ast)

if __name__ == "__main__":
    main()
