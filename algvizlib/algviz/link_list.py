#!/usr/bin/env python3

'''
单向链表节点定义。
'''
class ForwardListNode():
    def __init__(self, val):
        self.val = val
        self.next = None

    def _neighbors_(self):
        return ((self.next, None))
        
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
        
    def __call__(self, node):
        super().__setattr__('_node', node)
        self._graph.add_node(node, None, False)
        return self
    
    def __eq__(self, other):
        return super().__getattribute__('_node') == other
    
    def __ne__(self, other):
        return super().__getattribute__('_node') != other 
    
    def __getattribute__(self, name):
        if name == 'val':
            self._graph.trace_visit(super().__getattribute__('_node'), super().__getattribute__('_color'), super().__getattribute__('_hold'))
            return super().__getattribute__('_node').val
        elif name == 'next':
            return super().__getattribute__('_node').next
        else:
            return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        if name == 'val':
            setattr(self._node, 'val', value)
            self._graph.trace_visit(super().__getattribute__('_node'), super().__getattribute__('_color'), super().__getattribute__('_hold'))
        elif name == 'next':
            self._graph.delete_node(super().__getattribute__('_node').next, True)
            setattr(self._node, 'right', value)
            self._graph.add_node(value, super().__getattribute__('_node'), True)
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
    return cur_node
