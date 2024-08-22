#!/usr/bin/python
from parser import *
from expressionTree import *



# TODO: Implement parseTree to expressionTree conversion


if __name__ == "__main__":
    while True:
        line = "".join(input('> ').split(" "))
        print(f"Got line: {line}")
        setline(line)
        t = parse()
        print(f"Got tree:")
        print(t)

    
