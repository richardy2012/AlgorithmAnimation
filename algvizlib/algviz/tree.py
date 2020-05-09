#!/usr/bin/env python3

'''
二叉树节点的定义。
'''
class BinaryTreeNode:
    '''
    val:... 节点标签值（一般是整数）。
    '''
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        
    def _neighbors_(self):
        return (self.left, self.right)

'''
二叉树跟踪器的定义。
'''
class BinaryTreeTrace:
    '''
    graph:Graph 绑定要显示的图对象。
    color:(R,G,B) 跟踪器所在节点的RGB背景颜色。
    hold:bool 是否一直保留轨迹。
    node:BinaryTreeNode 初始化跟踪的二叉树节点。
    '''
    def __init__(self, graph, color, hold, node):
        self._graph = graph
        self._node = node
        self._color = color
        self._hold = hold
    
    def __getattribute__(self, name):
        pass
    
    def __setattr__(self, name, value):
        pass

'''
多叉树节点的定义。
'''
class MultiTreeNode:
    def __init__(self, val, children=list()):
        self.val = val
        self.children = children
        
    def _neighbors_(self):
        return self.children

'''
多叉树跟踪器的定义。
'''
class MultiTreeTrace:
    pass
