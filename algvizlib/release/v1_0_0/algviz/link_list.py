#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

import json

'''
单向链表节点定义。
'''
class ForwardListNode():
    '''
    val:... 链表节点上要显示的标签值。
    '''
    def __init__(self, val):
        self.val = val
        self.next = None

    '''
    返回：下一个节点。
    '''
    def _neighbors_(self):
        return [(self.next, None)]
        
'''
单向链表跟踪器定义。
'''
class ForwardListTrace():
    '''
    node:ForwardListNode 初始化的单向链表节点。
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
    node:ForwardListNode 为跟踪器绑定新的单向链表节点。
    '''
    def __call__(self, node):
        if type(node) == ForwardListTrace:
            node = node._node
        super().__setattr__('_node', node)
        self._graph.add_node(node)
        self._graph.trace_visit(node, self._color, self._hold)
        return self
    
    '''
    other:ForwardListNode 判断跟踪器所绑定的节点和other是否相同。
    '''
    def __eq__(self, other):
        return super().__getattribute__('_node') == other
    
    '''
    other:ForwardListNode 判断跟踪器所绑定的节点和other是否不同。
    '''
    def __ne__(self, other):
        return super().__getattribute__('_node') != other 
    
    '''
    name:str 访问跟踪器的属性，以及跟踪器所绑定单向链表的val,next属性。
    '''
    def __getattribute__(self, name):
        if name == 'val':
            return super().__getattribute__('_node').val
        elif name == 'next':
            return super().__getattribute__('_node').next
        else:
            return super().__getattribute__(name)
    
    '''
    name:str 修改跟踪器的属性，以及跟踪器所绑定单向链表的val,next属性。
    value:... 新的赋值（对于val,next属性是直接赋值给跟踪器所绑定单向链表中对应的属性）。
    '''
    def __setattr__(self, name, value):
        if name == 'val':
            setattr(self._node, 'val', value)
            self._graph.update_node_label(self._node, value)
        elif name == 'next':
            if type(value) == ForwardListTrace:
                value = value._node
            self._graph.add_node(value)
            setattr(self._node, 'next', value)
        else:
            super().__setattr__(name, value)

'''
li_str:str 表示单向链表的字符串，必须给出链表中每个节点的标签，空节点使用null代替。
返回：ForwardListNode 创建的单向链表的根节点。
'''
def parseForwardListNodes(li_str):
    li_vals = json.loads(li_str)
    if len(li_vals) == 0:
        return None
    head = ForwardListNode(li_vals[0])
    cur_node = head
    for i in range(1, len(li_vals)):
        cur_node.next = ForwardListNode(li_vals[i])
        cur_node = cur_node.next
    return head
