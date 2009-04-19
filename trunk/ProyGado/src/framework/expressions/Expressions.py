'''
Created on 10/04/2009

@author: Harold Selvaggi
'''
from framework.base.base import *

class Expression:
    def __init__(self):
        self.subs = []
    
    def evaluate(self):
        None

class ConstantExpression(Expression):
    def __init__(self, val):
        Expression.__init__(self)
        self.value = val
    
    def evaluate(self):
        return self.value

class NumericExpression(Expression):
    def __init__(self, go, family, field):
        Expression.__init__(self)
        self.go = go
        self.field = field
        self.family = family
    
    def evaluate(self):
        component = self.go.getComponent(self.family)
        return int(getattr(component, self.field, '0'))  

class FloatExpression(Expression):
    def __init__(self, go, family, field):
        Expression.__init__(self)
        self.go = go
        self.field = field
        self.family = family
    
    def evaluate(self):
        component = self.go.getComponent(self.family)
        retorno = float(getattr(component, self.field)) 
        return retorno

class AddExpression(Expression):
    def __init__(self, exp1, exp2):
        Expression.__init__(self)
        self.subs.append(exp1)
        self.subs.append(exp2)
    
    def evaluate(self):
        return int(self.subs[0].evaluate()) + int(self.subs[1].evaluate())

class AddFloatExpression(Expression):
    def __init__(self, exp1, exp2):
        Expression.__init__(self)
        self.subs.append(exp1)
        self.subs.append(exp2)
    
    def evaluate(self):
        expr1res = float(self.subs[0].evaluate())
        expr2res = float(self.subs[1].evaluate())
        return  expr1res + expr2res

class MulExpression(Expression):
    def __init__(self, exp1, ex2):
        Expression.__init__(self)
        self.subs.append(exp1)
        self.subs.append(exp2)
            
    def evaluate(self):
        return self.subs[0].evaluate()*self.subs[1].evaluate()

class DivExpression(Expression):
    def __init__(self, exp1, exp2):
        Expression.__init__(self)
        self.subs.append(exp1)
        self.subs.append(exp2)
            
    def evaluate(self):
        return self.subs[0].evaluate()/self.subs[1].evaluate()

