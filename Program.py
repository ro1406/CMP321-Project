# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 18:35:31 2022

@author: rohan
"""
class BinaryParseTree:
    class Node:
        def __init__(self, data, left=None, right=None):
            self.data, self.left, self.right = data, left, right
        def __str__(self): return self.data

    def __init__(self, root=None): self.root = root
    
    def fromList(self, list_repr):
        if not self.root:
            self.root=Node(None)
        def makeTree(currNode,listrep):
            if not currNode:
                return None
            
            currNode.data=listrep[0]
            
            if isinstance(listrep[1],str):
                currNode.left=listrep[1]
            else:#Its a nested list
                currNode
            
            if isinstance(listrep[2],str):
                currNode.right=listrep[2]
            
            return currNode
        
        self.root=makeTree(self.root,list_repr)
    
    def toList(self): pass # (part I)
    
    def prettyPrint(self): pass #
    
    def fromPrefix(self, expr=''): pass # to be implemented
    
    def fromInfix(self, expr=''): pass # (part II)
    
    def fromPostfix(self, expr=''): pass #
    
    def toPrefix(self): pass #
    
    def toInfix(self): pass #
    
    def toPostfix(self): pass #
    #def ??? # for list(tree)
    
    def nodesByLevel(self):
        if self.root == None: return []
        node = self.root
        bfsQueue, allNodes = [node], []
        while bfsQueue:
            node = bfsQueue.pop()
            allNodes.append(node.data)
            if node.left: bfsQueue.insert(0, node.left)
            if node.right: bfsQueue.insert(0, node.right)
        return allNodes
    
    def height(self):
        def __h(node):
            if node == None: return -1
            else: return 1 + max(__h(node.left), __h(node.right))
            
        return __h(self.root)


class XBinaryParseTree(BinaryParseTree): # to be implemented
    pass # (part III)


def test1(*args):
    for listrep in args:
        tree=BinaryParseTree().fromList(listrep)
        tree.prettyPrint() 
        assert tree.toList() == listrep
        
#Test Q1:

test1([['+', 'a', '1'],
       ['/', ['+', 'x', 'y'], '2'],
       ['*', 'A', ['+', 'B', ['^', 'C', 'D']]],
       #Convert these to prefix first:
       [(a+b)*(a-b)+(a+b)^2],
       [2*x^3*y^3-x^2-y^2]  ])
        
 
