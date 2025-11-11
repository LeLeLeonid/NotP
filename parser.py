from lexer import lexer


class Parser:
    """
    Parses a list of tokens into an Abstract Syntax Tree (AST).
    """
    def __init__(self, tokens):
        """Initializes the parser with a list of tokens."""
        self.tokens = tokens
        self.position = 0

    def peek(self):
        """
        Non-destructively looks at the next significant token.
        It skips over non-essential tokens like newlines and comments.
        This method does NOT advance the parser's position.
        """
        temp_pos = self.position
        while temp_pos < len(self.tokens):
            token = self.tokens[temp_pos]
            if token[0] not in ("NEWLINE", "COMMENT"):
                return token
            temp_pos += 1
        return None

    def consume(self, expected_type=None):
        """
        Consumes the next significant token, advancing the parser's position.
        """
        while self.position < len(self.tokens):
            token = self.tokens[self.position]
            self.position += 1
            if token[0] not in ("NEWLINE", "COMMENT"):
                if expected_type and token[0] != expected_type:
                    raise RuntimeError(f"Expected token {expected_type} but found {token[0]}")
                return token
        
        if expected_type:
            raise RuntimeError(f"Expected token {expected_type} but found end of input")
        return None

    def parse(self):
        """Parses the entire list of tokens into a program AST node."""
        statements = []
        while self.peek() is not None:
            statements.append(self.parse_statement())
        return ("program", statements)

    def parse_statement(self):
        """Parses a single statement based on the upcoming token."""
        token = self.peek()
        if not token:
            return None

        if token[0] == "PRINT":
            return self.parse_print_statement()
        elif token[0] == "IF":
            return self.parse_if_statement()
        elif token[0] == "WHILE":
            return self.parse_while_statement()
        elif token[0] == "FUNC":
            return self.parse_function_declaration()
        elif token[0] == "RETURN":
            return self.parse_return_statement()
        elif token[0] == "ID":
            if self._peek_next_significant()[0] == "ASSIGN":
                return self.parse_assignment_statement()
            else:
                return ("expression_statement", self.parse_expression())
        else:
            raise RuntimeError(f"Unexpected statement starting with token: {token}")

    def parse_print_statement(self):
        """Parses a print statement: print(...)"""
        self.consume("PRINT")
        self.consume("LPAREN")
        expr = self.parse_expression()
        self.consume("RPAREN")
        return ("print", expr)

    def parse_assignment_statement(self):
        """Parses an assignment statement: ID = ..."""
        var_name = self.consume("ID")[1]
        self.consume("ASSIGN")
        expr = self.parse_expression()
        return ("assign", var_name, expr)

    def parse_if_statement(self):
        """Parses an if-else statement."""
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
        """Parses a while loop."""
        self.consume("WHILE")
        self.consume("LPAREN")
        condition = self.parse_expression()
        self.consume("RPAREN")
        body = self.parse_block()
        return ("while", condition, body)

    def parse_function_declaration(self):
        """Parses a function declaration: func name(...) { ... }"""
        self.consume("FUNC")
        name = self.consume("ID")[1]
        self.consume("LPAREN")
        
        params = []
        if self.peek() and self.peek()[0] != "RPAREN":
            params.append(self.consume("ID")[1])
            while self.peek() and self.peek()[0] == "COMMA":
                self.consume("COMMA")
                params.append(self.consume("ID")[1])
        
        self.consume("RPAREN")
        body = self.parse_block()
        return ("function", name, params, body)
    
    def parse_return_statement(self):
        """Parses a return statement."""
        self.consume("RETURN")
        expr = self.parse_expression()
        return ("return", expr)

    def parse_block(self):
        """Parses a block of statements enclosed in braces { ... }."""
        statements = []
        self.consume("LBRACE")
        while self.peek() and self.peek()[0] != "RBRACE":
            statements.append(self.parse_statement())
        self.consume("RBRACE")
        return ("block", statements)

    def parse_expression(self):
        """Parses a logical comparison expression (lowest precedence)."""
        left = self.parse_term()
        while self.peek() and self.peek()[0] in ("EQ", "NE", "LT", "GT", "LE", "GE"):
            op = self.consume()
            right = self.parse_term()
            left = (op[0].lower(), left, right)
        return left

    def parse_term(self):
        """Parses an addition/subtraction expression."""
        left = self.parse_factor()
        while self.peek() and self.peek()[0] in ("PLUS", "MINUS"):
            op = self.consume()
            op_name = {"PLUS": "add", "MINUS": "sub"}[op[0]]
            right = self.parse_factor()
            left = (op_name, left, right)
        return left

    def parse_factor(self):
        """Parses a multiplication/division expression."""
        left = self.parse_primary()
        while self.peek() and self.peek()[0] in ("MULT", "DIV"):
            op = self.consume()
            op_name = {"MULT": "mult", "DIV": "div"}[op[0]]
            right = self.parse_primary()
            left = (op_name, left, right)
        return left

    def parse_primary(self):
        """Parses primary expressions."""
        token = self.peek()
        if token[0] == "NUMBER":
            return ("number", int(self.consume()[1]))
        elif token[0] == "STRING":
            return ("string", self.consume()[1])
        elif token[0] == "ID":
            if self._peek_next_significant()[0] == "LPAREN":
                return self.parse_function_call()
            else:
                return ("variable", self.consume()[1])
        elif token[0] == "LPAREN":
            self.consume("LPAREN")
            expr = self.parse_expression()
            self.consume("RPAREN")
            return expr
        else:
            raise RuntimeError(f"Unexpected token in expression: {token}")

    def parse_function_call(self):
        """Parses a function call: name(...)"""
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

    def _peek_next_significant(self):
        """Helper to look ahead one significant token without consuming."""
        start_pos = self.position
        while start_pos < len(self.tokens):
            if self.tokens[start_pos][0] not in ("NEWLINE", "COMMENT"):
                break
            start_pos += 1
        next_pos = start_pos + 1
        while next_pos < len(self.tokens):
            token = self.tokens[next_pos]
            if token[0] not in ("NEWLINE", "COMMENT"):
                return token
            next_pos += 1
        return ("EOF", None)