def interpret(ast, env=None):
    """Executes an AST directly using a tree-walking interpreter approach."""
    if env is None:
        env = {}

    cmd = ast[0]

    if cmd == "program":
        for stmt in ast[1]:
            interpret(stmt, env)
        if "main" in env:
            func_type, params, body = env["main"]
            interpret(body, env)

    elif cmd == "assign":
        var_name = ast[1]
        value = interpret(ast[2], env)
        env[var_name] = value

    elif cmd == "print":
        value = interpret(ast[1], env)
        print(value)

    elif cmd == "number":
        return ast[1]

    elif cmd == "string":
        return ast[1]

    elif cmd == "variable":
        var_name = ast[1]
        if var_name in env:
            return env[var_name]
        else:
            raise NameError(f"Variable '{var_name}' not defined")

    elif cmd == "add":
        left = interpret(ast[1], env)
        right = interpret(ast[2], env)
        return left + right

    elif cmd == "sub":
        left = interpret(ast[1], env)
        right = interpret(ast[2], env)
        return left - right

    elif cmd == "mult":
        left = interpret(ast[1], env)
        right = interpret(ast[2], env)
        return left * right

    elif cmd == "div":
        left = interpret(ast[1], env)
        right = interpret(ast[2], env)
        return left // right

    elif cmd == "eq":
        left = interpret(ast[1], env)
        right = interpret(ast[2], env)
        return left == right

    elif cmd == "lt":
        left = interpret(ast[1], env)
        right = interpret(ast[2], env)
        return left < right

    elif cmd == "gt":
        left = interpret(ast[1], env)
        right = interpret(ast[2], env)
        return left > right

    elif cmd == "le":
        left = interpret(ast[1], env)
        right = interpret(ast[2], env)
        return left <= right

    elif cmd == "ge":
        left = interpret(ast[1], env)
        right = interpret(ast[2], env)
        return left >= right

    elif cmd == "ne":
        left = interpret(ast[1], env)
        right = interpret(ast[2], env)
        return left != right

    elif cmd == "block":
        for stmt in ast[1]:
            interpret(stmt, env)

    elif cmd == "if":
        condition = interpret(ast[1], env)
        if condition:
            interpret(ast[2], env)
        else:
            if ast[3]:
                interpret(ast[3], env)

    elif cmd == "while":
        condition = interpret(ast[1], env)
        while condition:
            interpret(ast[2], env)
            condition = interpret(ast[1], env)

    elif cmd == "call":
        func_name = ast[1]
        args = [interpret(arg, env) for arg in ast[2]]
        if func_name == "print":
            print(*args)
        else:
            raise RuntimeError(f"Function '{func_name}' not defined")

    elif cmd == "function":
        name = ast[1]
        params = ast[2]
        body = ast[3]
        env[name] = ("function", params, body)

    elif cmd == "return":
        return interpret(ast[1], env)

    else:
        raise RuntimeError(f"Unknown command: {cmd}")
