# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 18:35:31 2022

@author: rohan
"""

#Custom exception

class IncorrectFormat(Exception):
    def __init__(self):
        super().__init__('[Error] Incorrect format supplied!')

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
        
        #Convert expression to list rep
        arr=self.convertExprToList(expr)
        
        operators='/+*-^'
        if arr[0] not in operators: #First thing inside () should be an operator
            raise IncorrectFormat
    
        #Call fromList function with the list representation:
        self.fromList(arr)
        return self
        
    
    def fromInfix(self, expr=''):
        
        operators='/+*-^'
        arr=self.convertExprToList(expr)
        if arr[1] not in operators: #First thing inside () should be an operator
            raise IncorrectFormat
        
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
        
        self.root=makeTree(self.root,arr)
        return self
    
    def fromPostfix(self, expr=''):
        
        operators='/+*-^'
        arr=self.convertExprToList(expr)

        if arr[2] not in operators: #First thing inside () should be an operator
            raise IncorrectFormat
            
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
        
        self.root=makeTree(self.root,arr)
        return self
    
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
        
        
    def __iter__(self):# For list(tree)
        import re
        return iter(re.sub(r'[() ]','',self.toPrefix())) # Remove all the spaces and parenthesis from the string
        
        
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


class XBinaryParseTree(BinaryParseTree):
    def __init__(self, root=None):
        super().__init__(root)
    
    def convertExprToList(self,expr):
        import re
        expr=re.sub('\(','[',expr)
        expr=re.sub('\)',']',expr)
        expr=re.sub( '([-/^+*><?:]|[0-9]|[a-z])', r'"\1"' ,expr) #Added operators
        expr=re.sub(" ",',',expr)
        arr=eval(expr) #Returns the array corresponding to expression
        return arr 
    
    def fromInfix(self, expr=''):
        
        operators='/+*-^?:<>'
        arr=self.convertExprToList(expr)
        if arr[1] not in operators: #First thing inside () should be an operator
            raise IncorrectFormat
        
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
        
        self.root=makeTree(self.root,arr)
        return self
    


#####################################################################################

def test1(*args):
    for listrep in args:
        print("Input:",listrep)
        tree=BinaryParseTree()
        tree.fromList(listrep)
        tree.prettyPrint() 
        assert tree.toList() == listrep
        
#Test Q1:
print('='*90)
print(' '*40,"Part 1")
print('='*90)

test1(['+', 'a', '1'],
        ['/', ['+', 'x', 'y'], '2'],
        ['*', 'A', ['+', 'B', ['^', 'C', 'D']]],
        ['+',['*',['+','a','b'],['-','a','b']],['^',['+','a','b'],'2']],
        ['-',['*','2',['*',['^','x','3'],['^','y','3']]],['-',['^','x','2'],['^','y','2']]] )


#Test Q2:

print('='*90)
print(' '*40,"Part 2")
print('='*90)    

def test2(*args):
    for listrep in args:
        tree=BinaryParseTree()
        print(listrep,':')
        print('    Infix:',tree.fromPrefix(listrep).toInfix())
        print('    Prefix:',tree.fromPrefix(listrep).toPrefix())
        print('    Postfix:',tree.fromPrefix(listrep).toPostfix())
        print()
        assert tree.fromPrefix(listrep).toPrefix() == listrep
   
  
test2('(+ a 1)',
        '(/ (+ x y) 2)',
        '(* a (+ b (^ c d)))',
        '(+ (* (+ a b) (- a b)) (^ (+ a b) 2))',
        '(- (* 2 (* (^ x 3) (^ y 3))) (- (^ x 2) (^ y 2)))' )

#Trying list(tree)
print("-"*90)
print("List(t) where t=BinaryParseTree().fromPostfix('(n 4 ^)') yields: ")
print(list(BinaryParseTree().fromPostfix('(n 4 ^)')))
print("-"*90)


#Test Q3:

print('='*90)
print(' '*40,"Part 3")
print('='*90)    

def test3(*args):
    for expr in args:
        tree=XBinaryParseTree()
        tree.fromInfix(expr)
        tree.prettyPrint()
        toInfixResult=tree.toInfix()
        print(toInfixResult)
        print("Infix list representation:")
        print(tree.convertExprToList(toInfixResult))
        print()
        assert toInfixResult==expr

test3('((a > b) ? (a : b))',
      '((x > (2 * y)) ? ((x + y) : (x - y)))', #Unary op for last part?
      '((a > b) ? (((a - b) ^ 2) : ((a + b) ^ 2)))')


