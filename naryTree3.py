import sys      
from random import randint

import commands
        
def printSpaces(i) :
    for ii in range(i) :
        sys.stdout.write(' ')   

class naryNode3 :
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.firstChild = None      #this node has pointers to only the first/last child node, not direct child node any more
        self.lastChild = None
        self.childCount = 0
        self.childIndices = []
        self.next = None        #this next/prev are sibling pointers
        self.prev = None  
        
    #def __del__(self):         #if __del__ is defined, this node will be 'freed' twice, by removeAll() and by gc
    #    print('del')
    #    self.removeAll()
                
    def newNode(self, data):
        return naryNode3(data)
                 
    def buildChildIndices(self):
        if self.firstChild :
            self.childIndices.clear()
            node = self.firstChild
            while node :
                self.childIndices.append(node)
                node.buildChildIndices()
                node = node.next

    def dump(self, level):
        printSpaces(level * 4)
        print(self.data, "childCnt=", len(self.childIndices))
        
        if self.firstChild == None :
            return
        
        node = self.firstChild
        while node:
            node.dump(level+1)
            node = node.next
                        
    def deleteChildNode(self, node):
        if self.firstChild == None:
            return
            
        self.childCount = self.childCount - 1
        
        #delete only node
        if node == self.firstChild and node == self.lastChild:
            self.firstChild = None
            self.lastChild = None
            return

        #delete firstChild
        if node == self.firstChild :
            self.firstChild = self.firstChild.next
            self.firstChild.prev = None
            return

        #delete lastChild
        if node == self.lastChild :
            self.lastChild = self.lastChild.prev
            self.lastChild.next = None
            return

        #delete middleNode
        node.prev.next = node.next;
        node.next.prev = node.prev;
        return      

        
            
    def addChildFirst(self, data):
        node = self.newNode(data)
        node.parent = self      
        self.childCount = self.childCount + 1
        node.childCount = 0
        node.next = None        #this next/prev are sibling pointers
        node.prev = None  
        
        if self.firstChild == None:
            self.firstChild = node
            self.lastChild = node
        else:
            node.next = self.firstChild
            self.firstChild.prev = node
            self.firstChild = node
            
        return node

    def addChildLast(self, data) :
        node = self.newNode(data)
        node.parent = self
        self.childCount = self.childCount + 1
        node.next = None        #this next/prev are sibling pointers
        node.prev = None  
        
        if self.lastChild == None:
            self.firstChild = node
            self.lastChild = node
        else:
            node.prev = self.lastChild
            self.lastChild.next = node
            self.lastChild = node
            
        return node
    
    def getRandomChildNode(self):
        return self.getChildNode(randint(0, self.childCount-1))

    def getNode(self, idx):
        node = self
        i = 0
        while node:
            if i == idx:
                return node
            i = i + 1
            node = node.next
        return None

    def getChildNode(self, idx):
        #commands.ODS(self.tp, self.status)
        return self.firstChild.getNode(idx)          
        
    def removeAll(self):        #this removes all inter-referencing of nodes
        node = self.firstChild
        while node:
            next = node.next
            node.removeAll()  
            node = next
                
        #print('remove', self.data)
        self.data = None
        self.parent = None
        self.firstChild = None
        self.lastChild = None
        self.childCount = 0
        self.childIndices.clear()
        self.next = None  
        self.prev = None        
        
    def findNodeInChildrenByData(self, data):
        node = self.firstChild
        if node == None:
            return None
        while node:
            if data == node.data:      
                return node
            node = node.next
        return None
        
    def createPath(self, data, *path):
        currentNode = self
        for pathName in path :
            c = currentNode.findNodeInChildrenByData(pathName)
            if c == None:
                currentNode = currentNode.addChildFirst(pathName)
            else :
                currentNode = c
        if currentNode.data == data :
            return
        c =  currentNode.findNodeInChildrenByData(data)
        if c == None :
            currentNode.addChildFirst(data) 

    def findNodeByPathName(self, *path):
        currentNode = self
        for pathName in path :
            currentNode = currentNode.findNodeInChildrenByData(pathName)
            if currentNode == None:
                return None
        return currentNode
        
    def dumpAsXml(self) :
        print('<data>')
        print(self.data)
        print('</data>')
           
        node = self.firstChild
        while node:
            print('<child>')
            node.dumpAsXml()        
            print('</child>')
            node = node.next


