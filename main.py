import sys
from lexer import lexer
from parser import Parser
from compiler import Compiler
from interpreter import interpret

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename> [--vm]")
        return

    filepath = sys.argv[1]
    
    use_vm = len(sys.argv) > 2 and sys.argv[2] == "--vm"

    try:
        with open(filepath) as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        return
    
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()

    if use_vm:
        print("--- Running on VM ---")
        compiler = Compiler()
        compiler.compile(ast)
        #print("AST: ", ast)
        compiler.run()
    else:
        print("--- Running with Interpreter ---")
        interpret(ast)

if __name__ == "__main__":
    main()
