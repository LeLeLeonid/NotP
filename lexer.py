import re

TOKEN_SPEC = [("NUMBER", r"\d+"),("STRING", r'"[^"]*"'),("PRINT", r"print"),("PLUS", r"\+"),("MINUS", r"-"),("MULT", r"\*"),("DIV", r"/"),("EQ", r"=="),("NE", r"!="),("LT", r"<"),("GT", r">"),("LE", r"<="),("GE", r">="),("LPAREN", r"\("),("RPAREN", r"\)"),("LBRACE", r"\{"),("RBRACE", r"\}"),("LBRACKET", r"\["),("RBRACKET", r"\]"),("COMMA", r","),("SEMICOLON", r";"),("ASSIGN", r"="),("FUNC", r"func"),("IF", r"if"),("ELSE", r"else"),("WHILE", r"while"),("RETURN", r"return"),("ID", r"[A-Za-z_][A-Za-z0-9_]*"),("SKIP", r"[ \t]+"),("NEWLINE", r"\n"),("MISMATCH", r"."),]

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
        else:
            RaisetimeError(f"Unexpected character at index {index}")
    return tokens
