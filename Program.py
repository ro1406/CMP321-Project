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
        #Assumes Prefix notation
        def makeTree(currNode,listrep):
            if isinstance(listrep,str):
                return self.Node(listrep)
            
            if not currNode:
                currNode=self.Node(listrep[0])
            else:
                currNode.data=listrep[0]
            currNode.left=makeTree(currNode.left,listrep[1])
            currNode.right=makeTree(currNode.right,listrep[2])
            
            return currNode
        
        self.root=makeTree(self.root,list_repr)
    
    def toList(self): 
        #Assumes Prefix notation
        def convert(currNode):
            if currNode.left is None and currNode.right is None:
                return currNode.data
            
            res=[currNode.data]
            if currNode.left:
                res.append(convert(currNode.left))
            if currNode.right:
                res.append(convert(currNode.right))
            return res                           
        return convert(self.root)
    
        
    def prettyPrint(self): 
        #Copied from: https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
        #To be changed
        root=self.root
        def height(root):
            return 1 + max(height(root.left), height(root.right)) if root else -1  
        nlevels = height(root)
        width =  pow(2,nlevels)
    
        q=[(root,0,width,'c')]
        levels=[]
    
        while(q):
            node,level,x,align= q.pop(0)
            if node:            
                if len(levels)<=level:
                    levels.append([])
            
                levels[level].append([node,level,x,align])
                seg= width//(pow(2,level+1))
                q.append((node.left,level+1,x-seg,'l'))
                q.append((node.right,level+1,x+seg,'r'))
    
        for i,l in enumerate(levels):
            pre=0
            preline=0
            linestr=''
            pstr=''
            seg= width//(pow(2,i+1))
            for n in l:
                valstr= str(n[0].data)
                if n[3]=='r':
                    linestr+=' '*(n[2]-preline-1-seg-seg//2)+ ' '*(seg +seg//2)+'\\'
                    preline = n[2] 
                if n[3]=='l':
                   linestr+=' '*(n[2]-preline-1)+'/' + ' '*(seg+seg//2)  
                   preline = n[2] + seg + seg//2
                pstr+=' '*(n[2]-pre-len(valstr))+valstr #correct the potition acording to the number size
                pre = n[2]
            print(linestr)
            print(pstr)   
        
        print('-'*95)
    
    
    def convertExprToList(self,expr):
        import re
        expr=re.sub('\(','[',expr)
        expr=re.sub('\)',']',expr)
        expr=re.sub( '([-/^+*]|[0-9]|[a-z])', r'"\1"' ,expr)
        expr=re.sub(" ",',',expr)
        arr=eval(expr) #Returns the array corresponding to expression
        return arr
    
    def convertListToExpr(self,arr):
        expr=str(arr)
        import re
        expr=re.sub('\[','(',expr)
        expr=re.sub('\]',')',expr)
        expr=re.sub( '"', '' ,expr)
        expr=re.sub( "'", '' ,expr)
        expr=re.sub(",",'',expr)
        return expr #Returns expression as defined by list
    
    def fromPrefix(self, expr=''): 
        #Expr example: '(/ (- a b) 3)' 
        #Raise exception for invalid expression TBD
        operators='/+*-^'
        if expr[1] not in operators: #First thing inside () should be an operator
            raise Exception
        #Convert to an array rep:
        arr=self.convertExprToList(expr)
        #Call fromList function with the list representation:
        self.fromList(arr)
        return self
        
    
    def fromInfix(self, expr=''):
        
        #Raise exception for invalid expression TBD
        def makeTree(currNode,listrep):
            if isinstance(listrep,str):
                return self.Node(listrep)
            
            if not currNode:
                currNode=self.Node(listrep[1])
            else:
                currNode.data=listrep[1]
            currNode.left=makeTree(currNode.left,listrep[0])
            currNode.right=makeTree(currNode.right,listrep[2])
            
            return currNode
        
        self.root=makeTree(self.root,self.convertExprToList(expr))
            
    
    def fromPostfix(self, expr=''):
        #Raise exception for invalid expression TBD
        def makeTree(currNode,listrep):
            if isinstance(listrep,str):
                return self.Node(listrep)
            
            if not currNode:
                currNode=self.Node(listrep[2])
            else:
                currNode.data=listrep[2]
            currNode.left=makeTree(currNode.left,listrep[0])
            currNode.right=makeTree(currNode.right,listrep[1])
            
            return currNode
        
        self.root=makeTree(self.root,self.convertExprToList(expr))
    
    def toPrefix(self):
        res=self.toList()
        return self.convertListToExpr(res)
    
    def toInfix(self):
        def convert(currNode):
            if currNode.left is None and currNode.right is None:
                return currNode.data
            
            res=[currNode.data]
            if currNode.left:
                res.insert(0,convert(currNode.left))
            if currNode.right:
                res.append(convert(currNode.right))
            return res                      
        
        res= convert(self.root)
        return self.convertListToExpr(res)
    
    def toPostfix(self):
        def convert(currNode):
            if currNode.left is None and currNode.right is None:
                return currNode.data
            
            res=[]
            if currNode.left:
                res.append(convert(currNode.left))
            if currNode.right:
                res.append(convert(currNode.right))
            res.append(currNode.data)
            return res                      
        
        res= convert(self.root)
        return self.convertListToExpr(res)
        
        
        
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
    #Rearrange the expression into infix notation and then call self.fromInfix :)


def test1(*args):
    for listrep in args:
        tree=BinaryParseTree()
        tree.fromList(listrep)
        tree.prettyPrint() 
        assert tree.toList() == listrep
        
#Test Q1:

test1(['+', 'a', '1'],
        ['/', ['+', 'x', 'y'], '2'],
        ['*', 'A', ['+', 'B', ['^', 'C', 'D']]],
        ['+',['*',['+','a','b'],['-','a','b']],['^',['+','a','b'],'2']],
        ['-',['*','2',['*',['^','x','3'],['^','y','3']]],['-',['^','x','2'],['^','y','2']]] )




print("Trying from prefix:")
tree=BinaryParseTree()
tree.fromPrefix('(* a (+ b (^ c d)))')
tree.prettyPrint()
print("Prefix expression:")
print("True val:",'(* a (+ b (^ c d)))')
print("Result:",tree.toPrefix())

print("Trying from infix:")
tree=BinaryParseTree()
tree.fromInfix('(a * (b + (c ^ d)))')
tree.prettyPrint()
print("Infix expression:")
print("True val:",'(a * (b + (c ^ d)))')
print("Result:",tree.toInfix())


print("Trying from postfix:")
tree=BinaryParseTree()
tree.fromPostfix('(a (b (c d ^) +) *)')
tree.prettyPrint()
print("Postfix expression:")
print("True val:",'(a (b (c d ^) +) *)')
print("Result:",tree.toPostfix())

        
 
