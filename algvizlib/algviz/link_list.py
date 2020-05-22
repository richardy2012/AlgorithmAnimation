#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

import json

'''
单向链表节点定义。
'''
class ListNode():
    '''
    val:... 链表节点上要显示的标签值。
    '''
    def __init__(self, val):
        self._bind_graphs = set()
        self.val = val
        self.next = None

    '''
    name:str 访问跟踪器的属性，以及跟踪器所绑定单向链表的val,next属性。
    '''
    def __getattribute__(self, name):
        if name == 'val':
            for gra in self._bind_graphs:
                gra.visit_node(self)
            return super().__getattribute__('val')
        elif name == 'next':
            node = super().__getattribute__('next')
            for gra in self._bind_graphs:
                gra.visit_node(self, node)
            return node
        else:
            return super().__getattribute__(name)
    
    '''
    name:str 修改跟踪器的属性，以及跟踪器所绑定单向链表的val,next属性。
    value:... 新的赋值（对于val,next属性是直接赋值给跟踪器所绑定单向链表中对应的属性）。
    '''
    def __setattr__(self, name, value):
        if name == 'val':
            super().__setattr__('val', value)
            for gra in self._bind_graphs:
                gra.visit_node(self, set_val=True)
        elif name == 'next':
            super().__setattr__(name, value)
            for gra in self._bind_graphs:
                gra.add_node(value)
                gra.visit_node(self, value, set_val=True)
        else:
            super().__setattr__(name, value)
    
    '''
    功能：格式化树节点。
    '''
    def __str__(self):
        return str(super().__getattribute__('val'))
    
    '''
    返回：下一个节点。
    '''
    def _neighbors_(self):
        next_node = super().__getattribute__('next')
        return [(next_node, None)]
    
    '''
    gra:SvgGraph 要添加的该节点绑定的拓扑图对象。
    '''
    def _add_graph_(self, gra):
        self._bind_graphs.add(gra)
    
    '''
    gra:SvgGraph 要移除的该节点绑定的拓扑图对象。
    '''
    def _remove_graph_(self, gra):
        if gra in self._bind_graphs:
            self._bind_graphs.remove(gra)

'''
li_str:str 表示单向链表的字符串，必须给出链表中每个节点的标签，空节点使用null代替。
返回：ForwardListNode 创建的单向链表的根节点。
'''
def parseLinkList(li_str):
    li_vals = json.loads(li_str)
    if len(li_vals) == 0:
        return None
    head = ListNode(li_vals[0])
    cur_node = head
    for i in range(1, len(li_vals)):
        cur_node.next = ListNode(li_vals[i])
        cur_node = cur_node.next
    return head
