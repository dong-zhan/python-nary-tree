#1, this is designed for task system
#2, 

import sys      
import linkedlist2
        
def printSpaces(i) :
    for ii in range(i) :
        sys.stdout.write(' ')   

class naryNode2 :
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = None  
        
    #def __del__(self):   		#if __del__ is defined, this node will be 'freed' twice, by removeAll() and by gc
    #    print('del')
    #    self.removeAll()
                
    #virtual allocator
    def newNode(self, data):
        return naryNode2(data)
                 
    def dump(self, level):
        printSpaces(level * 4)
        print(self.data)
        
        if self.children == None :
            return
        
        node = self.children.firstNode
        while not node == None:
            node.data.dump(level+1)
            node = node.next
            
    def addChildFirst(self, data):
        node = self.newNode(data)
        node.parent = self
        if self.children == None:
            self.children = LinkedList2()   
        self.children.addFirst(node)
        return node

    def addChildLast(self, data) :
        node = self.newNode(data)
        node.parent = self
        if self.children == None:
            self.children = LinkedList2()   
        self.children.addLast(node)
        return node
        
    #returns a naryNode2, not a node in linkedlist
    def getChild(self, idx):
        return self.children.getNode(idx).data

    def removeAll(self):  		#this removes all inter-referencing of nodes
        node = self.children
        if not node == None:
            node = node.firstNode
            while not node == None:
                node.data.removeAll()  #node.data is a naryNode2
                node = node.next
        #print('remove', self.data)
        self.data = None
        self.parent = None
        self.children = None        

    #returns a naryNode2, not a node in linkedlist
    def findNodeInChildrenByNode(self, data):
        node = self.children
        if node == None:
            return None
        node = node.firstNode
        while not node == None:
            if data == node.data:       #node.data is a naryNode2
                return node.data
            node = node.next
        return None
        
    #returns a naryNode2, not a node in linkedlist
    def findNodeInChildrenByData(self, data):
        node = self.children
        if node == None:
            return None
        node = node.firstNode
        while not node == None:
            if data == node.data.data:      #node.data is a naryNode2
                return node.data
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
        
    def delNodeInChildren(self, node) :
        linkedListNode = self.children.findNode(node)
        self.children.delete(linkedListNode)

    def dumpAsXml(self) :
        print('<data>')
        print(self.data)
        print('</data>')
           
        node = self.children.firstNode
        while not node == None:
            print('<child>')
            node.data.dumpAsXml()        
            print('</child>')
            node = node.next

    def test(self):
        self.addChildLast(1)
        self.dump(0)        

    def test1(self):
        
        for i in range(10) :
            self.addChildLast(i)
        
        self.dump(0)

        node = self.getChild(5)     
        print(node, node.data)        
        node = self.findNodeInChildrenByNode(node)        
        print(node, node.data)
        node = self.findNodeInChildrenByData(2)        
        print(node, node.data)
        
        self.createPath('memberA0', 'familyA')
        self.createPath('memberA1', 'familyA')
        self.createPath('memberB0', 'familyB')
        self.createPath('memberB1', 'familyB')
        self.createPath('memberC0', 'familyC')
        self.createPath('memberC1', 'familyC')
        self.createPath('memberCC1', 'familyC', 'memberC1')
        self.dump(0)        

        node = self.findNodeByPathName('familyC', 'memberC1', 'memberCC1')
        print(node, node.data)
        
        node.parent.delNodeInChildren(node)
        self.dump(0)        
        
        #self.dumpAsXml()



        
        

