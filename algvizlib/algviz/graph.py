#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

import json

'''
拓扑图节点的定义。
'''
class GraphNode():
    '''
    val:... 节点上显示的标签。
    '''
    def __init__(self, val):
        self._bind_graph = dict()
        self.val = val
        self.neighbors = list()
        self.weights = list()
    
    '''
    返回：跟踪器所跟踪的图节点中邻居的数量。
    '''
    def __len__(self):
        return len(self.neighbors)
    
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
            for gra in self._bind_graphs:
                gra.visit_node(self)
            return super().__getattribute__('_node').val
        else:
            return super().__getattribute__(name)
    
    '''
    name:str 修改跟踪器的属性，以及跟踪器所绑定拓扑图节点的val属性。
    value:... 新的赋值（对于val属性是直接赋值给跟踪器所绑定拓扑图节点中对应的属性）。
    '''
    def __setattr__(self, name, value):
        if name == 'val':
            super().__setattr__('val', value)
            for gra in self._bind_graphs:
                gra.visit_node(self, set_val=True)
        else:
            super().__setattr__(name, value)

    '''
    index:int 要获取的绑定节点的第index个子节点的索引。
    返回：GraphNode[edge_info] 对应子节点和对应边上权重信息。
    '''
    def __getitem__(self, index):
        node = super().__getattribute__('_node')
        if node.weights[index] is not None:
            return (node.neighbors[index], node.weights[index])
        else:
            return node.neighbors[index]
    
    '''
    index:int 要修改的子节点的索引，如果index大于子节点列表长度，则添加子节点。
    value:GraphNode[weight] 新的拓扑图节点值[对应边上的权重值]（value中node为None则代表删除节点）。
    '''
    def __setitem__(self, index, value):
        if index < 0:
            raise Exception('Graph index out of range!')
        node = super().__getattribute__('_node')
        child_node, child_edge = None, None
        if type(value) == tuple:
            child_node, child_edge = value[0], value[1]
        else:
            child_node = value
        if index >= len(node.neighbors):
            if child_node is not None:
                self._graph.add_node(child_node)
                node.neighbors.append(child_node)
                node.weights.append(child_edge)
        else:
            self._graph.add_node(child_node)
            node.neighbors[index] = child_node
            node.weights[index] = child_edge
    
    '''
    返回：所有邻居节点和邻居边的权重值。
    '''
    def _neighbors_(self):
        res = list()
        for i in range(len(self.neighbors)):
            res.append((self.neighbors[i], self.weights[i]))
        return res
    
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
node_str:json字符串 表示拓扑图中的节点信息和节点上的标签（eg:[[0, 1], [1, 2], [2, 3]]）。
edge_str:json字符串 表示拓扑图中的所有边（eg:[[0, 1], [1, 2], [2, 0]]）。
directed:bool 该拓扑图是否为有向图。
返回：dict 拓扑图中所有节点的集合（key:节点id, value:节点对象）。
'''
def parseGraph(node_str, edge_str, directed=True):
    nodes = json.loads(node_str)
    edges = json.loads(edge_str)
    res = dict()
    for node in nodes:
        nid, val = None, None
        if type(node) == list:
            nid, val = node
        else:
            nid = node
        res[nid] = GraphNode(val)
    for edge in edges:
        n1id, n2id, weight = None, None, None
        if len(edge) == 3:
            n1id, n2id, weight = edge
        elif len(edge) == 2:
            n1id, n2id = edge
        if n1id in res.keys() and n2id in res.keys():
            res[n1id].neighbors.append(res[n2id])
            res[n1id].weights.append(weight)
            if directed == False:
                res[n2id].neighbors.append(res[n1id])
                res[n2id].weights.append(weight)
    return res
