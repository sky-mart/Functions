# Functions

The project implements analytical functions logics. It is possible to create any function combinations and their value will be calculated correctly. The most original part is differentiating.

# Simplest funtional:
```python
x = Var('x')
print x.value(21)   # gives 21
```
# Addition and multiplication:
```python
f1 = (x + 2) * 4
print f1.value(17)  # gives 76
```
# Subtraction, division and priority
```python
f2 = x / 4 - 23.5
print f2.value(98)  # gives 1
```
# Function output and Derivative
```python
f3 = x*x + 2*x + 4
print f3.derv(x)            # gives 2x + 2
print f3.derv(x).value(9)   # gives 20
```
# Complex functions
```python
f4 = Ln(x)
print f4, f4.derv(x)		# gives ln(x), 1/x
f5 = Sin(x)
print f5, f5.derv(x)		# gives sin(x), cos(x)
f6 = Cos(x)
print f6, f6.derv(x)		# gives cos(x), -sin(x)
f7 = Tan(x)
print f7, f7.derv(x)		# gives tan(x), 1/cos(x)^2
```
