#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

from . import utility as util

'''
二叉树节点的定义。
'''
class TreeNode:
    '''
    val:... 节点标签值（一般是整数）。
    '''
    def __init__(self, val):
        super().__setattr__('val', val)
        super().__setattr__('left', None)
        super().__setattr__('right', None)
        super().__setattr__('_bind_graphs', set())
    
    '''
    name:str 访问跟踪器的属性，以及跟踪器所绑定二叉树的节点val,left,right属性。
    '''
    def __getattribute__(self, name):
        if name == 'val':
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markNode(self, util._getElemColor, hold=False)
            return super().__getattribute__('val')
        elif name == 'left' or name == 'right':
            node = super().__getattribute__(name)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markEdge(self, node, util._getElemColor, hold=False)
            return node
        else:
            return super().__getattribute__(name)
    
    '''
    name:str 修改跟踪器的属性，以及跟踪器所绑定二叉树的节点val,left,right属性。
    value:... 新的赋值（对于val,left,right属性是直接赋值给跟踪器所绑定二叉树中对应的属性）。
    '''
    def __setattr__(self, name, value):
        if name == 'val':
            super().__setattr__('val', value)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra._updateNodeLabel(self, value)
                gra.markNode(self, util._setElemColor, hold=False)
        elif name == 'left' or name == 'right':
            # 标记旧边。
            node = super().__getattribute__(name)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markEdge(self, node, util._setElemColor, hold=False)
            # 标记新边。
            super().__setattr__(name, value)
            for gra in bind_graphs:
                gra.addNode(value)
                gra.markEdge(self, value, util._setElemColor, hold=False)
        else:
            super().__setattr__(name, value)
    
    '''
    功能：格式化树节点。
    '''
    def __str__(self):
        return str(super().__getattribute__('val'))
    
    '''
    返回：左右子节点。
    '''
    def _neighbors_(self):
        left_node = super().__getattribute__('left')
        right_node = super().__getattribute__('right')
        return ((left_node, None), (right_node, None))
    
    '''
    gra:SvgGraph 要添加的该节点绑定的拓扑图对象。
    '''
    def _add_graph_(self, gra):
        bind_graphs = super().__getattribute__('_bind_graphs')
        bind_graphs.add(gra)
    
    '''
    gra:SvgGraph 要移除的该节点绑定的拓扑图对象。
    '''
    def _remove_graph_(self, gra):
        bind_graphs = super().__getattribute__('_bind_graphs')
        if gra in bind_graphs:
            bind_graphs.remove(gra)

'''
node_vals:list 必须给出树中的每个节点标签，空节点使用None代替。
返回：BinaryTreeNode 创建的二叉树的根节点。
'''
def parseTree(node_vals):
    if len(node_vals) == 0:
        return None
    root = TreeNode(node_vals[0])
    node_queue = [root]
    index = 1
    while len(node_queue) > 0:
        cur_node = node_queue.pop(0)
        if index >= len(node_vals):
            break
        left_node = None
        if node_vals[index] is not None:
            left_node = TreeNode(node_vals[index])
        node_queue.append(left_node)
        if index+1 >= len(node_vals):
            break
        left_right = None
        if node_vals[index+1] is not None:
            right_node = TreeNode(node_vals[index+1])
        node_queue.append(right_node)
        if cur_node is not None:
            cur_node.left = left_node
            cur_node.right = right_node
        index += 2
    return root
