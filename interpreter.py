from parser import Parser

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