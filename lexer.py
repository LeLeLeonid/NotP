import re

TOKEN_SPEC = [
    # --- Ignored Tokens ---
    ("COMMENT", r"//.*"),
    ("SKIP", r"[ \t]+"),
    ("NEWLINE", r"\n"),

    # --- Literals ---
    ("NUMBER", r"\d+"),
    ("STRING", r'"([^"\\]|\\.)*"'),

    # --- Keywords ---
    ("PRINT", r"print\b"),
    ("FUNC", r"func\b"),
    ("IF", r"if\b"),
    ("ELSE", r"else\b"),
    ("WHILE", r"while\b"),
    ("RETURN", r"return\b"),

    # --- Operators ---
    ("EQ", r"=="),
    ("NE", r"!="),
    ("LE", r"<="),
    ("GE", r">="),
    
    # --- Single-character Operators ---
    ("LT", r"<"),
    ("GT", r">"),
    ("ASSIGN", r"="),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MULT", r"\*"),
    ("DIV", r"/"),

    # --- Delimiters ---
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("COMMA", r","),

    # --- Identifiers ---
    ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),

    # --- Mismatch ---
    ("MISMATCH", r"."),
]


TOKEN_REGEXES = [(token_type, re.compile(pattern)) for token_type, pattern in TOKEN_SPEC]

def lexer(code):
    """
    Converts a string of source code into a list of tokens.
    """
    tokens = []
    index = 0
    match_found = False
    while index < len(code):
        match_found = False
        for token_type, regex in TOKEN_REGEXES:
            match = regex.match(code, index)
            if match:
                text = match.group(0)
                if token_type not in ("SKIP", "COMMENT", "NEWLINE"):
                    if token_type == "MISMATCH":
                        raise RuntimeError(f"Unexpected character: {text}")
                    tokens.append((token_type, text))
                index = match.end(0)
                match_found = True
                break
        if not match_found:
            raise RuntimeError(f"Lexer got stuck at index {index}")
    return tokens