# Interpiler — Hybrid Compiler & Interpreter

A custom programming language implementation built from scratch in Python. Interpiler parses source code, builds an Abstract Syntax Tree, and interprets it — combining compiler front-end techniques with an interpreter back-end. Comes with both a GUI and terminal interface.

**Repo:** [github.com/kanishk-io/Interpiler-Hybrid-compiler](https://github.com/kanishk-io/Interpiler-Hybrid-compiler)

---

## What It Does

Interpiler defines its own mini programming language with a custom grammar. You write code in that language, and Interpiler:

1. **Parses** it using an LALR parser (via Lark)
2. **Builds an AST** (Abstract Syntax Tree) using a Transformer
3. **Interprets** the AST by walking the tree and executing each node

---

## Supported Language Features

| Feature | Syntax |
|---|---|
| Variable assignment | `x = 10` |
| Arithmetic | `+` `-` `*` `/` |
| Print | `print x` |
| If / Else | `if (condition) { } else { }` |
| While loop | `while (condition) { }` |
| For loop | `for (init; condition; update) { }` |
| Comparisons | `<` `<=` `>` `>=` `==` `!=` |
| Logic operators | `and` `or` `not` |

---

## Example Code

```
x = 1
while (x <= 5) {
    print x
    x = x + 1
}
```

```
for (i = 0; i < 3; i = i + 1) {
    print i
}
```

```
a = 10
b = 20
if (a < b) {
    print a
} else {
    print b
}
```

---

## Features

- Custom LALR grammar written with Lark
- Full AST construction via Transformer pattern
- Symbol table for variable storage
- Zero-division error handling
- Tkinter GUI with live status and output panel
- CLI mode via terminal

---

## Tech Stack

| | |
|---|---|
| Language | Python 3 |
| Parser | Lark (LALR) |
| GUI | Tkinter |
| Pattern | Lexer → Parser → AST → Interpreter |

---

## Project Structure

```
Interpiler-Hybrid-compiler/
├── interpiler_gui.py       # GUI entry point
├── interpreter_engine.py   # Grammar, AST builder, interpreter
└── README.md
```

---

## How to Run

```bash
git clone https://github.com/kanishk-io/Interpiler-Hybrid-compiler.git
cd Interpiler-Hybrid-compiler

# Install dependency
pip install lark

# GUI version
python interpiler_gui.py
```

---

## How It Works

```
Source Code
    ↓
Lark LALR Parser  (grammar rules → parse tree)
    ↓
ASTBuilder        (transforms parse tree → clean AST)
    ↓
Interpreter       (walks AST, evaluates expressions, updates symbol table)
    ↓
Output
```

---

## Project Context

Built as part of a Compiler Design course to demonstrate lexical analysis, grammar definition, parse tree construction, AST transformation, and tree-walk interpretation.

---

## License

MIT
