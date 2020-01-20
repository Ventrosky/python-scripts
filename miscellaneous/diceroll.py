#!/usr/bin/python
from collections import deque
from random import seed, randint
from functools import reduce
import re, functools, sys

class DiceRoll():
    prec = {
        "d" : {"p":3,"f":lambda a,b: sum([randint(1,int(b)) for _ in range(int(a))])},
        "x" : {"p":2,"f":lambda a,b: a * b},
        "*" : {"p":2,"f":lambda a,b: a * b},
        "/" : {"p":2,"f":lambda a,b: a / b},
        "+" : {"p":1,"f":lambda a,b: a + b},
        "-" : {"p":1,"f":lambda a,b: a - b},
        "(" : {"p":0}
    }
    
    re_notation = re.compile('(\d+|[^ 0-9]|\d+\.\d+)')
    re_decimal = re.compile('^[+-]?\d+(\.\d+)?$')
    
    def to_posfix(self, string):
        isNotEmpty = lambda l: len(l) > 0
        self.posfix = []
        self.stack = deque()
        for o in re.findall(self.re_notation, string):
            if self.re_decimal.match(o):
                self.posfix.append(o)
            elif o == '(':
                self.stack.append(o)
            elif o == ')':
                oper = self.stack.pop()
                while not oper == '(':
                    self.posfix.append(oper)
                    oper = self.stack.pop()
            elif isNotEmpty(self.stack):
                while isNotEmpty(self.stack) and self.prec[self.stack[-1]]["p"] >= self.prec[o]["p"]:
                    self.posfix.append(self.stack.pop())
                self.stack.append(o)
            else:
                self.stack.append(o)
        while isNotEmpty(self.stack):
            self.posfix.append(self.stack.pop())
        return self.posfix

    def roll(self, a, x):
        value = 0
        for _ in range(a):
            value += randint(0, x)
    
    def evaluate(self, string):
        clean = string.lower().replace(" ", "").replace('x','*')
        self.to_posfix(clean)
        self.stack = deque()
        for o in self.posfix:
            if self.re_decimal.match(o):
                self.stack.append(o)
            else:
                b = float(self.stack.pop())
                a = float(self.stack.pop())
                self.stack.append(self.prec[o]["f"](a,b))
        return float(self.stack.pop())

dice = DiceRoll()

params = sys.argv[1:]
print()
print('** Evaluate dice rolling notation strings **')
if len(params) == 0:
    print('Usage:')
    print('./diceroll.py <expr_1> <expr_2> ... <expr_n>')
    print('Example:')
    print(' python3 ./diceroll.py 1d6*5 3d6x10+3 "3x(2d6+4)"')
    print()
    sys.exit()

print('List:', str(params))
print()
for dice_expr in params:
    print(dice_expr, ':')
    try:
        print(' =>', dice.evaluate(dice_expr))
    except:
        print(" => Something went wrong")

print()