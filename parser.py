from lexer import lexer

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