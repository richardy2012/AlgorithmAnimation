#!/usr/bin/env python3

import svg_graph
import json

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
        return ((self.left, None), (self.right, None))

'''
二叉树跟踪器的定义。
'''
class BinaryTreeTrace:
    '''
    graph:SvgGraph 绑定要显示的图对象。
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
        self._graph.trace_visit(self._node, self._color, self._hold)
        if name == 'val':
            return self._node.val
        elif name == 'left':
            return self._node.left
        elif name == 'right':
            return self._node.right
    
    def __setattr__(self, name, value):
        self._graph.trace_visit(self._node, self._color, self._hold)
        if name == 'val':
            self._node.val = value
        elif name == 'left':
            self._graph.delete_node(self._node.left, True)
            self._graph.add_node(value, self._node, True)
            self._node.left = value
        elif name == 'right':
            self._graph.delete_node(self._node.right, True)
            self._graph.add_node(value, self._node, True)
            self._node.right = value

'''
tree:str 表示二叉树的字符串，必须给出树中的每个节点标签，空节点使用null代替。
返回：BinaryTreeNode 创建的二叉树的根节点。
'''
def parseBinaryTree(tree):
    node_vals = json.loads(tree)
    if len(node_vals) == 0:
        return None
    root = BinaryTreeNode(node_vals[0])
    node_queue = [root]
    index = 1
    while len(node_queue) > 0:
        cur_node = node_queue.pop(0)
        if index >= len(node_vals):
            break
        left_node = None
        if node_vals[index] is not None:
            left_node = BinaryTreeNode(node_vals[index])
        node_queue.append(left_node)
        if index+1 >= len(node_vals):
            break
        left_right = None
        if node_vals[index+1] is not None:
            right_node = BinaryTreeNode(node_vals[index+1])
        node_queue.append(right_node)
        if cur_node is not None:
            cur_node.left = left_node
            cur_node.right = right_node
        index += 2
    return root
    
'''
多叉树节点的定义。
'''
class MultiTreeNode:
    def __init__(self, val, children=list()):
        self.val = val
        self.children = children
        
    def _neighbors_(self):
        res = list()
        for child in self.children:
            res.append((child, None))
        return res

'''
多叉树跟踪器的定义。
'''
class MultiTreeTrace:
    pass
