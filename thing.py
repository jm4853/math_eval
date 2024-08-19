#!/usr/bin/python

line = ""


# Next expression to fix: "x-x-1-1-x-1"
#   -> Gotta make classes for each node type
#        -> Probably worth making them derive OpNode class


# D - Digit
#     <D> :- 0|1|...|8|9
# N - Number
#     <N> :- <D> <N>
#          | ε
# V - Variable
#     <V> :- a|b|...|y|z
# S - Singleton
#     <S> :- <N>
#          | <V>
# T - Term (multiplicative group)
#     <T> :- ( <E> )
#          | <S>
# G - Group (of terms)
#     <G> :- <T> <G>
#          | <T>
# M - Multiplication
#     <M> :- <G> * <M>
#     <M> :- <G> / <M>
#          | <G>
# E - Expression
#     <E> :- <M> + <E>
#          | <M> - <E>
#          | <M>
# Q - Equation
#     <Q> :- <E> = <E>


class Operator:
    # Operator Function, String Representation, Order of Operation Precedence
    def __init__(self, op_func, op_str, op_p=0):
        self.f = op_func
        self.s = op_str
        self.p = op_p
    def __str__(self):
        return self.s
    def do(self, nodes):
        return self.f(nodes)

def do_bin_add(nodes):
    if len(nodes) != 2:
        print(f"Called do_bin_add with {len(nodes)} nodes, exiting")
        exit(1)
    return nodes[0] + nodes[1]

def do_bin_sub(nodes):
    if len(nodes) != 2:
        print(f"Called do_bin_sub with {len(nodes)} nodes, exiting")
        exit(1)
    return nodes[0] - nodes[1]

def do_bin_mult(nodes):
    if len(nodes) != 2:
        print(f"Called do_bin_mult with {len(nodes)} nodes, exiting")
        exit(1)
    return nodes[0] * nodes[1]

def do_bin_div(nodes):
    if len(nodes) != 2:
        print(f"Called do_bin_div with {len(nodes)} nodes, exiting")
        exit(1)
    return nodes[0] / nodes[1]

BIN_ADD = Operator(do_bin_add, '+')
BIN_SUB = Operator(do_bin_sub, '-')
BIN_MULT = Operator(do_bin_mult, '*')
BIN_DIV = Operator(do_bin_div, '/')


def add_spaces(lines, prefix=" "):
    return "\n".join([prefix + l for l in lines.split("\n") if l])

class Node:
    def __init__(self):
        pass
    def __add__(self, other):
        return makeAdd(self, other)
    def __sub__(self, other):
        return makeSub(self, other)
    def __mul__(self, other):
        return makeMult(self, other)
    def __truediv__(self, other):
        return makeDiv(self, other)

class ValNode(Node):
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return str(self.val) + "\n"
    def __add__(self, other):
        if isinstance(other, ValNode):
            return ValNode(self.val + other.val)
        return super().__add__(self, other)
    def __sub__(self, other):
        if isinstance(other, ValNode):
            return ValNode(self.val - other.val)
        return super().__sub__(self, other)
    def __mul__(self, other):
        if isinstance(other, ValNode):
            return ValNode(self.val * other.val)
        return super().__mul__(self, other)
    def __truediv__(self, other):
        if isinstance(other, ValNode):
            return ValNode(self.val * other.val)
        return super().__truediv__(self, other)
    def flatten(self):
        return ValNode(self.val)
    def eval(self):
        return ValNode(self.val)
        

class VarNode(Node):
    def __init__(self, var):
        self.var = var
    def __str__(self):
        return str(self.var) + "\n"
    def flatten(self):
        return VarNode(self.var)
    def eval(self, t=0):
        return VarNode(self.var)
        

