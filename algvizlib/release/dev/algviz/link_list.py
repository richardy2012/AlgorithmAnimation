#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

from . import utility as util

'''
单向链表节点定义。
'''
class ListNode():
    '''
    val:... 链表节点上要显示的标签值。
    '''
    def __init__(self, val):
        super().__setattr__('val', val)
        super().__setattr__('next', None)
        super().__setattr__('_bind_graphs', set())

    '''
    name:str 访问跟踪器的属性，以及跟踪器所绑定单向链表的val,next属性。
    '''
    def __getattribute__(self, name):
        if name == 'val':
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markNode(util._getElemColor, self, hold=False)
            return super().__getattribute__('val')
        elif name == 'next':
            node = super().__getattribute__('next')
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markEdge(util._getElemColor, self, node, hold=False)
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
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra._updateNodeLabel(self, value)
                gra.markNode(util._setElemColor, self, hold=False)
        elif name == 'next':
            # 标记旧边。
            node = super().__getattribute__(name)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markEdge(util._setElemColor, self, node, hold=False)
            # 标记新边。
            super().__setattr__(name, value)
            for gra in bind_graphs:
                gra.addNode(value)
                gra.markEdge(util._setElemColor, self, value, hold=False)
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
li_str:list 必须给出链表中每个节点的标签，空节点使用null代替。
返回：ForwardListNode 创建的单向链表的根节点。
'''
def parseLinkList(li_vals):
    if len(li_vals) == 0:
        return None
    head = ListNode(li_vals[0])
    cur_node = head
    for i in range(1, len(li_vals)):
        cur_node.next = ListNode(li_vals[i])
        cur_node = cur_node.next
    return head
