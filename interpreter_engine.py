from lark import Lark, Transformer, Tree, Token

# Grammar with for loop support
grammar = """
    ?start: statement+

    ?statement: assignment
              | print_stmt
              | if_stmt
              | while_stmt
              | for_stmt

    block: "{" statement+ "}"

    assignment: NAME "=" expr
    print_stmt: "print" expr

    if_stmt: "if" "(" condition ")" block ["else" block]
    while_stmt: "while" "(" condition ")" block
    for_stmt: "for" "(" assignment ";" condition ";" assignment ")" block

    ?condition: condition "or" cond_and    -> or_op
              | cond_and
    ?cond_and: cond_and "and" cond_not     -> and_op
             | cond_not
    ?cond_not: "not" cond_not              -> not_op
             | comparison

    ?comparison: expr COMPARATOR expr      -> compare
               | "(" condition ")"

    COMPARATOR: "<=" | "<" | ">=" | ">" | "==" | "!="

    ?expr: expr "+" term    -> add
         | expr "-" term    -> sub
         | term
    ?term: term "*" factor  -> mul
         | term "/" factor  -> div
         | factor
    ?factor: NUMBER         -> number
           | NAME           -> var
           | "(" expr ")"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

parser = Lark(grammar, parser="lalr")
symbol_table_i = {}

class ASTBuilder(Transformer):
    def number(self, n): return int(n[0])
    def var(self, v): return str(v[0])
    def add(self, items): return ('+', items[0], items[1])
    def sub(self, items): return ('-', items[0], items[1])
    def mul(self, items): return ('*', items[0], items[1])
    def div(self, items): return ('/', items[0], items[1])
    def assignment(self, items): return Tree("assignment", items)
    def print_stmt(self, items): return Tree("print_stmt", items)
    def block(self, items): return Tree("block", items)
    def if_stmt(self, items): return Tree("if_stmt", items)
    def while_stmt(self, items): return Tree("while_stmt", items)
    def for_stmt(self, items): return Tree("for_stmt", items)
    def or_op(self, items): return ('or', items[0], items[1])
    def and_op(self, items): return ('and', items[0], items[1])
    def not_op(self, items): return ('not', items[0])
    def compare(self, items):
        comparator = items[1].value
        return ('cmp', comparator, items[0], items[2])

def eval_expr(expr):
    if isinstance(expr, int):
        return expr
    if isinstance(expr, str):
        return symbol_table_i.get(expr, 0)
    if isinstance(expr, Tree):
        return eval_expr(expr.children[0])
    if isinstance(expr, tuple):
        op = expr[0]
        if op in ('+', '-', '*', '/'):
            a, b = eval_expr(expr[1]), eval_expr(expr[2])
            if op == '+': return a + b
            if op == '-': return a - b
            if op == '*': return a * b
            if op == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                return a // b
        elif op == 'cmp':
            comp, a, b = expr[1], eval_expr(expr[2]), eval_expr(expr[3])
            if comp == '<': return a < b
            if comp == '<=': return a <= b
            if comp == '>': return a > b
            if comp == '>=': return a >= b
            if comp == '==': return a == b
            if comp == '!=': return a != b
        elif op == 'and': return eval_expr(expr[1]) and eval_expr(expr[2])
        elif op == 'or': return eval_expr(expr[1]) or eval_expr(expr[2])
        elif op == 'not': return not eval_expr(expr[1])
    raise ValueError(f"Cannot evaluate expression: {expr}")

def execute_statements(statements):
    for stmt in statements:
        if isinstance(stmt, Tree) and stmt.data == "block":
            execute_statements(stmt.children)
        else:
            execute_statement(stmt)

def execute_statement(stmt):
    if stmt.data == "block":
        execute_statements(stmt.children)
    elif stmt.data == "assignment":
        var_token = stmt.children[0]
        var_name = var_token.value if isinstance(var_token, Token) else str(var_token)
        value = eval_expr(stmt.children[1])
        symbol_table_i[var_name] = value
    elif stmt.data == "print_stmt":
        value = eval_expr(stmt.children[0])
        print(value)
    elif stmt.data == "if_stmt":
        condition = eval_expr(stmt.children[0])
        true_block = stmt.children[1]
        false_block = stmt.children[2] if len(stmt.children) > 2 else None
        if condition:
            execute_statements(true_block.children)
        elif false_block:
            execute_statements(false_block.children)
    elif stmt.data == "while_stmt":
        condition_node = stmt.children[0]
        block = stmt.children[1]
        while eval_expr(condition_node):
            execute_statements(block.children)
    elif stmt.data == "for_stmt":
        init = stmt.children[0]
        condition_node = stmt.children[1]
        update = stmt.children[2]
        block = stmt.children[3]
        execute_statement(init)
        while eval_expr(condition_node):
            execute_statements(block.children)
            execute_statement(update)
    else:
        raise NotImplementedError(f"Unknown statement type: {stmt.data}")

def interpret_terminal(tree):
    symbol_table_i.clear()
    execute_statements(tree.children)
