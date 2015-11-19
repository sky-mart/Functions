from abc import ABCMeta, abstractmethod
from numbers import Number
import math

class Func(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def value(self, varValues):
        pass

    @abstractmethod
    def derivative(self, arg):
        pass

    def withBraces(self):
        if isinstance(self, FuncConst) or isinstance(self, FuncVar):
            return str(self)
        return '(' + str(self) + ')'

    def __add__(self, other):
        if isinstance(other, Number):
            other = FuncConst(other)
        if isinstance(self, FuncConst):
            if self.c == 0:
                return other
            if isinstance(other, FuncConst):
                return FuncConst(self.c + other.c)
        if isinstance(other, FuncConst) and other.c == 0:
            return self
        return FuncSum(self, other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Number):
            other = FuncConst(other)
        if isinstance(self, FuncConst):
            if self.c == 0:
                return other
            if isinstance(other, FuncConst):
                return FuncConst(self.c - other.c)
        if isinstance(other, FuncConst) and other.c == 0:
            return self
        return FuncDiff(self, other)

    def __rsub__(self, other):
        if isinstance(other, Number):
            other = FuncConst(other)
        return other - self

    def __mul__(self, other):
        if isinstance(other, Number):
            other = FuncConst(other)
        if isinstance(self, FuncConst):
            if self.c == 0:
                return FuncConst(0)
            if self.c == 1:
                return other
            if isinstance(other, FuncConst):
                return FuncConst(self.c * other.c)
        if isinstance(other, FuncConst):
            if other.c == 0:
                return FuncConst(0)
            if other.c == 1:
                return self
        return FuncProd(self, other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Number):
            other = FuncConst(other)
        if isinstance(self, FuncConst):
            if self.c == 0:
                return FuncConst(0)
            if isinstance(other, FuncConst):
                return FuncConst(self.c / other.c)
        if isinstance(other, FuncConst):
            if other.c == 0:
                raise ValueError('Dividing by zero')
            if other.c == 1:
                return self
        return FuncQuot(self, other)

    def __rtruediv__(self, other):
        if isinstance(other, Number):
            other = FuncConst(other)
        return other / self

    def __pow__(self, power, modulo=None):
        if isinstance(power, Number):
            power = FuncConst(power)
        if isinstance(self, FuncConst):
            if self.c == 0:
                return FuncConst(0)
            if self.c == 1:
                return FuncConst(1)
            if isinstance(power, FuncConst):
                return FuncConst(self.c ** power.c)
        if isinstance(power, FuncConst):
            if power.c == 0:
                return FuncConst(1)
            if power.c == 1:
                return self
        return Pow(self, power)

    def __rpow__(self, power, modulo=None):
        if isinstance(power, Number):
            other = FuncConst(power)
        return other ** self


class FuncConst(Func):
    def __init__(self, c):
        self.c = c

    def value(self, varValues):
        return self.c

    def derivative(self, arg):
        return FuncConst(0)

    def __str__(self):
        return str(self.c)


class FuncVar(Func):
    def __init__(self, varName):
        self.varName = varName

    def value(self, varValues):
        if isinstance(varValues, dict) and self in varValues:
            return varValues[self]
        return varValues

    def derivative(self, arg):
        if arg is self:
            return FuncConst(1)
        return FuncConst(0)

    def __str__(self):
        return self.varName


class FuncOper(Func):
    def __init__(self, u, v):
        self.u = u
        self.v = v


class FuncSum(FuncOper):
    def value(self, varValues):
        return self.u.value(varValues) + self.v.value(varValues)

    def derivative(self, arg):
        return self.u.derivative(arg) + self.v.derivative(arg)

    def __str__(self):
        return self.u.withBraces() + ' + ' + self.v.withBraces()


class FuncDiff(FuncOper):
    def value(self, varValues):
        return self.u.value(varValues) - self.v.value(varValues)

    def derivative(self, arg):
        return self.u.derivative(arg) - self.v.derivative(arg)

    def __str__(self):
        return self.u.withBraces() + ' - ' + self.v.withBraces()


class FuncProd(FuncOper):
    def value(self, varValues):
        return self.u.value(varValues) * self.v.value(varValues)

    def derivative(self, arg):
        return self.u.derivative(arg) * self.v + self.u * self.v.derivative(arg)

    def __str__(self):
        return self.u.withBraces() + ' * ' + self.v.withBraces()


class FuncQuot(FuncOper):
    def value(self, varValues):
        return self.u.value(varValues) / self.v.value(varValues)

    def derivative(self, arg):
        return (self.u.derivative(arg) * self.v - self.u * self.v.derivative(arg)) / (self.v * self.v)

    def __str__(self):
        return self.u.withBraces() + ' / ' + self.v.withBraces()


class Pow(FuncOper):
    def value(self, varValues):
        return self.u.value(varValues) ** self.v.value(varValues)

    def derivative(self, arg):
        return Exp(Ln(self.u) * self.v).derivative(arg)

    def __str__(self):
        return self.u.withBraces() + ' ** ' + self.v.withBraces()


class ComplexFunc(Func):
    def __init__(self, arg):
        self.arg = arg

    @abstractmethod
    def simpleValue(self, x):
        pass

    def value(self, varValues):
        return self.simpleValue(self.arg.value(varValues))

    @abstractmethod
    def simpleDerivative(self):
        pass

    def derivative(self, arg):
        if arg is not self.arg:
            return self.simpleDerivative() * self.arg.derivative(arg)
        return self.simpleDerivative()


class Exp(ComplexFunc):
    def simpleValue(self, x):
        return math.exp(x)

    def simpleDerivative(self):
        return self

    def __str__(self):
        return 'exp(' + str(self.arg) + ')'


class Ln(ComplexFunc):
    def simpleValue(self, x):
        return math.log(x)

    def simpleDerivative(self):
        return FuncConst(1) / self.arg

    def __str__(self):
        return 'ln(' + str(self.arg) + ')'


class Sin(ComplexFunc):
    def simpleValue(self, x):
        return math.sin(x)

    def simpleDerivative(self):
        return Cos(self.arg)

    def __str__(self):
        return 'sin(' + str(self.arg) + ')'


class Cos(ComplexFunc):
    def simpleValue(self, x):
        return math.cos(x)

    def simpleDerivative(self):
        return FuncConst(-1) * Sin(self.arg)

    def __str__(self):
        return 'cos(' + str(self.arg) + ')'


class Tan(ComplexFunc):
    def simpleValue(self, x):
        return math.tan(x)

    def simpleDerivative(self):
        return FuncConst(1) / (Cos(self.arg) ** FuncConst(2))

    def __str__(self):
        return 'tan(' + str(self.arg) + ')'


class Asin(ComplexFunc):
    def simpleValue(self, x):
        return math.asin(x)

    def simpleDerivative(self):
        return FuncConst(1) / ((FuncConst(1) - (self.arg ** FuncConst(2))) ** FuncConst(0.5))

    def __str__(self):
        return 'asin(' + str(self.arg) + ')'


class Acos(ComplexFunc):
    def simpleValue(self, x):
        return math.acos(x)

    def simpleDerivative(self):
        return FuncConst(-1) / ((FuncConst(1) - (self.arg ** FuncConst(2))) ** FuncConst(0.5))

    def __str__(self):
        return 'acos(' + str(self.arg) + ')'


class Atan(ComplexFunc):
    def simpleValue(self, x):
        return math.atan(x)

    def simpleDerivative(self):
        return FuncConst(1) / (FuncConst(1) + (self.arg ** FuncConst(2)))

    def __str__(self):
        return 'atan(' + str(self.arg) + ')'


class Poly(ComplexFunc):
    def __init__(self, arg, coeffs):
        super().__init__(arg)
        self.coeffs = {p: cf for p, cf in coeffs.items() if cf != 0}

    def simpleValue(self, x):
        return sum([cf * (x ** p) for p, cf in self.coeffs.items()])

    def simpleDerivative(self):
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
                        s += self.arg.withBraces()
                        if p != 1:
                            s += ' ** ' + str(p)
                if i != len(self.coeffs):
                    s += ' + '
            i += 1
        return s


def jacobian(funcs, vars):
    return [[f.derivative(v) for v in vars] for f in funcs]

x = FuncVar('x')
y = FuncVar('y')
z = FuncVar('z')

f = x ** 2 + y ** 2
g = Sin(x * y)

J = jacobian([f, g], [x, y])

for row in J:
    for j in row:
        print(j)