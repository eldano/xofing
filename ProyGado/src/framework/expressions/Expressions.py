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

class NumericExpression(Expression):
    def __init__(self, go, family, field):
        Expression.__init__(self)
        self.go = go
        self.field = field
        self.family = family
    
    def evaluate(self):
        component = self.go.getComponent(self.family)
        return int(getattr(component, self.field, '0'))

class AddExpression(Expression):
    def __init__(self, exp1, exp2):
        Expression.__init__(self)
        self.subs.append(exp1)
        self.subs.append(exp2)
    
    def evaluate(self):
        return int(self.subs[0].evaluate()) + int(self.subs[1].evaluate())

class MulExpression(Expression):
    def __init__(self, exp1, ex2):
        Expression.__init__(self)
        self.subs.append(exp1)
        self.subs.append(exp2)
            
    def evaluate(self):
        return self.subs[0].evaluate()*self.subs[1].evaluate()

class DivExpression(Expression):
    def __init__(self, exp1, ex2):
        Expression.__init__(self)
        self.subs.append(exp1)
        self.subs.append(exp2)
            
    def evaluate(self):
        return self.subs[0].evaluate()/self.subs[1].evaluate()
