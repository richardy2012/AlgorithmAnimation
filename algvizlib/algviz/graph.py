#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

import utility as util

'''
拓扑图的邻居节点迭代器。
'''
class GraphNeighborIter():
    def __init__(self, node, bind_graphs, neighbors):
        self._node = node
        self._bind_graphs = bind_graphs
        self._neighbors = neighbors
        self._next_index = 0
    
    def __iter__(self):
        self._next_index = 0
        return self
    
    def __next__(self):
        if self._next_index >= len(self._neighbors):
            raise StopIteration
        else:
            neighbor = self._neighbors[self._next_index]
            self._next_index += 1
            for gra in self._bind_graphs:
                gra.markEdge(self._node, neighbor[0], util._getElemColor, hold=False)
            return neighbor

'''
拓扑图节点的定义。
'''
class GraphNode():
    '''
    val:... 节点上显示的标签。
    '''
    def __init__(self, val):
        super().__setattr__('val', val)
        super().__setattr__('_neighbors', list())
        super().__setattr__('_bind_graphs', set())
    
    '''
    功能：格式化树节点。
    '''
    def __str__(self):
        return str(super().__getattribute__('val'))
    
    '''
    name:str 访问跟踪器的属性，以及跟踪器所绑定拓扑图节点的val属性。
    '''
    def __getattribute__(self, name):
        if name == 'val':
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markNode(self, util._getElemColor, hold=False)
            return super().__getattribute__('val')
        else:
            return super().__getattribute__(name)
    
    '''
    name:str 修改跟踪器的属性，以及跟踪器所绑定拓扑图节点的val属性。
    value:... 新的赋值（对于val属性是直接赋值给跟踪器所绑定拓扑图节点中对应的属性）。
    '''
    def __setattr__(self, name, value):
        if name == 'val':
            super().__setattr__('val', value)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra._updateNodeLabel(self, value)
                gra.markNode(self, util._setElemColor, hold=False)
        else:
            super().__setattr__(name, value)

    '''
    功能：返回所有邻居节点。
    '''
    def neighbors(self):
        iter_neighbors = super().__getattribute__('_neighbors')
        bind_graphs = super().__getattribute__('_bind_graphs')
        return GraphNeighborIter(self, bind_graphs, iter_neighbors)
    
    '''
    功能：向最后一个邻居点后添加一个节点。
    node:GraphNode 要添加的节点对象。
    weight:... 边上的权重值。
    '''
    def append(self, node, weight=None):
        pos = self._get_node_index_(node)
        if pos == -1:
            neighbors_ = super().__getattribute__('_neighbors')
            neighbors_.append([node, weight])
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.addNode(node)
                gra.markEdge(self, node, util._setElemColor, hold=False)
    
    '''
    功能：向某个邻居节点前插入一个节点。
    node:GraphNode 要添加的节点对象。
    ref_node:GraphNode 在该节点之前插入。
    weight:... 边上的权重值。
    '''
    def insertBefore(self, node, ref_node, weight=None):
        pos = self._get_node_index_(ref_node)
        pos2 = self._get_node_index_(node)
        if pos != -1 and pos2 == -1:
            neighbors_ = super().__getattribute__('_neighbors')
            neighbors_.insert(pos, [node, weight])
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.addNode(node)
                gra.markEdge(self, node, util._setElemColor, hold=False)
    
    '''
    功能：替换某一个邻居节点。
    new_node:GraphNode 新的节点。
    old_node:GraphNode 旧的节点。
    weight:... 边上的权重值。
    '''
    def replace(self, new_node, old_node, weight=None):
        pos = self._get_node_index_(old_node)
        if pos != -1:
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markEdge(self, old_node, util._setElemColor, hold=False)
            pos2 = self._get_node_index_(new_node)  # 检测new_node是否已经是当前节点的邻居节点。
            if pos2 == -1:
                neighbors_ = super().__getattribute__('_neighbors')
                neighbors_[pos] = [new_node, weight]
                for gra in bind_graphs:
                    gra.addNode(new_node)
                    gra.markEdge(self, new_node, util._setElemColor, hold=False)
            else:
                neighbors_.pop(pos)
    
    '''
    功能：移除一个邻居节点。
    node:GraphNode 要移除的节点。
    '''
    def remove(self, node):
        pos = self._get_node_index_(node)
        if pos != -1:
            neighbors_ = super().__getattribute__('_neighbors')
            neighbors_.pop(pos)
            bind_graphs = super().__getattribute__('_bind_graphs')
            for gra in bind_graphs:
                gra.markEdge(self, node, util._setElemColor, hold=False)
    
    '''
    node:GraphNode 要定位的节点对象。
    返回:int node节点在neighbors中的索引位置。
    '''
    def _get_node_index_(self, node):
        neighbors_ = super().__getattribute__('_neighbors')
        for i in range(len(neighbors_)):
            if neighbors_[i][0] == node:
                return i
        return -1
                    
    '''
    返回：所有邻居节点和邻居边的权重值。
    '''
    def _neighbors_(self):
        return super().__getattribute__('_neighbors')
           
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
功能：更新两个节点之间边上的权重值。
node1/node2:GraphNode 要更新的邻居节点对象。
weight:... 新的权重值。
'''
def updateEdgeWeight(node1, node2, weight):
    pos1 = node1._get_node_index_(node2)
    pos2 = node2._get_node_index_(node1)
    if pos1 != -1:
        node1._neighbors[pos1][1] = weight
        for gra in node1._bind_graphs:
            gra._updateEdgeLabel(node1, node2, weight)
            gra.markEdge(node1, node2, util._setElemColor, hold=False)
    if pos2 != -1:
        node2._neighbors[pos2][1] = weight
        for gra in node2._bind_graphs:
            gra._updateEdgeLabel(node2, node1, weight)
            gra.markEdge(node2, node1, util._setElemColor, hold=False)
    
'''
edges:list(tuple/list) 表示拓扑图中的所有边（eg:[[0, 1], [1, 2], [2, 0]]）。
nodes:list(tuple/list) 表示拓扑图中的节点信息和节点上的标签（eg:[[0, 1], [1, 2], [2, 3]]）。
directed:bool 该拓扑图是否为有向图。
返回：dict 拓扑图中所有节点的集合（key:节点id, value:节点对象）。
'''
def parseGraph(edges_, nodes_=None, directed=True):
    res = dict()
    # 创建拓扑图节点。
    if nodes_ is not None:
        for nid, val in nodes_:
            res[nid] = GraphNode(val)
    else:
        for edge in edges_:
            if edge[0] not in res.keys():
                res[edge[0]] = GraphNode(edge[0])
            if edge[1] not in res.keys():
                res[edge[1]] = GraphNode(edge[1])
    # 为拓扑图添加边。
    for edge in edges_:
        n1id, n2id, weight = None, None, None
        if len(edge) == 3:
            n1id, n2id, weight = edge
        elif len(edge) == 2:
            n1id, n2id = edge
        if n1id in res.keys() and n2id in res.keys():
            res[n1id].append(res[n2id], weight)
            if directed == False:
                res[n2id].append(res[n1id], weight)
    return res
