class ReturnSignal(Exception):
    """A special exception used to handle 'return' statements."""
    def __init__(self, value):
        self.value = value

class Environment:
    """Manages a scope for variables, with a reference to a parent scope."""
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def define(self, name, value):
        """Defines a new variable in the current scope."""
        self.vars[name] = value

    def assign(self, name, value):
        """Assigns a value to an existing variable, searching up the scope chain."""
        if name in self.vars:
            self.vars[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise NameError(f"Variable '{name}' is not defined.")

    def lookup(self, name):
        """Looks up a variable's value, searching up the scope chain."""
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.lookup(name)
        raise NameError(f"Variable '{name}' is not defined.")

def interpret(ast, env=None):
    """
    Executes an AST directly using a tree-walking interpreter approach.

    Args:
        ast: The Abstract Syntax Tree node to be interpreted.
        env: The environment that stores variables and scopes.

    Returns:
        The result of the evaluated expression, or None for statements.
    """
    if env is None:
        env = Environment()

    cmd = ast[0]

    if cmd == "program":
        result = None
        for stmt in ast[1]:
            result = interpret(stmt, env)
        return result

    elif cmd == "block":
        for stmt in ast[1]:
            interpret(stmt, env)

    elif cmd == "assign":
        var_name = ast[1]
        value = interpret(ast[2], env)
        env.define(var_name, value)

    elif cmd == "print":
        value = interpret(ast[1], env)
        print(value)

    elif cmd == "number":
        return ast[1]

    elif cmd == "string":
        return ast[1][1:-1]

    elif cmd == "variable":
        return env.lookup(ast[1])

    elif cmd in ("add", "sub", "mult", "div", "eq", "ne", "lt", "gt", "le", "ge"):
        left = interpret(ast[1], env)
        right = interpret(ast[2], env)
        if cmd == "add": return left + right
        if cmd == "sub": return left - right
        if cmd == "mult": return left * right
        if cmd == "div": return left // right
        if cmd == "eq": return left == right
        if cmd == "ne": return left != right
        if cmd == "lt": return left < right
        if cmd == "gt": return left > right
        if cmd == "le": return left <= right
        if cmd == "ge": return left >= right

    elif cmd == "if":
        condition = interpret(ast[1], env)
        if condition:
            interpret(ast[2], env)
        elif ast[3]:
            interpret(ast[3], env)

    elif cmd == "while":
        while interpret(ast[1], env):
            interpret(ast[2], env)

    elif cmd == "function":
        name, params, body = ast[1], ast[2], ast[3]
        env.define(name, ("function", params, body, env))

    elif cmd == "call":
        func_name = ast[1]
        callee = env.lookup(func_name)
        
        if not isinstance(callee, tuple) or callee[0] != "function":
            raise TypeError(f"'{func_name}' is not a function.")

        _, params, body, definition_env = callee
        args = [interpret(arg, env) for arg in ast[2]]

        if len(params) != len(args):
            raise TypeError(f"Function '{func_name}' expects {len(params)} arguments, but got {len(args)}.")

        call_env = Environment(parent=definition_env)
        for param_name, arg_value in zip(params, args):
            call_env.define(param_name, arg_value)

        try:
            interpret(body, call_env)
            return None
        except ReturnSignal as ret:
            return ret.value

    elif cmd == "return":
        value = interpret(ast[1], env)
        raise ReturnSignal(value)

    elif cmd == "expression_statement":
        return interpret(ast[1], env)

    else:
        raise RuntimeError(f"Unknown AST node type: {cmd}")