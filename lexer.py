import re

TOKEN_SPEC = [("NUMBER", r"\d+"),("PRINT", r"print"),("PLUS", r"\+"),("LPAREN", r"\("),("RPAREN", r"\)"),("FUNC", r"func"),("IF", r"if"),("ELSE", r"else"),("WHILE", r"while"),("RETURN", r"return"),("EQ", r"="),("ID", r"[A-Za-z_][A-Za-z0-9_]*"), ("SKIP", r"[ \t]+"),("MISMATCH", r"."), ]

def lexer(code):
    """
    Lexer for the Notp language.
    Accepts source code (string).
    Returns a list of tokens in video tuples (token type, text).
    """
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
