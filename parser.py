from lexer import lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        
    def peek(self):
        while self.position < len(self.tokens):
            token = self.tokens[self.position]
            if token[0] != "NEWLINE":
                return token
            self.position += 1
        return None
        
    def consume(self, expected_type=None):
        while self.position < len(self.tokens):
            token = self.tokens[self.position]
            if token[0] != "NEWLINE":
                if expected_type and token[0] != expected_type:
                    raise RuntimeError(f"Expected {expected_type} but found {token[0]}")
                self.position += 1
                return token
            self.position += 1
        if expected_type:
            raise RuntimeError(f"Expected token {expected_type} but found end of input")
        return None
        
    def parse(self):
        statements = []
        while self.peek() is not None:
            stmt = self.parse_statement()
            statements.append(stmt)
        return ("program", statements)
    
    def parse_statement(self):
        token = self.peek()
        if token[0] == "PRINT":
            return self.parse_print()
        elif token[0] == "FUNC":
            return self.parse_function_declaration()
        elif token[0] == "IF":
            return self.parse_if_statement()
        elif token[0] == "WHILE":
            return self.parse_while_statement()
        elif token[0] == "RETURN":
            return self.parse_return_statement()
        elif token[0] == "ID":
            next_token = self.tokens[self.position + 1] if self.position + 1 < len(self.tokens) else None
            if next_token and next_token[0] == "ASSIGN":
                return self.parse_assignment()
            else:
                return self.parse_expression()
        else:
            return self.parse_expression()
     
    def parse_assignment(self):
        var_name = self.consume("ID")[1]
        self.consume("ASSIGN")
        expr = self.parse_expression()
        return ("assign", var_name, expr)
        
    def parse_print(self):
        self.consume("PRINT")
        self.consume("LPAREN")
        expr = self.parse_expression()
        self.consume("RPAREN")
        return ("print", expr)
    
    def parse_function_declaration(self):
        self.consume("FUNC")
        name = self.consume("ID")[1]
        self.consume("LPAREN")
        self.consume("RPAREN")
        body = self.parse_block()
        return ("function", name, [], body)
        
    def parse_if_statement(self):
        self.consume("IF")
        self.consume("LPAREN")
        condition = self.parse_expression()
        self.consume("RPAREN")
        then_branch = self.parse_block()
        else_branch = None
        if self.peek() and self.peek()[0] == "ELSE":
            self.consume("ELSE")
            else_branch = self.parse_block()
        return ("if", condition, then_branch, else_branch)
    
    def parse_while_statement(self):
        self.consume("WHILE")
        self.consume("LPAREN")
        condition = self.parse_expression()
        self.consume("RPAREN")
        body = self.parse_block()
        return ("while", condition, body)
    
    def parse_return_statement(self):
        self.consume("RETURN")
        expr = self.parse_expression()
        return ("return", expr)

    def parse_block(self):
        statements = []
        self.consume("LBRACE")
        while self.peek() and self.peek()[0] != "RBRACE":
            stmt = self.parse_statement()
            statements.append(stmt)
        self.consume("RBRACE")
        return ("block", statements)
        
    def parse_expression(self):
        left = self.parse_comparison()
        while self.peek() and self.peek()[0] in ("PLUS", "MINUS"):
            op = self.consume()
            op_name = {"PLUS": "add", "MINUS": "sub"}[op[0]]
            right = self.parse_comparison()
            left = (op_name, left, right)
        return left
        
    def parse_term(self):
        left = self.parse_factor()
        while self.peek() and self.peek()[0] in ("MULT", "DIV"):
            op = self.consume()
            op_name = {"MULT": "mult", "DIV": "div"}[op[0]]
            right = self.parse_factor()
            left = (op_name, left, right)
        return left
        
    def parse_comparison(self):
        left = self.parse_term()
        if self.peek() and self.peek()[0] in ("EQ","NE","LT","GT","LE","GE"):
            op = self.consume()
            right = self.parse_term()
            return (op[0].lower(), left, right)
        return left
        
    def parse_factor(self):
        token = self.peek()
        if token[0] == "NUMBER":
            return ("number", int(self.consume("NUMBER")[1]))
        elif token[0] == "STRING":
            return ("string", self.consume("STRING")[1][1:-1])
        elif token[0] == "ID":
            next_token = self.tokens[self.position + 1] if self.position + 1 < len(self.tokens) else None
            if next_token and next_token[0] == "LPAREN":
                return self.parse_function_call()
            else:
                return ("variable", self.consume("ID")[1])
        elif token[0] == "LPAREN":
            self.consume("LPAREN")
            expr = self.parse_expression()
            self.consume("RPAREN")
            return expr
        else:
            raise RuntimeError(f"Unexpected token in term: {token}")
    
    def parse_function_call(self):
        name = self.consume("ID")[1]
        self.consume("LPAREN")
        args = []
        if self.peek() and self.peek()[0] != "RPAREN":
            args.append(self.parse_expression())
            while self.peek() and self.peek()[0] == "COMMA":
                self.consume("COMMA")
                args.append(self.parse_expression())
        self.consume("RPAREN")
        return ("call", name, args)