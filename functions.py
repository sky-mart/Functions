from numbers import Number
import math

class Func(object):
    def value(self, varValue):
        pass

    def derv(self, arg):
        pass

    def str_with_parentheses(self):
        if isinstance(self, (Const, Var)):
            return str(self)
        return '(' + str(self) + ')'

    def __add__(self, other):
        if isinstance(other, Number):
            other = Const(other)
        if isinstance(self, Const):
            if self.c == 0:
                return other
            if isinstance(other, Const):
                return Const(self.c + other.c)
        if isinstance(other, Const) and other.c == 0:
            return self
        return Sum(self, other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Number):
            other = Const(other)
        if isinstance(self, Const):
            if self.c == 0:
                return other
            if isinstance(other, Const):
                return Const(self.c - other.c)
        if isinstance(other, Const) and other.c == 0:
            return self
        return Diff(self, other)

    def __rsub__(self, other):
        if isinstance(other, Number):
            other = Const(other)
        return other - self

    def __mul__(self, other):
        if isinstance(other, Number):
            other = Const(other)
        if isinstance(self, Const):
            if self.c == 0:
                return Const(0)
            if self.c == 1:
                return other
            if isinstance(other, Const):
                return Const(self.c * other.c)
        if isinstance(other, Const):
            if other.c == 0:
                return Const(0)
            if other.c == 1:
                return self
        return Prod(self, other)

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if isinstance(other, Number):
            other = Const(other)
        if isinstance(self, Const):
            if self.c == 0:
                return Const(0)
            if isinstance(other, Const):
                return Const(self.c / float(other.c))
        if isinstance(other, Const):
            if other.c == 0:
                raise ValueError('Dividing by zero')
            if other.c == 1:
                return self
        return Quot(self, other)

    def __rdiv__(self, other):
        if isinstance(other, Number):
            other = Const(other)
        return other / self

    def __pow__(self, power, modulo=None):
        if isinstance(power, Number):
            power = Const(power)
        if isinstance(self, Const):
            if self.c == 0:
                return Const(0)
            if self.c == 1:
                return Const(1)
            if isinstance(power, Const):
                return Const(self.c ** power.c)
        if isinstance(power, Const):
            if power.c == 0:
                return Const(1)
            if power.c == 1:
                return self
        return Pow(self, power)

    def __rpow__(self, power, modulo=None):
        if isinstance(power, Number):
            other = Const(power)
        return other ** self


class Const(Func):
    def __init__(self, c):
        self.c = c

    def value(self, varValue):
        return self.c

    def derv(self, arg):
        return Const(0)

    def __str__(self):
        return str(self.c)


class Var(Func):
    def __init__(self, name):
        self.name = name

    def value(self, varValue):
        if isinstance(varValue, dict) and self in varValue:
            return varValue[self]
        return varValue

    def derv(self, arg):
        if arg is self:
            return Const(1)
        return Const(0)

    def __str__(self):
        return self.name


class Oper(Func):
    def __init__(self, u, v):
        self.u = u
        self.v = v


class Sum(Oper):
    def value(self, varValue):
        return self.u.value(varValue) + self.v.value(varValue)

    def derv(self, arg):
        return self.u.derv(arg) + self.v.derv(arg)

    def __str__(self):
        return self.u.str_with_parentheses() + ' + ' + self.v.str_with_parentheses()


class Diff(Oper):
    def value(self, varValue):
        return self.u.value(varValue) - self.v.value(varValue)

    def derv(self, arg):
        return self.u.derv(arg) - self.v.derv(arg)

    def __str__(self):
        return self.u.str_with_parentheses() + ' - ' + self.v.str_with_parentheses()


class Prod(Oper):
    def value(self, varValue):
        return self.u.value(varValue) * self.v.value(varValue)

    def derv(self, arg):
        return self.u.derv(arg) * self.v + self.u * self.v.derv(arg)

    def __str__(self):
        return self.u.str_with_parentheses() + ' * ' + self.v.str_with_parentheses()


class Quot(Oper):
    def value(self, varValue):
        return self.u.value(varValue) / float(self.v.value(varValue))

    def derv(self, arg):
        return (self.u.derv(arg) * self.v - self.u * self.v.derv(arg)) / (self.v * self.v)

    def __str__(self):
        return self.u.str_with_parentheses() + ' / ' + self.v.str_with_parentheses()


