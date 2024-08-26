# Maybe pass around ignore list for reduce?

# Use Reduced Expressions
# 


# reduce:   (Expr)          ->  (Expr)
#           1+(1+2)         ->  1+1+2
#           2-(3+2)         ->  2+[-3]+[-2]
#           2(2*2)          ->  (2)(2)(2)
#           2(2(2(2)))      ->  (2)(2)(2)(2)
#           2(2(2+1))       ->  (2)(2)(2+1)
#           2(2(3/2))       ->  (2)(2)(3)((2)^(-1))
#           (1/(1+2))/(3+1) ->  (1)((1+2)^(-1))((3+1)^(-1))
#           3/2             ->  (3)((2)^(-1))
#           1/2             ->  (2)^(-1)

# simplify  (Expr)          ->  (Expr)
#           (1)(x+1(2+1))   ->  (x+1(2+1))
#           (-1)(-1)        ->  1
#           0+x
#            


# Val:       (Real) Value
# Var:       (Char) Variable
# ExpoGroup:   (Expr) Base, (Expr) Power
# MultGroup:   (List Expr)
# DivGroup:    (Expr) Num, (Expr) Dem
# AddGroup:    (List Expr)
# Expression:  Everything derives it


def add_spaces(lines, prefix=" "):
    return "\n".join([prefix + l for l in lines.split("\n") if l])


class Expression:

    def __init__(self):
        pass

    def reduce(self):
        pass


class Primitive(Expression):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)


class Value(Primitive):

    def __init__(self, value):
        # value - Real
        super().__init__(self, value)

    def reduce(self):
        return Value(self.val)


class Variable(Primitive):

    def __init__(self, variable_name):
        # variable_name - Char
        super().__init__(self, variable_name)

    def reduce(self):
        return Variable(self.val)



# Maybe?
# class Group(Expression):
# Then extend Add/Mult/Div group

class AddGroup(Expression):

    def __init__(self, terms):
        # terms - List:Expression
        self.terms = terms

    def reduce(self):
        return AddGroup(None)

    def __str__(self):
        s = ""
        for t in self.terms:
            if s:
                s += "+\n"
            s += add_spaces(str(t)) + "\n"


class MultGroup(Expression):

    def __init__(self, terms):
        #terms - List:Expression
        self.terms = terms

    def reduce(self):
        return MultGroup(None)
    
    def __str__(self):
        s = ""
        for t in self.terms:
            if s:
                s += "*\n"
            s += add_spaces(str(t)) + "\n"


class DivGroup(Expression):

    def __init__(self, numerator, denominator):
        # numerator - Expression
        # denominator - Expression
        self.num = numerator
        self.dem = denominator

    def reduce(self):
        return MultGroup(None)
    
    def __str__(self):
        return (add_spaces(str(self.num)) +
                "\n/\n" +
                add_spaces(str(self.dem)) +
                "\n")

