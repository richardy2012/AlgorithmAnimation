#!/usr/bin/env python3

import json

'''
拓扑图节点的定义。
'''
class GraphNode():
    '''
    val:... 节点上显示的标签。
    neighbors:list(GraphNode) 该节点所有的邻居节点。
    edge_infos:list(...) 该节点与邻居节点所构成边上的信息值。
    '''
    def __init__(self, val, neighbors=list(), edge_infos=None):
        self.val = val
        self.neighbors = neighbors
        self.edge_infos = edge_infos
    
    '''
    返回：所有邻居节点和邻居边的权重值。
    '''
    def _neighbors_(self):
        res = list()
        for i in range(len(self.neighbors)):
            if self.edge_infos is None:
                res.append((self.neighbors[i], None))
            else:
                res.append((self.neighbors[i], self.edge_infos[i]))
        return res

'''
拓扑图节点跟踪器的定义。
'''
class GraphTrace():
    '''
    node:GraphNode 初始化跟踪拓扑图的节点。
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
    node:GraphNode 为跟踪器绑定新的拓扑图节点。
    '''
    def __call__(self, node):
        if type(node) == GraphTrace:
            node = node._node
        super().__setattr__('_node', node)
        self._graph.add_node(node)
        self._graph.trace_visit(node, self._color, self._hold)
        return self._node

    '''
    other:GraphNode 判断跟踪器所绑定的节点和other是否相同。
    '''
    def __eq__(self, other):
        return super().__getattribute__('_node') == other
    
    '''
    other:GraphNode 判断跟踪器所绑定的节点和other是否相同。
    '''
    def __ne__(self, other):
        return super().__getattribute__('_node') != other 
    
    '''
    返回：跟踪器所跟踪的图节点中邻居的数量。
    '''
    def __len__(self):
        return len(self.neighbors)
    
    '''
    name:str 访问跟踪器的属性，以及跟踪器所绑定拓扑图节点的val属性。
    '''
    def __getattribute__(self, name):
        if name == 'val':
            return super().__getattribute__('_node').val
        else:
            return super().__getattribute__(name)
    
    '''
    name:str 修改跟踪器的属性，以及跟踪器所绑定拓扑图节点的val属性。
    value:... 新的赋值（对于val属性是直接赋值给跟踪器所绑定拓扑图节点中对应的属性）。
    '''
    def __setattr__(self, name, value):
        if name == 'val':
            setattr(self._node, 'val', value)
            self._graph.update_node_label(self._node, value)
        else:
            super().__setattr__(name, value)

    '''
    index:int 要获取的绑定节点的第index个子节点的索引。
    返回：GraphNode[edge_info] 对应子节点和对应边上权重信息。
    '''
    def __getitem__(self, index):
        node = super().__getattribute__('_node')
        if node.edge_infos is None:
            return node.neighbors[index]
        else:
            return (node.neighbors[index], self.edge_infos[index])
    
    '''
    index:int 要修改的子节点的索引，如果index大于子节点列表长度，则添加子节点。
    value:GraphNode[edge_info] 新的拓扑图节点值[对应边上的权重值]。
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
            self._graph.add_node(child_node)
            node.neighbors.append(child_node)
        else:
            self._graph.add_node(child_node)
            node.neighbors[index] = child_node
        if node.edge_infos is not None:
            if index >= len(node.edge_infos):
                node.edge_infos.append(child_edge)
            else:
                node.edge_infos[index] = child_edge

'''
graph_str:str 表示拓扑图邻接表的json字符串。
directed:bool 该拓扑图是否为有向图。
返回：拓扑图中根结点，如果是离散的图则返回节点集合。
'''
def parseGraph(graph_str, directed=True)
    pass
