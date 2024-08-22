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

    def flatten(self):
        return ValNode(self.val)
        

class VarNode(Node):

    def __init__(self, var):
        self.var = var

    def __str__(self):
        return str(self.var) + "\n"

    def flatten(self):
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


class ParenNode(Node):

    def __init__(self, child):
        self.child = child

    def __str__(self):
        return "(\n" + add_spaces(str(self.child)) + "\n)\n"

    def flatten(self):
        return ParenNode(self.child.flatten())

