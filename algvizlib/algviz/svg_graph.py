#!/usr/bin/env python3

import graphviz
import xml.dom.minidom as xmldom
import utility as util

class SvgGraph(): 
    '''
    data:... 拓扑图的初始化数据，可以是图/树/链表的节点，也可以是表示邻接表的list。
    directed:bool 表示拓扑图是否为有向图。
    '''
    def __init__(self, data, directed):
        self._next_node_id = 0          # 记录所有新增的节点。
        self._directed = directed       # 拓扑图是否为有向图。
        self._addr_node = dict()        # 拓扑图节点地址到节点编号的映射。
        self._node_label = dict()       # 拓扑图每个节点上要显示的标签信息。
        self._edge_label = dict()       # 拓扑图的所有边上的标签信息。
        self._node_tcs = dict()         # 记录所有节点中的轨迹访问信息（节点索引：ColorStack）信息。
        self._frame_trace_old = list()  # 缓存上一帧需要清除的节点相关信息（节点索引，轨迹颜色值）。
        self._frame_trace = list()      # 记录下一帧待刷新的节点相关信息(节点索引，轨迹颜色值，是否持久化)。
        self._node_appear = list()      # 记录下一帧动画中出现的节点索引集合。
        self._node_disappear = list()   # 记录下一帧动画中消失的节点索引集合。
        self._old_svg = None            # 上一帧显示的拓扑图的svg对象记录。
        self._svg = None                # 将要显示的拓扑图的svg对象。

    '''
    node:... 要添加的节点对象，可以是拓扑图/树/链表节点。
    recur:bool 是否递归的添加和node相关联的节点。
    '''
    def add_node(self, node, recur):
        visited = set()
        node_stack = [node]
        while len(node_stack) > 0:
            cur_node = node_stack.pop()
            cur_node_id = id(cur_node)
            if cur_node_id not in visited:
                visited.add(cur_node_id)
            self._addr_node[cur_node_id] = self._next_node_id
            self._node_label[self._next_node_id] = cur_node.val
            self._node_appear.append(self._next_node_id)
            # TODO 处理边。
            self._next_node_id += 1
            for neigh in cur_node._neighbors_():
                node_stack.append(neigh)
    
    '''
    node:... 要删除的节点对象，可以是拓扑图/树/链表节点。
    recur:bool 是否递归的删除和node相关联的节点。
    '''
    def delete_node(self, node, recur):
        pass
    
    '''
    nid:int 访问的节点对象的id值，可以是拓扑图/树/链表节点。
    color:(R,G,B) 跟踪器的颜色。
    hold:bool 是否保留轨迹颜色。
    '''
    def visit_node(self, nid, color, hold):
        pass
    
    '''
    color:(R,G,B) 将要被删除的跟踪器颜色。
    hold:bool 是否保留轨迹颜色。
    '''
    def delete_trace(self, color, hold):
        pass
    
    '''
    返回:str 拓扑图SVG显示字符串。
    '''
    def __repr_svg__(self):
        pass
    
    '''
    功能：更新拓扑图中各个节点的位置。
    返回:xmldom.Document 经过graphviz排版后拓扑图。
    '''
    def _update_svg_(self):
        dot = None
        if self._directed:
            dot = graphviz.Digraph(format='svg')
        else:
            dot = graphviz.Graph(format='svg')
        for (node, label) in self._node_label:
            fill_color = self._node_tcs[node].color()
            dot.node(name='{}'.format(gid), label=label, fillcolor=fill_color, shape='circle')
        # TODO 添加边，返回解析的对象。
    