class OpNode(Node):
    def __init__(self, op, children):
        self.op = op
        self.children = children
    def __str__(self):
        s = ""
        for c in self.children:
            if s:
                s += str(self.op) + "\n"
            s += add_spaces(str(c)) + "\n"
        return s
    def flatten(self):
        new_children = []
        for c in self.children:
            c = c.flatten()
            if isinstance(c, OpNode) and (c.op == self.op):
                new_children += c.children
            else:
                new_children.append(c)
        return OpNode(self.op, new_children)
    def eval(self):
        # Recursively evaluate children
        eval_children = [c.eval() for c in self.children]
        constant = None
        # If the first value is a value than we can combine all the
        # values. If its not the first value, it can get confusing
        # with operations like "x - 1 - 1"
        #   Could be fixed by making all operations order independent
        #   i.e. "x - 1 - 1" => "x + (-1) + (-1)"
        if isinstance(eval_children[0], ValNode):
            constant = eval_children[0]
            eval_children = eval_children[1:]
        new_children = []
        for c in eval_children:
            # If the child is a value, combine it with constant
            if constant and isinstance(c, ValNode):
                constant = self.op.do([constant, c])
            # Otherwise, add it to new_children
            else:
                new_children.append(c)
        if constant:
            new_children = [constant] + new_children
        if len(new_children) == 1:
            return new_children[0]
        return OpNode(self.op, new_children)
                

# class TermNode(Node):
#     def __init__(self, child):
#         self.child = child
        

def setline(new_line):
    global line
    line = new_line

def peek():
    global line
    if len(line) == 0:
        return ""
    return line[0]

def next_c():
    global line
    line = line[1:]

def panic(c='none'):
    print(f"Panic! (from {c})")
    exit(1)


def makeVal(v):
    return ValNode(v)

def makeVar(v):
    return VarNode(v)

def makeMult(nodes):
    return OpNode(BIN_MULT, nodes)

def makeDiv(nodes):
    return OpNode(BIN_DIV, nodes)

def makeAdd(nodes):
    return OpNode(BIN_ADD, nodes)

def makeSub(nodes):
    return OpNode(BIN_SUB, nodes)


def parseN_helper(v):
    n = peek()
    if n.isdigit():
        v *= 10
        v += int(n)
        next_c()
        return parseN_helper(v)
    return v

def parseN():
    # N - Number
    #     <N> :- <D> <N>
    #          | ε
    v = parseN_helper(0)
    return makeVal(v)

def parseV():
    # V - Variable
    #     <V> :- a|b|...|y|z
    n = peek()
    if n.isalpha():
        next_c()
        return makeVar(n)
    panic('V')

def parseS():
    # S - Singleton
    #     <S> :- <N>
    #          | <V>
    c = peek()
    if c.isdigit():
        return parseN()
    elif c.isalpha():
        return parseV()
    panic('S')

def parseT():
    # T - Term (multiplicative group)
    #     <T> :- ( <E> )
    #          | <S>
    if peek() == '(':
        next_c()
        E = parseE()
        if peek() != ')':
            panic('T')
        next_c()
        return E
        # return makeParen(c)
    return parseS()

def is_S():
    c = peek()
    if c.isalnum():
        return True
    return False

def is_T():
    return (is_S() or peek() == '(')

def parseG():
    # G - Group (of terms)
    #     <G> :- <T> <G>
    #          | <T>
    T = parseT()
    if is_T():
        return makeMult([T, parseG()])
    return T

def parseM():
    # M - Multiplication
    #     <M> :- <G> * <M>
    #     <M> :- <G> / <M>
    #          | <G>
    G = parseG()
    if peek() == '*':
        next_c()
        return makeMult([G, parseM()])
    if peek() == '/':
        next_c()
        return makeDiv([G, parseM()])
    return G

def parseE():
    # E - Expression
    #     <E> :- <M> + <E>
    #          | <M> - <E>
    #          | <M>
    M = parseM()
    if peek() == '+':
        next_c()
        return makeAdd([M, parseE()])
    if peek() == '-':
        next_c()
        return makeSub([M, parseE()])
    return M

def parse():
    # Must flatten or sub/div wont work
    return parseE().flatten()

def sub2add(t):
    if isinstance(t, OpNode):
        new_children = [sub2add(c) for c in t.children]
        if t.op == BIN_SUB:
            return makeAdd([new_children[0],
                            makeMult([makeVal(-1),
                                      makeAdd(new_children[1:])])])
        return OpNode(t.op, new_children)
    else:
        return t
def div2mult(t):
    return t
def eval_tree(t):
    return div2mult(sub2add(t)).eval()
    

if __name__ == "__main__":
    while True:
        line = "".join(input('> ').split(" "))
        print(f"Got line: {line}")
        t = parse()
        print(f"Got tree:")
        print(t)

    
