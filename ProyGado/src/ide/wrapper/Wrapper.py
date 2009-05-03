'''
Created on 03/05/2009

@author: Harold Selvaggi
'''

class CodeManager:
    def __init__(self):
        self.generated = []
    
    def isGenerated(self, name):
        return self.generated.__contains__(name)
    
    def addGenerated(self, name):
        self.generated.append(name) 

class TypeBase:
    CONDITION = 1
    GAMEOBJECT = 2
    STRING = 3
    NUMBER = 4
    FIELD = 5   # Representa un campo de uno de los Wrappers asociados
    FAMILY = 6  # Representa un enumerado de ComponentFamily
    ACTIONLIST = 7 # Representa una lista de Actions

class Wrapper:
    def __init__(self, name):
        self.name = name
    
    # La interface grafica toma estos atributos como los editables del objeto
    # return: List<(name, TypeBase)>
    def getAttributeList(self):
        return []

    def generateCode(self, codeManager, identLevel):
        return ""
    
    # Devuelve un string representando el una parte de XML a persistirse
    def persist(self, codeManager):
        return ""

class AndCondition(Wrapper):
    def __init__(self, name):
        Wrapper.__init__(self, name)
        self.cond1 = None
        self.cond2 = None
    
    def getAttributeList(self):
        return [('cond1', TypeBase.CONDITION), ('cond2', TypeBase.CONDITION)]

    def generateCode(self, codeManager, identLevel):
        if codeManager.generated(name):
            return ""
        else:
            codeManager.addGenerated(name)
            res = ""
            res = res + cond1.generateCode(codeManager,identLevel)
            res = res + cond2.generateCode(codeManager,identLevel)
            res = res + self.name + " = AndCondition(" + self.cond1.name + ", " + self.cond2.name + ")\n"
            return res
        
    def persist(self, codeManager):
        return ""

class EqualCondition(Wrapper):
    def __init__(self, name):
        Wrapper.__init__(self, name)
        self.go = None
        self.value = None
        self.family = None
        self.field = None
        self.proxyList = []
    
    def getAttributeList(self):
        return [('go', TypeBase.GAMEOBJECT), ('value', TypeBase.STRING), ('family', TypeBase.FAMILY), ('field', TypeBase.FIELD), ('proxyList', TypeBase.ACTIONLIST)]

    def generateCode(self, codeManager, identLevel):
        if codeManager.generated(name):
            return ""
        else:
            codeManager.addGenerated(name)
            res = self.name + " = EqualCondition(" + self.go.name + ", " + self.family + ", " + self.field + ". " + self.value + ")\n"
            for proxy in self.proxyList:
                res = res + self.name + ".addProxy(" + proxy.name + ")\n"
            return res
        
    def persist(self, codeManager):
        return ""