#!/usr/bin/python

line = ""


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



def add_spaces(lines, prefix=" "):
    return "\n".join([prefix + l for l in lines.split("\n") if l])

class Node:
    def __init__(self):
        pass

class ValNode(Node):
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return str(self.val) + "\n"

class VarNode(Node):
    def __init__(self, var):
        self.var = var
    def __str__(self):
        return str(self.var) + "\n"

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

class TermNode(Node):
    def __init__(self, child):
        self.child = child
        

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

def makeMult(a, b):
    return OpNode('*', [a, b])

def makeDiv(a, b):
    return OpNode('/', [a, b])

def makeAdd(a, b):
    return OpNode('+', [a, b])

def makeSub(a, b):
    return OpNode('-', [a, b])

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
        return makeMult(T, parseG())
    return T

def parseM():
    # M - Multiplication
    #     <M> :- <G> * <M>
    #     <M> :- <G> / <M>
    #          | <G>
    G = parseG()
    if peek() == '*':
        next_c()
        return makeMult(G, parseM())
    if peek() == '/':
        next_c()
        return makeDiv(G, parseM())
    return G

def parseE():
    # E - Expression
    #     <E> :- <M> + <E>
    #          | <M> - <E>
    #          | <M>
    M = parseM()
    if peek() == '+':
        next_c()
        return makeAdd(M, parseE())
    if peek() == '-':
        next_c()
        return makeSub(M, parseE())
    return M


if __name__ == "__main__":
    while True:
        line = "".join(input('> ').split(" "))
        print(f"Got line: {line}")
        t = parseE()
        print(f"Got tree:")
        print(t)

    
