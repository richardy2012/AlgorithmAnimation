#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

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
    
    '''
    返回：左右子节点。
    '''
    def _neighbors_(self):
        return ((self.left, None), (self.right, None))

'''
二叉树跟踪器的定义。
'''
class BinaryTreeTrace:
    '''
    node:BinaryTreeNode 初始化跟踪的二叉树节点。
    graph:SvgGraph 绑定要显示的图对象。
    color:(R,G,B) 跟踪器所在节点的RGB背景颜色。
    hold:bool 是否一直保留轨迹。
    '''
    def __init__(self, node, graph, color, hold):
        self._graph = graph
        self._node = node
        self._color = color
        self._hold = hold
        if node is not None:
            self._graph.add_node(node)
            self._graph.trace_visit(self._node, self._color, self._hold)
    
    '''
    功能：清除图中跟踪器的轨迹记录。
    '''
    def __del__(self):
        self._graph.delete_trace(self._color, self._hold)
    
    '''
    node:BinaryTreeNode 为跟踪器绑定新的二叉树节点。
    '''
    def __call__(self, node):
        if type(node) == BinaryTreeTrace:
            node = node._node
        super().__setattr__('_node', node)
        self._graph.add_node(node)
        self._graph.trace_visit(node, self._color, self._hold)
        return self
    
    '''
    other:BinaryTreeNode 判断跟踪器所绑定的节点和other是否相同。
    '''
    def __eq__(self, other):
        return super().__getattribute__('_node') == other
    
    '''
    other:BinaryTreeNode 判断跟踪器所绑定的节点和other是否不同。
    '''
    def __ne__(self, other):
        return super().__getattribute__('_node') != other 
    
    '''
    name:str 访问跟踪器的属性，以及跟踪器所绑定二叉树的节点val,left,right属性。
    '''
    def __getattribute__(self, name):
        if name == 'val':
            return super().__getattribute__('_node').val
        elif name == 'left':
            return super().__getattribute__('_node').left
        elif name == 'right':
            return super().__getattribute__('_node').right
        else:
            return super().__getattribute__(name)
    
    '''
    name:str 修改跟踪器的属性，以及跟踪器所绑定二叉树的节点val,left,right属性。
    value:... 新的赋值（对于val,left,right属性是直接赋值给跟踪器所绑定二叉树中对应的属性）。
    '''
    def __setattr__(self, name, value):
        if name == 'val':
            setattr(self._node, 'val', value)
            self._graph.update_node_label(self._node, value)
        elif name == 'left':
            if type(value) == BinaryTreeTrace:
                value = value._node
            self._graph.add_node(value)
            setattr(self._node, 'left', value)
        elif name == 'right':
            if type(value) == BinaryTreeTrace:
                value = value._node
            self._graph.add_node(value)
            setattr(self._node, 'right', value)
        else:
            super().__setattr__(name, value)

'''
tree_str:str 表示二叉树的字符串，必须给出树中的每个节点标签，空节点使用null代替。
返回：BinaryTreeNode 创建的二叉树的根节点。
'''
def parseBinaryTree(tree_str):
    node_vals = json.loads(tree_str)
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
