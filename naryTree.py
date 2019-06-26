#1, this is designed for task system
#2, 

import sys      
        
def printSpaces(i) :
    for ii in range(i) :
        sys.stdout.write(' ')

class naryNode :
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children  = []
        
    def removeAll(self):  #useless, but I think, this should make python garbage collector work faster.
        for s in self.children :
            s.removeAll()
        self.data = None
        self.children = None
            
    def dump(self, level):
        printSpaces(level * 4)
        #sys.stdout.write('*')
        #if self.parent == None :
            #print(self.data)
        #else:
            #print(self.data, '^', self.parent.data)
            
        print(self.data)
            
        for s in self.children :
            s.dump(level+1)
         
    def delChild(self, i):
        del self.children[i]  
        
    def addChildFirst(self, data):
        child = self.children
        child.insert(0, naryNode(data))
        child[0].parent = self
        return child[0]

    def addChildLast(self, data) :
        child = self.children
        l = len(child)
        child.insert(l, naryNode(data))
        child[l].parent = self
        return child[l]
        
    def addChild(self, i, data) :
        child = self.children
        child.insert(i, naryNode(data))
        child[i].parent = self
        return child[i]

    def getChild(self, i, data):
        return self.children[i]
              
    def findInChildren(self, data):
        for s in self.children :
            if s.data == data :
                return s
        return None

    def setByPathName(self, data, *args):
        currentNode = self
        for arg in args :
            c = currentNode.findInChildren(arg)
            if c == None:
                currentNode = currentNode.addChildFirst(arg)
            else :
                currentNode = c
        if currentNode.data == data :
            return
        c =  currentNode.findInChildren(data)
        if c == None :
            currentNode.addChildFirst(data) 

    def findNodeByPathName(self, *args):
        currentNode = self
        for arg in args :
            currentNode = currentNode.findInChildren(arg)
            if currentNode == None:
                return None
        return currentNode
        
    def delNodeInChildren(self, node) :
        i = 0
        for n in self.children:
            if n == node :
                del self.children[i]
                break
            i = i+1
            
    def dumpAsXml(self) :
        print('<data>')
        print(self.data)
        print('</data>')
           
        for s in self.children :
            print('<child>')
            s.dumpAsXml()        
            print('</child>')
                
    def test(self):
        self.setByPathName('memberA0', 'familyA')
        self.setByPathName('memberA1', 'familyA')
        self.setByPathName('memberB0', 'familyB')
        self.setByPathName('memberB1', 'familyB')
        self.setByPathName('memberC0', 'familyC')
        self.setByPathName('memberC1', 'familyC')
        self.setByPathName('memberCC1', 'familyC', 'memberC1')
        self.dump(0)
        node = self.findNodeByPathName('familyC', 'memberC1', 'memberCC1')
        node.parent.delNodeInChildren(node)
        self.dump(0)
        
        


        
        

