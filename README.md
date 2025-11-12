# NotP Language
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Status](https://img.shields.io/badge/status-in--development-orange)]()

NotP is an experimental, dynamically-typed programming language built from scratch in Python. It features a tree-walking interpreter and a bytecode compiler with its own virtual machine (stack-based). This project serves as a practical exploration of compiler theory, language design, and virtual machine architecture.

## Features

*   **Dual Execution Modes**: Run code instantly with the interpreter or compile it to bytecode for the custom stack-based VM.
*   **C-like Syntax**: Supports variables, arithmetic (`+`, `-`, `*`, `/`), comparisons (`>`, `<`, `==`), `if/else` statements, and `while` loops.
*   **Comments**: Use `//` for single-line comments.
*   **Clean Codebase**: A minimal, understandable implementation perfect for learning.

## Quick Start

### Prerequisites

*   Python 3.8+

### Running a Program

1.  Clone the repository:
    ```bash
    git clone https://github.com/LeLeLeonid/NotP.git
    cd NotP
    ```

2.  Run an example file using the default **interpreter**:
    ```bash
    python main.py examples/03_fibonacci.notp
    ```

3.  Run the same file using the **virtual machine**:
    ```bash
    python main.py examples/03_fibonacci.notp --vm
    ```

## Language Syntax Tour

#### Variables and Operations
```notp
// NotP supports variables and basic math.
x = 10
y = (x * 2) + 5 // y will be 25

print("The value of y is:")
print(y)
```

#### Control Flow (if/else and while)
```notp
// Conditional logic is straightforward.
a = 100
if (a > 50) {
  print("a is large")
} else {
  print("a is small")
}

// Loops are simple and powerful.
i = 0
print("Countdown:")
while (i < 5) {
  print(5 - i)
  i = i + 1
}
```

#### Fibonacci Example
A classic test for any language, demonstrating assignments, loops, and arithmetic working together.
```notp
// Calculate and print the first 10 Fibonacci numbers.
limit = 10
a = 0
b = 1

print("First 10 Fibonacci numbers:")
print(a)
print(b)

count = 2
while (count < limit) {
  next = a + b
  print(next)
  a = b
  b = next
  count = count + 1
}
```

## Project Roadmap

-   [x] Stable Lexer with comment support
-   [x] Robust Parser with correct operator precedence
-   [x] Tree-walking Interpreter (variables, arithmetic, control flow)
-   [x] Bytecode Compiler & VM (variables, arithmetic, control flow)
-   [x] Full implementation of function definitions, calls, and scopes.
-   [ ] **Next Up**: Add more data types (e.g., Arrays, Strings with escape sequences).
-   [ ] Build a small standard library.
-   [ ] **Long-term Goal**: Bootstrap the compiler to be self-hosting.

## Contributing

This is a learning project, and contributions are highly welcome! Feel free to open an issue to report a bug or suggest a feature, or submit a pull request with your improvements.