class Pow(Oper):
    def value(self, varValue):
        return self.u.value(varValue) ** self.v.value(varValue)

    def derv(self, arg):
        return Exp(Ln(self.u) * self.v).derv(arg)

    def __str__(self):
        return self.u.str_with_parentheses() + ' ** ' + self.v.str_with_parentheses()


class ComplexFunc(Func):
    def __init__(self, arg):
        self.arg = arg

    def simple_value(self, x):
        pass

    def value(self, varValue):
        return self.simple_value(self.arg.value(varValue))

    def simple_derv(self):
        pass

    def derv(self, arg):
        if arg is not self.arg:
            return self.simple_derv() * self.arg.derv(arg)
        return self.simple_derv() 


class Exp(ComplexFunc):
    def simple_value(self, x):
        return math.exp(x)

    def simple_derv(self):
        return self

    def __str__(self):
        return 'exp(' + str(self.arg) + ')'


class Ln(ComplexFunc):
    def simple_value(self, x):
        return math.log(x)

    def simple_derv(self):
        return 1 / self.arg

    def __str__(self):
        return 'ln(' + str(self.arg) + ')'


class Sin(ComplexFunc):
    def simple_value(self, x):
        return math.sin(x)

    def simple_derv(self):
        return Cos(self.arg)

    def __str__(self):
        return 'sin(' + str(self.arg) + ')'


class Cos(ComplexFunc):
    def simple_value(self, x):
        return math.cos(x)

    def simple_derv(self):
        return -1 * Sin(self.arg)

    def __str__(self):
        return 'cos(' + str(self.arg) + ')'


class Tan(ComplexFunc):
    def simple_value(self, x):
        return math.tan(x)

    def simple_derv(self):
        return 1 / (Cos(self.arg) ** 2)

    def __str__(self):
        return 'tan(' + str(self.arg) + ')'


class Asin(ComplexFunc):
    def simple_value(self, x):
        return math.asin(x)

    def simple_derv(self):
        return 1 / (1 - self.arg ** 2) ** 0.5

    def __str__(self):
        return 'asin(' + str(self.arg) + ')'


class Acos(ComplexFunc):
    def simple_value(self, x):
        return math.acos(x)

    def simple_derv(self):
        return -1 / (1 - self.arg ** 2) ** 0.5

    def __str__(self):
        return 'acos(' + str(self.arg) + ')'


class Atan(ComplexFunc):
    def simple_value(self, x):
        return math.atan(x)

    def simple_derv(self):
        return 1 / (1 + self.arg ** 2)

    def __str__(self):
        return 'atan(' + str(self.arg) + ')'


class Poly(ComplexFunc):
    def __init__(self, arg, coeffs):
        super().__init__(arg)
        self.coeffs = {p: cf for p, cf in coeffs.items() if cf != 0}

    def simple_value(self, x):
        return sum([cf * (x ** p) for p, cf in self.coeffs.items()])

    def simple_derv(self):
        return Poly(self.arg, {p - 1: cf * p for p, cf in self.coeffs.items()})

    def __str__(self):
        s = ''
        i = 1
        for p, cf in self.coeffs.items():
            if cf != 0:
                if p == 0:
                    if cf != 0:
                        s += str(cf)
                else:
                    if cf != 0:
                        if cf != 1:
                            s += str(cf) + ' * '
                        s += self.arg.str_with_parentheses()
                        if p != 1:
                            s += ' ** ' + str(p)
                if i != len(self.coeffs):
                    s += ' + '
            i += 1
        return s


def jacobian(funcs, vars):
    return [[f.derv(v) for v in vars] for f in funcs]


if __name__ == '__main__':
    # Simplest funtional:
    x = Var('x')
    print x.value(21)   # gives 21

    # Addition and multiplication:
    f1 = (x + 2) * 4
    print f1.value(17)  # gives 76

    # Subtraction, division and priority
    f2 = x / 4 - 23.5
    print f2.value(98)  # gives 1

    # Function output and Derivative
    f3 = x*x + 2*x + 4
    print f3.derv(x)            # gives 2x + 2
    print f3.derv(x).value(9)   # gives 20

    # Complex functions
    f4 = Ln(x)
    print f4, f4.derv(x)
    f5 = Sin(x)
    print f5, f5.derv(x)
    f6 = Cos(x)
    print f6, f6.derv(x)
    f7 = Tan(x)
    print f7, f7.derv(x)
