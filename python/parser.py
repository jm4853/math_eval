from parseTree import *

line = ""

# Grammar:
# 
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


# Parsing Helpers
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


# Node creation helpers
def makeVal(v):
    return ValNode(v)

def makeVar(v):
    return VarNode(v)

def makeMult(nodes):
    return OpNode("*", nodes)

def makeDiv(nodes):
    return OpNode("/", nodes)

def makeAdd(nodes):
    return OpNode("+", nodes)

def makeSub(nodes):
    return OpNode("-", nodes)

def makeParen(child):
    return ParenNode(child)


# Parsing functions
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
    # T - Term
    #     <T> :- ( <E> )
    #          | <S>
    if peek() == '(':
        next_c()
        E = parseE()
        if peek() != ')':
            panic('T')
        next_c()
        return makeParen(E)
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
    return parseE().flatten()

