
line = ""


# D - Digit
#     <D> :- 0|1|...|8|9
# N - Number
#     <N> :- <D> <N>
#          | ε
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



class Node:
    def __init__(self, node_t, val=0, children=[]):
        self.t = node_t
        self.val = val
        self.children = children
        

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
    return Node(node_t="VAL", val=v)

def makeVar(v):
    return Node(node_t="VAR", val=v)

def makeMult(a, b):
    return Node(node_t="MULT", children=[a,b])

def makeDiv(a, b):
    return Node(node_t="DIV", children=[a,b])

def makeAdd(a, b):
    return Node(node_t="ADD", children=[a,b])

def makeSub(a, b):
    return Node(node_t="SUB", children=[a,b])

def parseN_helper(v):
    n = peek()
    if n.isdigit():
        v *= 10
        v += int(n)
        next_c()
        return parseN_helper(v)
    return v

def parseN():
    v = parseN_helper(0)
    return makeVal(v)

def parseV():
    n = peek()
    if n.isalpha():
        next_c()
        return makeVar(n)
    panic('V')

def parseS():
    c = peek()
    if c.isdigit():
        return parseN()
    elif c.isalpha():
        return parseV()
    panic('S')

def parseT():
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
    T = parseT()
    if is_T():
        return makeMult(T, parseG())
    return T

def parseM():
    G = parseG()
    if peek() == '*':
        next_c()
        return makeMult(G, parseM())
    if peek() == '/':
        next_c()
        return makeDiv(G, parseM())
    return G

def parseE():
    M = parseM()
    if peek() == '+':
        next_c()
        return makeAdd(M, parseE())
    if peek() == '-':
        next_c()
        return makeSub(M, parseE())
    return M


def printTree(t, offset=0):
    if not t:
        print("GOT NONE")
        return
    if t.t == "VAL" or t.t == "VAR":
        print(f"{' ' * offset}{t.val}")
    if t.t == "ADD":
        printTree(t.children[0], offset+1)
        print(f"{' ' * offset}+")
        printTree(t.children[1], offset+1)
    if t.t == "SUB":
        printTree(t.children[0], offset+1)
        print(f"{' ' * offset}-")
        printTree(t.children[1], offset+1)
    if t.t == "MULT":
        printTree(t.children[0], offset+1)
        print(f"{' ' * offset}*")
        printTree(t.children[1], offset+1)
    if t.t == "DIV":
        printTree(t.children[0], offset+1)
        print(f"{' ' * offset}/")
        printTree(t.children[1], offset+1)



if __name__ == "__main__":
    while True:
        line = "".join(input('> ').split(" "))
        print(f"Got line: {line}")
        t = parseE()
        print(f"Got tree:")
        printTree(t)

    
